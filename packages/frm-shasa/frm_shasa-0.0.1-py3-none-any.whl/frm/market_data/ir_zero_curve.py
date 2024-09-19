# -*- coding: utf-8 -*-
"""
@author: Shasa Foster
https://www.linkedin.com/in/shasafoster
"""

if __name__ == "__main__":
    import os
    import pathlib
    os.chdir(pathlib.Path(__file__).parent.parent.parent.resolve())     
    print('__main__ - current working directory:', os.getcwd())
        
from frm.frm.instruments.ir.swap import Swap
from frm.frm.instruments.ir.leg import Leg
from frm.frm.schedule.daycounter import DayCounter, VALID_DAY_COUNT_BASIS_TYPES
from frm.frm.market_data.iban_ccys import VALID_CCYS
from frm.frm.schedule.business_day_calendar import get_calendar
from frm.frm.schedule.tenor import calc_tenor_date
from frm.frm.schedule.utilities import convert_column_type

from scipy.interpolate import CubicSpline 
import pandas as pd
import numpy as np
from scipy.optimize import fsolve
from dataclasses import dataclass, field, InitVar
from typing import Optional, Union, Literal
import matplotlib.pyplot as plt


VALID_COMPOUNDING_FREQUENCY = Literal['continuously','simple','weekly','daily','monthly','quarterly','semiannually','annually']
VALID_INTERPOLATION_METHOD = Literal['linear_on_log_of_discount_factors','cubic_spline_on_log_of_discount_factors']
VALID_EXTRAPOLATION_METHOD = Literal['none','flat']

@dataclass
class ZeroCurve:
    curve_date: pd.Timestamp
    curve_ccy: str = None 
    
    historical_fixings: InitVar[Optional[pd.DataFrame]] = None
    day_count_basis: InitVar[Optional[VALID_DAY_COUNT_BASIS_TYPES]] = 'act/act'
    zero_data: InitVar[Optional[pd.DataFrame]] = None
    zero_rate_compounding_frequency: InitVar[VALID_COMPOUNDING_FREQUENCY] = 'continuous'
    interpolation_method: VALID_INTERPOLATION_METHOD = 'linear_on_log_of_discount_factors'
    extrapolation_method: VALID_EXTRAPOLATION_METHOD = 'none'
    instruments: InitVar[Optional[dict]] = None
    dsc_crv: InitVar[Optional['ZeroCurve']] = None
    fwd_crv: InitVar[Optional['ZeroCurve']] = None
    
    # Non initialisation arguments
    daycounter: DayCounter = field(init=False)
    df_data: pd.DataFrame = field(init=False, repr=False)
    
    
    def __post_init__(self, historical_fixings, day_count_basis, zero_data, zero_rate_compounding_frequency, instruments, dsc_crv, fwd_crv):
        
        # validate curve_ccy
        if self.curve_ccy is not None:
            self.curve_ccy = self.curve_ccy.lower().strip()
            assert len(self.curve_ccy) in {3,6}
        
        self.daycounter = DayCounter(day_count_basis)
                
        if historical_fixings is not None:
            assert 'date' in historical_fixings.columns and 'fixing' in historical_fixings.columns 
            self.historical_fixings = dict(zip(historical_fixings.date, historical_fixings.fixing)) 
            
        if zero_data is not None:    
            assert 'tenor_date' in zero_data.columns or 'tenor_name' in zero_data.columns
            assert 'discount_factor' in zero_data.columns or 'zero_rate' in zero_data.columns 
            
            if 'tenor_date' not in zero_data.columns:
                if len(self.curve_ccy) == 3:
                    holiday_calendar = get_calendar(ccys=[self.curve_ccy])
                elif len(self.curve_ccy) == 6:
                    holiday_calendar = get_calendar(ccys=[self.curve_ccy[:3],self.curve_ccy[3:]])
  
                tenor_date, tenor_name_cleaned, spot_date = calc_tenor_date(self.curve_date, zero_data['tenor_name'].values, self.curve_ccy, holiday_calendar)
                zero_data['tenor_date'] = tenor_date
                zero_data['tenor_name'] = tenor_name_cleaned
            
            zero_data = convert_column_type(zero_data)
            
            # Construct zero curve from pandas dataframe of dates and discount factors or zero rates
            self.zero_data = {self.curve_date: 1.0}
            
            if 'discount_factor' not in zero_data.columns:
                years = self.daycounter.year_fraction(self.curve_date, zero_data['tenor_date'])

                if zero_rate_compounding_frequency == 'continuous': 
                    zero_data['discount_factor'] = np.exp(-zero_data['zero_rate'] * years)
                elif zero_rate_compounding_frequency == 'monthly': 
                    zero_data['discount_factor'] = 1 / (1+zero_data['zero_rate']/12)**(12*years)
                elif zero_rate_compounding_frequency == 'quarterly': 
                    zero_data['discount_factor'] = 1 / (1+zero_data['zero_rate']/4)**(4*years)
                elif zero_rate_compounding_frequency == 'semi-annual': 
                    zero_data['discount_factor'] = 1 / (1+zero_data['zero_rate']/2)**(2*years)
                elif zero_rate_compounding_frequency == 'annual': 
                    zero_data['discount_factor'] = 1 / (1+zero_data['zero_rate']/1)**(1*years)
                else: 
                    raise ValueError("The zero rate compounding frequency '" + zero_rate_compounding_frequency + "' is not supported")
                
            for i,row in zero_data.iterrows():
                self.zero_data[row['tenor_date']] = row['discount_factor']
                 
            self.__interpolate_zero_data()
                
        else:
            # Or bootstrap zero curve from par instruments
            self.__bootstrap(instruments=instruments, dsc_crv=dsc_crv, fwd_crv=fwd_crv)
    

    def __interpolate_zero_data(self):
        tenor_dates = list(self.zero_data.keys())
        years = self.daycounter.year_fraction(self.curve_date, tenor_dates)
        date_range = pd.date_range(self.curve_date,max(tenor_dates),freq='d')
        years_to_date = self.daycounter.year_fraction(self.curve_date,date_range)
        
        if self.interpolation_method == 'cubic_spline_on_log_of_discount_factors':
            log_discount_obj = CubicSpline(years,-np.log(list(self.zero_data.values())))
            self.df_data = pd.DataFrame({'date':date_range.to_list(), 
                                         'years_to_date': years_to_date, 
                                         'discount_factor': np.exp(-log_discount_obj(years_to_date))})
        elif self.interpolation_method == 'linear_on_log_of_discount_factors':            
            interpolated = np.interp(years_to_date, years, -np.log(list(self.zero_data.values())))
            self.df_data = pd.DataFrame({'date':date_range.to_list(), 
                                         'years_to_date': years_to_date, 
                                         'discount_factor': np.exp(-interpolated)})        
        
        
    def __bootstrap(self, 
                  instruments: dict,
                  dsc_crv: Optional['ZeroCurve']=None,
                  fwd_crv: Optional['ZeroCurve']=None):
        
        # When dsc_crv is specified, we apply the dsc_crv to all relevent instruments and solve the fwd_crv that gives them a par value 
        # Example: 
        # Solving for the USD LIBOR 3M forward curve from USD LIBOR 3M fix-flt par swaps quoted from LCH (i.e that are fully collatarised). 
        # As these instruments are collatarised the discount curve does not equal the forward curve. 
        # We must solve this curve prior (i.e a USD SOFR curve or a cheapest-to-deliver OIS curve) and input it as the dsc_crv.
        
        # When fwd_crv is specified, we apply the fwd_crv to all relevent instruments and solve the dsc_crv that gives them a par value
        # Example:
        # Solving for the discount curve from USD floating rate bonds that reference USD LIBOR 1M
        # We must solve the USD LIBOR 1M curve prior and input this as the fwd_crv. 
        # As these instruments are collatarised the discount curve does not equal the forward curve. 
        # We must solve this discount curve prior (i.e a USD SOFR curve or a cheapest-to-deliver OIS curve)
        
        # This functionality will cover most most applications.  
        # This fuctionality does NOT cover the case you want to boostrap with 
        # a set of instruments reference this curve as the forward curve
        # with another set of instruments that reference this curve as the discount curve. 
        

        self.zero_data = {self.curve_date: 1.0}
        self.df_data = pd.DataFrame({'date': [self.curve_date],
                                     'years_to_date': [0.0], 
                                     'discount_factor': [1.0]})

        if 'deposits' in instruments.keys():
            deposits = instruments['deposits']
            deposits.sort(key=lambda x: x.maturity_date, reverse=False) 
            for deposit in instruments['deposits']:
                assert deposit.effective_date == self.curve_date, f"deposit.effective_date: {deposit.effective_date}, self.curve_date: {self.curve_date}"
                self.zero_data[deposit.maturity_date] = deposit.implied_discount_factor()
            self.__interpolate_zero_data()

        if 'futures' in instruments.keys():
            futures = instruments['futures']
            futures.sort(key=lambda x: x.maturity_date, reverse=False) 
            # Bootstrapping using futures/FRAs requires the futures to have overlap over the end and start dates of two successive futures
            # For example, a future ends on 15 June 2022, the next future must start on 15 June 2022 or earlier            
            for i,future in enumerate(futures):
                self.zero_data[future.maturity_date] = self.discount_factor(pd.Timestamp(future.effective_date)).at[0] \
                    / (future.forward_interest_rate * future.daycounter.year_fraction(future.effective_date,future.maturity_date) + 1)                                        
                self.__interpolate_zero_data()
        
        if 'FRAs' in instruments.keys():
            FRAs = instruments['FRAs']
            FRAs.sort(key=lambda x: x.maturity_date, reverse=False) 
            # Bootstrapping using futures/FRAs requires the futures to have overlap over the end and start dates of two successive futures
            # For example, a future ends on 15 June 2022, the next future must start on 15 June 2022 or earlier            
            for i,fra in enumerate(FRAs):
                self.zero_data[fra.maturity_date] = self.discount_factor([pd.Timestamp(future.effective_date)]).at[0] \
                    / (fra.forward_interest_rate * fra.daycounter.year_fraction(fra.effective_date,fra.maturity_date) + 1)                                        
                self.__interpolate_zero_data()
             
        if 'swaps' in instruments.keys():
            swaps = instruments['swaps']
            swaps.sort(key=lambda x: x.pay_leg.schedule['payment_date'].iloc[-1], reverse=False) 
            
            for i,swap in enumerate(swaps):
                final_payment_date = swap.pay_leg.schedule['payment_date'].iloc[-1]

                if final_payment_date > self.df_data['date'].iloc[-1]:
                    
                    # Set the initial guess to be the swaps par coupon rate
                    zero_rate = swap.pay_leg.fixed_rate if swap.pay_leg.leg_type == 'fixed' else swap.rec_leg.fixed_rate   
                    self.zero_data[final_payment_date] = np.exp(-zero_rate * self.daycounter.year_fraction(self.curve_date, final_payment_date))
                    
                    if dsc_crv is not None:
                        swap.set_discount_curve(dsc_crv)
                    if fwd_crv is not None:
                        swap.set_forward_curve(fwd_crv)
                    
                    def solve_to_par(zero_cpn_rate: [float],
                                     swap: Swap,
                                     zero_curve: ZeroCurve,
                                     final_payment_date: pd.Timestamp,
                                     solve_fwd_crv: bool,
                                     solve_dsc_crv: bool):
                        
                        zero_curve.zero_data[final_payment_date] = \
                            np.exp(-zero_cpn_rate[0] * zero_curve.daycounter.year_fraction(zero_curve.curve_date, final_payment_date))
                        zero_curve.__interpolate_zero_data()
              
                        if solve_fwd_crv:
                            swap.set_forward_curve(zero_curve)
                        if solve_dsc_crv:
                            swap.set_discount_curve(zero_curve)

                        
                        pricing = swap.price()
                        return pricing['price']
                    
                    solve_fwd_crv = fwd_crv is None
                    solve_dsc_crv = dsc_crv is None    
                    x, infodict, ier, msg = fsolve(solve_to_par, [
                                                   zero_rate], 
                                                   args=(swap, self, final_payment_date, solve_fwd_crv, solve_dsc_crv), 
                                                   full_output=True)

                    self.zero_data[final_payment_date] = np.exp(-x[0] * self.daycounter.year_fraction(self.curve_date, final_payment_date))
                    self.__interpolate_zero_data()
                    
                    if ier != 1:
                        print('Error bootstrapping swap with maturity', swap.pay_leg.maturity_date.strftime('%Y-%m-%d'), msg)                        
                else:        
                    print('Swap with maturity', swap.pay_leg.maturity_date.strftime('%Y-%m-%d'), \
                          'excluded from bootstrapping as prior instruments have covered this period.')

        if 'legs' in instruments.keys():
            legs = instruments['legs']
            legs.sort(key=lambda x: x.schedule['payment_date'].iloc[-1], reverse=False) 
            
            for i,leg in enumerate(legs):
                final_payment_date = leg.schedule['payment_date'].iloc[-1]

                if final_payment_date > self.df_data['date'].iloc[-1]:
                    
                    # Set the initial guess to be the swaps par coupon rate
                    zero_rate = leg.fixed_rate if leg.leg_type == 'fixed' else leg.fixed_rate   
                    self.zero_data[final_payment_date] = np.exp(-zero_rate * self.daycounter.year_fraction(self.curve_date, final_payment_date))
                    
                    if dsc_crv is not None:
                        leg.set_discount_curve(dsc_crv)
                    if fwd_crv is not None:
                        leg.set_forward_curve(fwd_crv)
                    
                    def solve_to_par(zero_cpn_rate: [float],
                                     leg: Leg,
                                     zero_curve: ZeroCurve,
                                     final_payment_date: pd.Timestamp,
                                     solve_fwd_crv: bool,
                                     solve_dsc_crv: bool):
                        
                        zero_curve.zero_data[final_payment_date] = \
                            np.exp(-zero_cpn_rate[0] * zero_curve.daycounter.year_fraction(zero_curve.curve_date, final_payment_date))
                        zero_curve.__interpolate_zero_data()
              
                        if solve_fwd_crv:
                            leg.set_forward_curve(zero_curve)
                        if solve_dsc_crv:
                            leg.set_discount_curve(zero_curve)

                        
                        pricing = leg.price()
                        return pricing['price'] - leg.notional * (leg.transaction_price / 100.0)
                    
                    solve_fwd_crv = fwd_crv is None
                    solve_dsc_crv = dsc_crv is None    
                    x, infodict, ier, msg = fsolve(solve_to_par, [
                                                   zero_rate], 
                                                   args=(leg, self, final_payment_date, solve_fwd_crv, solve_dsc_crv), 
                                                   full_output=True)

                    self.zero_data[final_payment_date] = np.exp(-x[0] * self.daycounter.year_fraction(self.curve_date, final_payment_date))
                    self.__interpolate_zero_data()
                    
                    if ier != 1:
                        print('Error bootstrapping leg with maturity', leg.maturity_date.strftime('%Y-%m-%d'), msg)                        
                else:        
                    print('Leg with maturity', leg.maturity_date.strftime('%Y-%m-%d'), \
                          'excluded from bootstrapping as prior instruments have covered this period.')


    
    
    def flat_shift(self, 
                   basis_points: float=1) -> 'ZeroCurve':
        tenor_dates = list(self.zero_data.keys())
        years_to_date = self.daycounter.year_fraction(self.curve_date, tenor_dates)
        shifted = - np.log(list(self.zero_data.values())) / years_to_date + basis_points / 10000    
        df_shifted_data = pd.DataFrame({'tenor_date': tenor_dates, 
                                        'years_to_date': years_to_date, 
                                        'discount_factor':np.exp(-shifted * years_to_date)})
        df_shifted_data.loc[0,'discount_factor'] = 1.0 # set the discount factor on the curve date to be 1.0
        return ZeroCurve(curve_date=self.curve_date, 
                         zero_data = df_shifted_data,
                         day_count_basis = self.daycounter.day_count_basis)
                   
    def forward_rate(self,
                     d1: Union[pd.Timestamp, pd.Series],
                     d2: Union[pd.Timestamp, pd.Series],
                     compounding_frequency: VALID_COMPOUNDING_FREQUENCY='simple') -> pd.Series:

        assert len(d1) == len(d2)
        assert type(d1) == type(d2)
        
        bool_cond = d1 < self.curve_date
        
        historical_fixings = []
        if sum(bool_cond) > 0:
            historical_fixings = pd.Series([self.historical_fixings[d] if d in self.historical_fixings.keys() else np.nan for d in d1[bool_cond]])
            
        years = pd.Series(self.daycounter.year_fraction(d1, d2))            
        
        dsc_d1 = self.discount_factor(d1[np.logical_not(bool_cond)])
        dsc_d2 = self.discount_factor(d2[np.logical_not(bool_cond)])
        
        # https://en.wikipedia.org/wiki/Forward_rate
        if compounding_frequency == 'simple':
            forward_fixings = pd.Series(list((1 / years) * (dsc_d1 / dsc_d2 - 1)))
        elif compounding_frequency == 'yearly':
            forward_fixings = pd.Series(list( (dsc_d1 / dsc_d2) ** (1/years)  - 1 ))
        elif compounding_frequency == 'continuously':
            forward_fixings = pd.Series(list((1 / years) * (np.log(dsc_d1) - np.log(dsc_d2))))
        
        forward_fixings[years==0] = 0
        
        return pd.Series(historical_fixings + forward_fixings.to_list())
       

    def discount_factor(self,  
                        dates: Union[pd.Timestamp, pd.Series]) -> pd.Series:
        if type(dates) is pd.Timestamp: 
            dates = pd.Series([dates])
        return pd.Series(pd.merge(pd.DataFrame(data=dates.values, columns=['date']), self.df_data, left_on='date',right_on='date')['discount_factor'].values)

    
    def zero_rate(self, 
                  dates: Union[pd.Timestamp, pd.Series],
                  compounding_frequency: VALID_COMPOUNDING_FREQUENCY='continuously') -> pd.Series:
                
        if type(dates) is pd.Timestamp: dates = pd.Series([dates])
        
        if self.extrapolation_method == 'none':    
            msg = ". NaN will be returned. Consider applying the ZeroCurve 'extrapolation_method'"
        elif self.extrapolation_method == 'flat':
            msg = '. Flat extropolation will be applied.'
        
        # check if any of the dates are outside the available data
        min_date = self.df_data['date'].min()
        below_range = dates < min_date
        dates_below = []
        if any(below_range):
            bound_date = self.df_data['date'].min()
            for i,date in enumerate(dates[below_range]):
                print('Date', date.strftime('%Y-%m-%d'), 'is below the min available data of ' + bound_date.strftime('%Y-%m-%d') + msg)
                if self.extrapolation_method == 'none':    
                    dates_below.append(np.nan)
                elif self.extrapolation_method == 'flat':    
                    dates_below.append(bound_date)
        
        max_date = self.df_data['date'].max()
        above_range = dates > max_date
        dates_above = []
        if any(above_range):
            bound_date = self.df_data['date'].max()
            for i,date in enumerate(dates[above_range]):
                print('Date', date.strftime('%Y-%m-%d'), 'is above the max available data of ' + bound_date.strftime('%Y-%m-%d') + msg)
                if self.extrapolation_method == 'none':    
                    dates_above.append(np.nan)
                elif self.extrapolation_method == 'flat':    
                    dates_above.append(bound_date)
      
        in_range = np.logical_and(np.logical_not(below_range),np.logical_not(above_range))
        cleaned_dates = dates_below + list(dates[in_range].values) + dates_above
        
        # this would be quicker if used pandas index
        df = pd.merge(pd.DataFrame(data=cleaned_dates, columns=['date']), self.df_data, left_on='date',right_on='date', how='left')
        if compounding_frequency == 'continuously':
            result = (- np.log(df['discount_factor']) / df['years_to_date'])
        elif compounding_frequency == 'daily':
            days_to_date = self.daycounter.day_count(self.curve_date,df['date']) 
            result = (days_to_date * ((1 / df['discount_factor']) ** (1.0 / (days_to_date * df['years_to_date'])) - 1.0))
        elif compounding_frequency == 'monthly':
            result = (12.0 * ((1.0 / df['discount_factor']) ** (1.0 / (12.0 * df['years_to_date'])) - 1.0))
        elif compounding_frequency == 'quarterly':
            result = (4.0 * ((1.0 / df['discount_factor']) ** (1.0 / (4.0 * df['years_to_date'])) - 1.0))
        elif compounding_frequency == 'semi-annually':
            result = (2.0 * ((1.0 / df['discount_factor']) ** (1.0 / (2.0 * df['years_to_date'])) - 1.0))
        elif compounding_frequency == 'annually':
            result = ((1.0 / df['discount_factor']) ** (1.0 / df['years_to_date']) - 1.0)
        elif compounding_frequency == 'simple':
            result = (((1.0 / df['discount_factor']) - 1.0) / df['years_to_date'])
    
        return result
        
        
    def plot(self, forward_rate_terms=[90]):
            

        # Zero rates
        min_date = self.df_data['date'].iloc[1]
        max_date = self.df_data['date'].iloc[-1]
        date_range = pd.date_range(min_date,max_date,freq='d')
        years_zr = self.daycounter.year_fraction(self.curve_date,date_range)
        zero_rates = pd.Series(self.zero_rate(date_range)) * 100
        
        fig, ax = plt.subplots()
        
        ax.plot(years_zr, zero_rates, label='zero rate')  
  
        # Forward rates
        for term in forward_rate_terms:
            d1 = pd.date_range(min_date,max_date - pd.DateOffset(days=term),freq='d')
            d2 = pd.date_range(min_date + pd.DateOffset(days=term),max_date ,freq='d')
        
            years_fwd = self.daycounter.year_fraction(self.curve_date,d1)
            fwd_rates = pd.Series(self.forward_rate(d1,d2)) * 100       
        
            ax.plot(years_fwd, fwd_rates, label=str(term)+' day forward rate') 
        
        ax.set(xlabel='years', ylabel='interest rate (%)')
        
        ax.grid()
        ax.legend()
        plt.xlim([min(years_zr), 1.05*max(years_zr)])
        plt.show()

    def subtract_curve(self, 
                   zero_curve: 'ZeroCurve',
                   day_count_basis: Optional[VALID_DAY_COUNT_BASIS_TYPES]=None,
                   name: Optional[str]=None,
                   task=None):
    
        # Returns a zero curve constructed from zero rates where,
        # zero rates = self.zero_rates - zero_curve.zero_rates
        
        assert self.curve_date == zero_curve.curve_date        
        if day_count_basis is None:
            day_count_basis = self.daycounter.day_count_basis
            
        if name is None:
            if self.name is not None and zero_curve.name is not None:
                name = '[' + self.name + '] - [' + zero_curve.name + ']'
            
        min_date = min(self.df_data['date'].iloc[-1], zero_curve.df_data['date'].iloc[-1])

        date_range = pd.date_range(self.curve_date, min_date,freq='d')
        date_range = date_range[1:] # exclude the zero_rate on self.data which is probably a np.nan

        zero_rates_self = self.zero_rate(date_range)
        zero_rates_other = zero_curve.zero_rate(date_range)
        
        zero_rate_difference = zero_rates_self - zero_rates_other
        df_diff = pd.DataFrame({'date': date_range,
                                'zero_rate': zero_rate_difference})
        
        return ZeroCurve(date=self.curve_date, 
                         name=name,
                         zero_data=df_diff,
                         day_count_basis=day_count_basis)
        
    
    def add_curve(self, 
                  zero_curve: 'ZeroCurve',
                  day_count_basis: Optional[VALID_DAY_COUNT_BASIS_TYPES]=None,
                  name: Optional[str]=None):
    
        # Returns a zero curve constructed from zero rates where,
        # zero rates = self.zero_rates + zero_curve.zero_rates
        
        assert self.curve_date == zero_curve.curve_date        
        if day_count_basis is None:
            day_count_basis = self.daycounter.day_count_basis
            
        if name is None:
            if self.name is not None and zero_curve.name is not None:
                name = '[' + self.name + '] + [' + zero_curve.name + ']'
            
        min_date = min(self.df_data['date'].iloc[-1], zero_curve.df_data['date'].iloc[-1])

        date_range = pd.date_range(self.curve_date, min_date,freq='d')
        date_range = date_range[1:] # exclude the zero_rate on self.data which is probably a np.nan

        zero_rates_self = self.zero_rate(date_range)
        zero_rates_other = zero_curve.zero_rate(date_range)
        
        zero_rate_difference = zero_rates_self + zero_rates_other
        df_diff = pd.DataFrame({'date': date_range,
                                'zero_rate': zero_rate_difference})
        
        return ZeroCurve(date=self.curve_date, 
                         name=name,
                         zero_data=df_diff,
                         day_count_basis=day_count_basis)
        
        
        
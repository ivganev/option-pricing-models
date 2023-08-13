
from instrument_market_classes import OptionClass, MarketConditions
from matplotlib import pyplot as plt
from pricing_model_menagerie import *


class PricingModel:
    def __init__(self, model_name: str, params: dict, conditions: MarketConditions) -> None:
        self.model_name = model_name
        self.params = params
        self.conditions = conditions
        self.max_strike_of_interest=conditions.max_strike_of_interest
        self.min_strike_of_interest=conditions.min_strike_of_interest

        if model_name == "Black-Scholes":
            assert 'volatility' in params, "Missing paramter"
            self.model = BlackScholes(volatility=params['volatility'])

        elif model_name == "Quadratic volatility smile":
            assert 'atm_vol' in params, "Missing parameter"
            assert 'skew' in params, "Missing parameter"
            assert 'curvature' in params, "Missing parameter"
            self.model = VolSmileQuadratic(
                c0=params['atm_vol'], 
                c1=params['skew'], 
                c2=params['curvature'])
        elif model_name == "Hyperbolic volatility smile":
            assert 'atm_vol' in params, "Missing parameter"
            assert 'skew' in params, "Missing parameter"
            assert 'right_asymp' in params, "Missing parameter"
            assert 'left_asymp' in params, "Missing parameter"
            self.model = VolSmileHyperbolic(
                c0=params['atm_vol'], 
                c1=sqrt(params['skew']*2*params['atm_vol']), 
                c2_plus=params['right_asymp'], 
                c2_minus=params['left_asymp'])
        elif model_name == "Binomial":
            assert 'up_tick' in params, "Missing parameter"
            assert 'down_tick' in params, "Missing parameter"
            assert 'num_intervals' in params, "Missing parameter"
            self.model = Binomial(
                up_tick=params['up_tick'], 
                down_tick=params['down_tick'], 
                num_intervals=params['num_intervals'])
        else:
            assert False, "Unrecognized model type"

    def info_string(self, time_to_expiry: float) -> str:
        info_string = f"Model type:\n{self.model_name}" 
        info_string += "\n\nParameters:"
        for p in self.params:
            info_string += f"\n{p}: {round(self.params[p],4)}"
        info_string += "\n\nConditions:" + f"\nspot={self.conditions.spot}" + f"\ntime_to_expiry={round(time_to_expiry,4)}" + f"\ninterest_rate={self.conditions.interest_rate}"
        return info_string
               

    def model_pricing_function(self, option: OptionClass, time_value_only=False):
        if self.model_name == "Black-Scholes":
            price = self.model.bs_pricing_function(option=option, conditions=self.conditions)
        elif self.model_name == "Quadratic volatility smile":
            price = self.model.quadratic_pricing_function(option=option, conditions=self.conditions)
        elif self.model_name == "Hyperbolic volatility smile":
            price = self.model.hyperbolic_pricing_function(option=option, conditions=self.conditions)
        elif self.model_name == "Binomial":
            price = self.model.binomial_pricing_function(option=option, conditions=self.conditions)
        if time_value_only:
            if option.option_type == "call":
                price -= max(0, self.conditions.spot - option.strike)
            else: 
                price -= max(0, option.strike - self.conditions.spot)
        return price
        
    def pricing_plot(
            self, 
            time_to_expiry: float, 
            num_samples=100,
            plot=True,
            time_value_only=False
        ) -> dict:
        min_strike= self.min_strike_of_interest
        max_strike= self.max_strike_of_interest
        step_size = (max_strike - min_strike )/num_samples
        strikes = [min_strike + i*step_size for i in range(num_samples)]
        call_prices = [
            self.model_pricing_function(
                option=OptionClass(strike=K, time_to_expiry=time_to_expiry, option_type="call"), 
                time_value_only=time_value_only)
            for K in strikes
        ]
        put_prices = [
            self.model_pricing_function(
                option=OptionClass(strike=K, time_to_expiry=time_to_expiry, option_type="put"), 
                time_value_only=time_value_only)
            for K in strikes
        ]

        if plot:
            plt.plot(strikes, call_prices, label="calls")
            plt.plot(strikes, put_prices, label="puts")
            plt.title(f"Option prices")
            plt.xlabel("strike")
            plt.ylabel("price")
            plt.figtext(0.95, 0.5,
                self.info_string(time_to_expiry=time_to_expiry), 
                horizontalalignment ="left", verticalalignment ="center", 
                wrap = True, fontsize = 10)
            plt.legend()    
            plt.show()
        return {'strikes' : strikes, 'call_prices' : call_prices, 'put_prices' : put_prices}
    
    def butterfly_price(self, option: OptionClass, radius: float):
        abbrev_pricing_function = lambda x: self.model_pricing_function(
            option=OptionClass(strike=x, time_to_expiry=option.time_to_expiry, option_type=option.option_type)
            )
        left_wing = abbrev_pricing_function(option.strike - radius)
        body = abbrev_pricing_function(option.strike)
        right_wing = abbrev_pricing_function(option.strike + radius)
        return round(left_wing - 2*body + right_wing, 9) 
    
    def probability_distribution_plot(
            self,
            time_to_expiry: float,

            precision=0.1,
            num_samples=100,
            plot=True
        ):
        max_strike=self.max_strike_of_interest
        min_strike=self.min_strike_of_interest
        step_size = (max_strike - min_strike )/num_samples
        strikes = [min_strike + i*step_size for i in range(num_samples)]
        probs = [
            self.butterfly_price(
                option=OptionClass(strike=K, time_to_expiry=time_to_expiry, option_type="call"),
                radius=precision
            )/(precision*precision) for K in strikes
        ]
        if plot:
            plt.plot(strikes, probs)
            plt.title("Risk-neutral probability density function")
            plt.xlabel("price of underlying")
            plt.figtext(0.95, 0.5,
                self.info_string(time_to_expiry=time_to_expiry),
                horizontalalignment ="left", verticalalignment ="center", 
                wrap = True, fontsize = 10)
            plt.show()
        return {'strikes': strikes, 'probs': probs}

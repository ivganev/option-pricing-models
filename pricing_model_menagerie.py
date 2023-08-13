
from helper_functions import choose, gluing_function, black_scholes_formula
from instrument_market_classes import OptionClass, MarketConditions
from matplotlib import pyplot as plt
from math import log, sqrt, exp
from helper_functions import relu


class BlackScholes:
    def __init__(self, volatility) -> None:
        assert volatility > 0, "Volatility must be positive"
        self.volatility = volatility

    def bs_pricing_function(self, conditions: MarketConditions, option: OptionClass) -> float:
        return black_scholes_formula(
            spot=conditions.spot, 
            strike=option.strike,
            volatility=self.volatility,
            time_to_expiry=option.time_to_expiry, 
            interest_rate=conditions.interest_rate,
            option_type=option.option_type
        )

##################################

class VolSmileQuadratic:
    def __init__(self, c0: float, c1: float, c2: float) -> None:
        assert c0 > 0, "Volatility must be positive"
        assert c1*c1 - 4*c0*c2 <= 0, "Invalid parameters"
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2

    def quadratic_vol_smile_function(self, x):
        return self.c0 + self.c1*x + self.c2*x*x

    def plot_smile(self, min_d1=-4, max_d1=4, num_samples=100):
        step_size = (max_d1 - min_d1 )/num_samples
        d1s = [min_d1 + i*step_size for i in range(num_samples)]
        vols = [self.quadratic_vol_smile_function(d1) for d1 in d1s]

        plt.plot(d1s, vols, color="black")
        plt.ylim([0,max(1,max(vols)*1.2)])
        plt.title("A quadratic volatility smile" )
        plt.xlabel("d1 value")
        plt.ylabel("volatility")
        plt.figtext(1.0, 0.8,
            f"atm-vol={self.c0}\nskew={self.c1}\ncurvature={self.c2}",
            horizontalalignment ="left", 
            verticalalignment ="center", 
            wrap = True, fontsize = 10)
        plt.show()

    def quadratic_pricing_function(self, option: OptionClass, conditions: MarketConditions) -> float:
        strike, time_to_expiry = option.strike, option.time_to_expiry
        spot, interest_rate = conditions.spot, conditions.interest_rate
        d1 = (log(spot/strike) + interest_rate*time_to_expiry)/(self.c0*sqrt(time_to_expiry))
        vol = self.quadratic_vol_smile_function(x=d1)
        return black_scholes_formula(
            spot=conditions.spot, 
            strike=option.strike,
            time_to_expiry=option.time_to_expiry,
            volatility=vol, 
            interest_rate=conditions.interest_rate,
            option_type=option.option_type
        )

##################################

class VolSmileHyperbolic:
    def __init__(self, c0: float, c1: float, c2_plus: float, c2_minus) -> None:
        assert min(c0,c1,c2_minus, c2_plus) > 0, "All parameters must be positive"
        assert max(c1*c1*c1*c1 - 4*c0*c0*c2_plus*c2_plus, c1*c1*c1*c1 - 4*c0*c0*c2_minus*c2_minus) < 0, "Invalid parameters"
        self.c0 = c0
        self.c1 = c1
        self.c2_plus = c2_plus
        self.c2_minus = c2_minus

    def hyperbolic_vol_smile_function(self, x, glue_end_point=3):
        f_plus = sqrt(self.c0*self.c0 + self.c1*self.c1*x + self.c2_plus*self.c2_plus*x*x)
        f_minus = sqrt(self.c0*self.c0 + self.c1*self.c1*x + self.c2_minus*self.c2_minus*x*x)
        interpolation = gluing_function((x+glue_end_point)/(2*glue_end_point))
        return interpolation*f_plus + (1-interpolation)*f_minus

    def plot_smile(self, min_d1=-4, max_d1=4, num_samples=100):
        step_size = (max_d1 - min_d1 )/num_samples
        d1s = [min_d1 + i*step_size for i in range(num_samples)]
        vols = [self.hyperbolic_vol_smile_function(d1) for d1 in d1s]

        plt.plot(d1s, vols, color="black")
        plt.ylim([0,max(1,max(vols)*1.2)])
        plt.title("A hyperbolic volatility smile" )
        plt.xlabel("d1 value")
        plt.ylabel("volatility")
        plt.figtext(1.0, 0.8,
            f"atm-vol={self.c0}\nskew={round(self.c1*self.c1/(2*self.c0),4)}\nright_asymptote={-self.c2_minus}\nleft_asymptote={self.c2_plus}",
            horizontalalignment ="left", 
            verticalalignment ="center", 
            wrap = True, fontsize = 10)
        plt.show()

    def hyperbolic_pricing_function(self, option: OptionClass, conditions: MarketConditions) -> float:
        strike, time_to_expiry = option.strike, option.time_to_expiry
        spot, interest_rate = conditions.spot, conditions.interest_rate
        d1 = (log(spot/strike) + interest_rate*time_to_expiry)/(self.c0*sqrt(time_to_expiry))
        vol = self.hyperbolic_vol_smile_function(x=d1)
        return black_scholes_formula(
            spot=conditions.spot, 
            strike=option.strike,
            time_to_expiry=option.time_to_expiry,
            volatility=vol, 
            interest_rate=conditions.interest_rate,
            option_type=option.option_type
        )

#####################

class Binomial:
    def __init__(self, up_tick: float, down_tick: float, num_intervals: int) -> None:
        assert min(up_tick, down_tick, num_intervals) > 0, "All parameters must be positive"
        assert 0 < down_tick < up_tick, "Invalid parameters"
        self.up_tick = up_tick
        self.down_tick = down_tick
        self.num_intervals = num_intervals

    def binomial_pricing_function(self, option: OptionClass, conditions: MarketConditions) -> float:
        strike, time_to_expiry = option.strike, option.time_to_expiry
        spot, interest_rate = conditions.spot, conditions.interest_rate
        time_interval = time_to_expiry/self.num_intervals

        up_tick = self.up_tick
        down_tick = self.down_tick
        interest = exp(interest_rate*time_interval)

        assert down_tick < interest and interest < up_tick, "There is no probability eliminating arbitrage"
        martingale_prob = (interest - down_tick)/(up_tick - down_tick)

        running_sum = 0
        for i in range(self.num_intervals+1):
            Sfinal = spot*(up_tick**i)*(down_tick**(self.num_intervals-i))
            probability = (martingale_prob**i)*((1-martingale_prob)**(self.num_intervals-i))
            if option.option_type == "call":
                running_sum += choose(i,self.num_intervals)*relu(Sfinal - strike)*probability
            else:
                running_sum += choose(i,self.num_intervals)*relu(strike - Sfinal)*probability
        discount_factor = exp(-interest_rate*time_to_expiry)
        return discount_factor*running_sum




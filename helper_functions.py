from scipy.stats import norm
import scipy.stats
from math import log, exp, sqrt

Norm = scipy.stats.norm.cdf

# Black-Scholes formula
def black_scholes_formula(
        spot: float, 
        strike: float, 
        volatility: float, 
        time_to_expiry: float,
        interest_rate = 0.0, 
        option_type = "call"
    ):
    assert option_type == "call" or option_type == "put", "Invalid option type; must be 'call' or 'put'"
    dplus = (log(spot/strike) + (interest_rate + (volatility**2)*0.5)*time_to_expiry)/(volatility*sqrt(time_to_expiry))
    dminus = (log(spot/strike) + (interest_rate - (volatility**2)*0.5)*time_to_expiry)/(volatility*sqrt(time_to_expiry))
    if option_type == "call":
        return spot*Norm(dplus) - strike*exp(-interest_rate*time_to_expiry)*Norm(dminus)
    else:
        return strike*exp(-interest_rate*time_to_expiry)*Norm(-dminus) - spot*Norm(-dplus)
    
# Smooth gluing function, constantly zero on {x<=0}, constantly one on {x>=1}
def gluing_function(x):
    if 0 < x < 1:
        return exp(-1/x)/(exp(-1/x) + exp(-1/(1-x)))
    elif x <= 0:
        return 0
    else:
        return 1
    
# ReLu function
def relu(x):
    return max(x,0)
    
# Choose function
def choose(k, n):
    a = 1
    for i in range(k):
        a *= (n-i)/(i+1)
    return a


assert choose(2,4) == 6, "choose function error"
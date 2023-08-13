from instrument_market_classes import MarketConditions
from comparisons import ModelAndParams
from comparisons import compare_pricing_models, compare_distributions
from math import exp, sqrt


def run_experiments(
		conditions: MarketConditions,
		bs_vol: float, 
		option_time_to_expiry: float
	):

	models_to_compare1 = [
	        ModelAndParams(
	            model_name="Black-Scholes", 
	            params={'volatility': bs_vol}),
	        ModelAndParams(
	            model_name="Quadratic volatility smile", 
	            params={"atm_vol":bs_vol, 'skew':0.03, 'curvature':0.035}),
	        ModelAndParams(
	            model_name="Hyperbolic volatility smile", 
	            params={"atm_vol":bs_vol, 'skew':0.03, 'right_asymp':0.2, 'left_asymp':0.17})
	    ]

	compare_pricing_models(
	    models_list=models_to_compare1, 
	    time_to_expiry=option_time_to_expiry,
	    conditions=conditions
	)

	compare_distributions(
	    models_list=models_to_compare1, 
	    time_to_expiry=option_time_to_expiry,
	    conditions=conditions
	)

	models_to_compare2 = [
	        ModelAndParams(
	            model_name="Black-Scholes", 
	            params={'volatility': bs_vol})
	            ]

	for n in [2, 5, 10]:
	    models_to_compare2.append(
	        ModelAndParams(
	            model_name="Binomial", 
	            params={
	                'up_tick': exp(bs_vol*sqrt(option_time_to_expiry/n)), 
	                'down_tick': exp(-bs_vol*sqrt(option_time_to_expiry/n)), 
	                'num_intervals': n}
	    ))

	compare_pricing_models(
	    models_list=models_to_compare2,
	    time_to_expiry=option_time_to_expiry,
	    conditions=conditions,
	    num_samples=100
	)

	models_to_compare3 = [
	        ModelAndParams(
	            model_name="Black-Scholes", 
	            params={'volatility': bs_vol})
	            ]
	for m in [100, 1000]:
	    models_to_compare3.append(
	        ModelAndParams(
	            model_name="Binomial", 
	            params={
	                'up_tick': exp(bs_vol*sqrt(option_time_to_expiry/m)), 
	                'down_tick': exp(-bs_vol*sqrt(option_time_to_expiry/m)), 
	                'num_intervals': m}
	    ))

	compare_distributions(
	    models_list=models_to_compare3,
	    time_to_expiry=option_time_to_expiry,
	    conditions=conditions,
	    num_samples=200
	)


def main():
	run_experiments(
		MarketConditions(spot=100, interest_rate=0.01),
		bs_vol=0.4,
		option_time_to_expiry=2/12)

main()
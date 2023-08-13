from instrument_market_classes import MarketConditions
from pricing_model_class import PricingModel


def run_experiments(
	conditions: MarketConditions, 
	bs_vol: float,
	option_time_to_expiry: float):

	bs_model = PricingModel(
	    model_name="Black-Scholes", 
	    params={'volatility': bs_vol}, 
	    conditions= conditions
	    )
	bs_model.model.volatility
	bs_model.pricing_plot(time_to_expiry=option_time_to_expiry, time_value_only=False)
	bs_model.probability_distribution_plot(time_to_expiry=option_time_to_expiry)


	quad_vs_model = PricingModel(
	    model_name="Quadratic volatility smile", 
	    params={'atm_vol': bs_vol, 'skew': 0.03, 'curvature': 0.015}, 
	    conditions= conditions
	    )
	quad_vs_model.model.plot_smile()
	quad_vs_model.pricing_plot(time_to_expiry=option_time_to_expiry, time_value_only=False)
	quad_vs_model.probability_distribution_plot(time_to_expiry=option_time_to_expiry)

	hyp_vs_model = PricingModel(
	    model_name="Hyperbolic volatility smile", 
	    params={'atm_vol': bs_vol, 'skew': 0.01, 'left_asymp': 0.15, 'right_asymp' : 0.1}, 
	    conditions= conditions
	    )
	hyp_vs_model.model.plot_smile()
	hyp_vs_model.pricing_plot(time_to_expiry=option_time_to_expiry, time_value_only=False)
	hyp_vs_model.probability_distribution_plot(time_to_expiry=option_time_to_expiry)

	binomial_model = PricingModel(
	    model_name="Binomial", 
	    params={'up_tick': 1.1, 'down_tick': 0.9, 'num_intervals': 5}, 
	    conditions= conditions
	    )
	binomial_model.pricing_plot(time_to_expiry=option_time_to_expiry, time_value_only=True)
	binomial_model.pricing_plot(time_to_expiry=option_time_to_expiry, time_value_only=False)
	binomial_model.probability_distribution_plot(time_to_expiry=option_time_to_expiry, precision=0.01, num_samples=100)


def main():
	current_conditions =  MarketConditions(spot=100, interest_rate=0.01)
	current_conditions.set_min_max_strikes_of_interest(
		new_min_strike_of_interest=50,
		new_max_strike_of_interest=150)

	run_experiments(
		conditions = current_conditions,
		bs_vol = 0.4,
		option_time_to_expiry=2/12
)

main()
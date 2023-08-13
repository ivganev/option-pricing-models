from instrument_market_classes import MarketConditions
from typing import List
from matplotlib import pyplot as plt
from pricing_model_class import PricingModel


class ModelAndParams:
    def __init__(self, model_name: str, params: str) -> None:
        self.model_name = model_name
        self.params = params


def compare_pricing_models(
        models_list: List[ModelAndParams],
        time_to_expiry:float, 
        conditions:MarketConditions, 
        num_samples=100):
    
    common_min_strike = conditions.min_strike_of_interest
    common_max_strike = conditions.max_strike_of_interest
    fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12,5))

    for i, mod_params in enumerate(models_list):
        current_model = PricingModel(
            model_name=mod_params.model_name, 
            params=mod_params.params, 
            conditions= conditions
        )
        current_model_prices = current_model.pricing_plot(
            time_to_expiry=time_to_expiry,
            min_strike=common_min_strike,
            max_strike=common_max_strike,
            time_value_only=True,
            plot=False,
            num_samples=num_samples
        )
        
        if mod_params.model_name == "Binomial":
            fig_label = f"Binomial (n={mod_params.params['num_intervals']})"
        else:
            fig_label = mod_params.model_name

        ax1.plot(
            current_model_prices['strikes'],
            current_model_prices['call_prices'], label=fig_label)
        
        ax2.plot(
            current_model_prices['strikes'],
            current_model_prices['put_prices'], label=fig_label)
        
        plt.figtext(0.15+i/6, -0.1,
            f"MODEL #{i+1}:\n" +
            current_model.info_string(time_to_expiry=time_to_expiry),
            horizontalalignment ="left", verticalalignment ="top", 
            wrap = True, fontsize = 10)

    ax1.set_title("Time values for call options")
    ax1.set(xlabel="strike", ylabel ="price")
    ax1.legend()  
    ax2.set_title("Time values for put options")
    ax2.set(xlabel="strike", ylabel ="price")
    ax2.legend() 
    plt.show()
    return

def compare_distributions(
        models_list: List[ModelAndParams],
        time_to_expiry:float, 
        conditions:MarketConditions, 
        num_samples=100
    ):
    common_min_strike = conditions.min_strike_of_interest
    common_max_strike = conditions.max_strike_of_interest
    # fig, (ax1,ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(18,5))

    for i, mod_params in enumerate(models_list):
        current_model = PricingModel(
            model_name=mod_params.model_name, 
            params=mod_params.params, 
            conditions= conditions
        )
        current_model_pdf = current_model.probability_distribution_plot(
            time_to_expiry=time_to_expiry, 
            min_strike=common_min_strike, 
            max_strike=common_max_strike, 
            num_samples=num_samples,
            plot=False)
        
        if mod_params.model_name == "Binomial":
            fig_label = f"Binomial (n={mod_params.params['num_intervals']})"
        else:
            fig_label = mod_params.model_name

        plt.plot(
            current_model_pdf['strikes'],
            current_model_pdf['probs'], label=fig_label)
        
        plt.figtext(0.95+i/3, 0.5,
            f"MODEL #{i+1}:\n" +
            current_model.info_string(time_to_expiry=time_to_expiry),
            horizontalalignment ="left", verticalalignment ="top", 
            wrap = True, fontsize = 10)

    plt.title("Risk-neutral distributions")
    plt.xlabel("price of underlying")
    plt.legend()  
    plt.show()
    return
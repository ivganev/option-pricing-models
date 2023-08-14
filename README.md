# Option pricing models

We compare four different option pricing models:

* The Black-Scholes formula
* The quadratic volatility smile model
* The hyperbolic volatility smile model
* The binomial pricing model

## Pricing models

These four models are encapsulated in classes defined in the file `priding_model_menagerie.py`. The file `pricing_model_class.py` defines a unifying class for pricing models, with several methods:

* the `info_string` for displaying the parameters and market conditions in figures
* the `model_pricing_function` for computing option prices
* the `pricing_plot` method for visualizing the option prices, with the possibility of displaying only the time values
* the `butterly_price` method for computing the price of a butterfly
* the `probability_distribution_plot` method for visualizing the risk-neutral probability density function

Examples of the models appear in the script `pricing_examples.py`, and can be seen by running:

    python pricing_examples.py

## Comparisons 

The functions in the file `comparisons.py` allow one to compare any of these models by displaying the (time-value) pricing functions and the probability distributions. Examples appear in the script `comparison_examples.py`, and can be visualized by running:

    python comparison_examples.py

## Other

The remaining files, namely `helper_functions.py` and `instrument_market_classes.py` contain auxiliary classes and functions used by the other files. 

## References:

* Derman and Miller. *The Volatility Smile*. Wiely, 2016.
* Roman. *Introduction to the Mathematics of Finance*. Springer, 2nd ed., 2012.
* Shreve. *Stochastic Calculus for Finance II: Continuous-Time Model*. Springer, 2010.

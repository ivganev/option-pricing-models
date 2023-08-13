# The volatility smile and other option pricing models

We compare four different option pricing models:

* The Black-Scholes formula
* A quadratic volatility smile model
* A hyperbolic volatility smile model
* A binomial pricing model

These four models are encapsulated in classes defined in the file `priding_model_menagerie.py`. The file `pricing_model_class.py` defines a unifying class for pricing models, with methods for plotting the pricing function and risk-neutral probability distribution. 

The functions in the file `comparisons.py` allow one to compare any of these models by displaying the (time-value) pricing functions and the probability distributions. 

Examples of the models appear in the scripts `pricing_examples.py` and `comparison_examples.py`:

```> python3 pricing_examples.py```

```> python3 comparison_examples.py```

The remaining files, namely `helper_functions.py` and `instrument_market_classes.py` contain auxiliary classes and functions used by the other files. 

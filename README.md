# Option pricing models

## Introduction

We compare four different option pricing models. To describe them, consider an option (either call or put) with strike $K$ and expiry in $T$ years. let $S$ be the current price of the underlying and let $r$ be the annualized interest rate.  

### 1. The Black-Scholes formula

The Black-Scholes model assumes the underlying follows a geometric Brownian motion with volatility $\sigma$. The price of the call and put options are given by:
$$SN(d_+) - Ke^{-rT}N(d_-)$$ $$K e^{-rT}N(-d_-) - SN(-d_+),$$
respectively, where $d_\pm = \frac{\ln\left(\frac{S}{K}\right) + \left( r \pm \frac{\sigma^2}{2}\right)\sqrt{T}  }{\sigma \sqrt{T}}$.


### 2. The quadratic volatility smile model

The volatility smile models are variations of the Black-Scholes model where the volatility is assumed to be a function of the stirke price. Specifically, let $\sigma_\text{atm}$ be the at-the-money volatility. Then the quadratic volatilty smile assumes that the volatility is given by
$$\sigma(K) = c_2 d^2 + c_1 d + c_0$$
for some constants $c_i$, where $d = \frac{\ln\left( \frac{S}{K}\right) + rT}{\sigma_\text{atm}\sqrt{T}}$. Since $d=0$ for an at-the-money strike, we have that $c_0 = \sigma_\text{atm}$. Moreover, $c_1$ is the *skew*, i.e., the slope of the volatility smile at $d=0$. Finally, $c_2$ is the *curvature*, i.e., the second derivative at $d=0$. Option prices are obtained via the Black-Scholes formula, but with plugging in $\sigma(K)$ rather than a constant $\sigma$. 

### 3. The hyperbolic volatility smile model

This model is similar to the above, but with volatility smile given by:
$$\sigma(K) = \sqrt{c_2 d^2 + c_1 d + c_0}$$
for some constants $c_i$, where again $d = \frac{\ln\left( \frac{S}{K}\right) + rT}{\sigma_\text{atm}\sqrt{T}}$. Note that, as a function of $d$, this volatility smile is asymptotically linear with slope $\pm c_2$ as $d \to \pm \infty$. 

In order to obtain different behavior for $d \to \infty$ and $d \to -\infty$, we  consider a slightly more general version of this model. Namely, instead of a single parameter $c_2$, we have parameters $c_2^+$ and $c_2^-$. These define different hyperbolas:
$$\sigma_+(K) = \sqrt{c_2^+ d^2 + c_1 d + c_0} \qquad \sigma_-(K) = \sqrt{c_2^- d^2 + c_1 d + c_0}$$
We glue these together:
$$\sigma(K) = \lambda(K) \sigma_+(K) + (1-\lambda(K))  \sigma_-(K)$$
where $\lambda$ is a smooth glueing function such that, once we change variables to $d$, we have $\lambda(d) = 0$ for $d < -3$ and $\lambda(d) =1$ for $d >3$. The resulting function $\sigma$ is asymptotically linear with slope $-c_2^-$ as $d \to -\infty$ and slope $c_2^+$ as $d \to \infty$. 

### 4. The binomial pricing model

In contrast to the above, the binomial model is a discrete pricing model. Suppose we divide the time to expiry $T$ into $N$ time intervals, each of size $t = T/N$. Suppose further that for each interval, the underlying either goes up by a factor of $u$ or down by a factor of $d$. The risk-free (or martingale) up-tick probability is given by 
$$\pi = \frac{e^{rt} - d}{u-d}.$$
The call and put option prices are given by:
$$e^{-rT} \sum_{n=0}^N { N \choose n} \left( S u^n d^{N-n} - K\right)^+ \pi^n (1-\pi)^{N-n}$$ 
$$e^{-rT} \sum_{n=0}^N { N \choose n} \left( K - S u^n d^{N-n} \right)^+ \pi^n (1-\pi)^{N-n},$$
respectively, where $x^+ = \max(0,x)$. This model limits to the Black-Scholes model with volatility $\sigma$ when the up-tick and down-tick factors are $e^{\pm \sigma \sqrt{T/N}}$, and taking $N\to \infty$.

## Pricing models

Each of the four described above is encapsulated in separate class defined in the file `priding_model_menagerie.py`. The file `pricing_model_class.py` defines a unifying class for pricing models, with several methods:

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

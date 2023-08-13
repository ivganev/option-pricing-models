class OptionClass:
    def __init__(self, strike: float, time_to_expiry: float, option_type: str) -> None:
        assert option_type == "call" or option_type == "put", "Option type must be 'call' or 'put'"
        self.strike = strike
        self.time_to_expiry = time_to_expiry
        self.option_type = option_type

    def value_at_expiration(self, spot_at_expiry: float) -> float:
        if self.option_type == "call":
            return max(0, spot_at_expiry - self.strike)
        else:
            return max(0, self.strike - spot_at_expiry)



class MarketConditions:
    def __init__(self, spot, interest_rate) -> None:
        self.spot = spot
        self.interest_rate = interest_rate
        self.min_strike_of_interest=0.5*self.spot
        self.max_strike_of_interest=2*self.spot

    def set_min_max_strikes_of_interest(self, new_min_strike_of_interest, new_max_strike_of_interest):
        self.min_strike_of_interest = new_min_strike_of_interest
        self.max_strike_of_interest = new_max_strike_of_interest


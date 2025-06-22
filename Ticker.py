class Ticker:

    def __init__(self, name, buy_price, gain=None):
        self.name = name
        self.buy_price = buy_price
        self.gain = gain

    def __str__(self):
        return f"Ticker({self.name}, Buy: {self.buy_price}, Gain: {self.gain})"
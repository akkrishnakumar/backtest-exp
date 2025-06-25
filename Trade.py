class Trade:

    def __init__(self, name, buy_price, sell_price, qty):
        self.name = name
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.qty = qty
    
    def __str__(self):
        return f"Trade({self.name}, Buy Price: {self.buy_price}, Sell Price: {self.sell_price}, Qty: {self.qty})"
    
    def __repr__(self):
        return str(self)
        
    # Create method to calculate various metrics of the trade.
    def pnl_percent(self):
        return ((self.sell_price - self.buy_price) / self.buy_price) * 100
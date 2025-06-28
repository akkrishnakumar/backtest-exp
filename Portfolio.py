from CLI import println
from Holding import Holding

class Portfolio:
    
    holdings = {}
    tradebook = []
    
    def __init__(self, initialBuys):
        self.initialBuys = initialBuys
        println("Initializing Portfolio...")
        
        println("- Making first purchase")
        for initialBuy in initialBuys:
            self.holdings[initialBuy.name] = Holding(initialBuy)

        println("Portfolio Initialized !")
    
    def holding_names(self):
        return set(self.holdings.keys())
    
    def update_holdings(self, tickers):
        for ticker in tickers:
            if ticker.name not in self.holdings:
                self.holdings[ticker.name] = Holding(ticker)
        
    # positions_to_close is only a set of strings    
    def close_positions(self, positions_to_close, sell_date):
        for position in positions_to_close:
            if position in self.holdings.keys():
                popped = self.holdings.pop(position)
                trade = popped.sell(sell_date)
                self.tradebook.append(trade)
        
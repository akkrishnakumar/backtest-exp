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
        return self.holdings.keys()
    
    def rebalance(self, tickers, rebalance_date):
        # buy new entries
        for ticker in tickers:
            if ticker.name not in self.holdings.keys():
                self.holdings[ticker.name] = Holding(ticker)
            self.buy(ticker)
            
        # sell entries which are not present in the new updated portfolio
        ticker_names_to_sell = set(self.holding_names()).difference([t.name for t in tickers])
        for t in ticker_names_to_sell:
            self.sell(t, rebalance_date)
            
        println(f"New holdings: {[t.name for t in tickers]}")
        println(f"Sold holdings: {list(ticker_names_to_sell)}")
        
    def buy(self, ticker):
        if ticker.name not in self.holding_names():
            self.holdings[ticker.name] = Holding(ticker)
    
    def sell(self, ticker, sell_date):
        popped_holding = self.holdings.pop(ticker)
        self.tradebook.append(popped_holding.sell(sell_date))
        
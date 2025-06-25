class Backtest:
    
    def __init__(self, target_date, tickers):
        self.target_date = target_date
        self.tickers = tickers
    
    def __str__(self):
        return f"Backtest(Target Date: {self.target_date}, Tickers: {self.tickers})"
    
    def __repr__(self):
        return str(self)
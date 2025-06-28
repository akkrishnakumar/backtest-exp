import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta
from Trade import Trade
from DateUtil import nearest_friday_of, next_day_of
from CLI import println, br

class Holding:
    
    def __init__(self, ticker, qty = 1):
        self.name = ticker.name
        self.buy_price = ticker.buy_price
        self.qty = qty
    
    def sell(self, sell_date):
        return Trade(self.name, self.buy_price, 0, 1)
    
    def last_close_price_of(self, date):
        try:
            # TODO: move this logic into a generic method in YF.py
            adj_date = nearest_friday_of(date)
            data = yf.download(self.name, adj_date , next_day_of(adj_date), auto_adjust=True)
            if not data.empty:
                return data['Close'][self.name].iloc[0]
            else:
                println(f"Last close price of {self.name} is not available for date {adj_date}")
                return 0
        except Exception as e:
            print(f"An error occurred while fetching last close price: {e}")
            return 0
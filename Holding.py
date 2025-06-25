import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta
from Trade import Trade

class Holding:
    
    def __init__(self, ticker, qty = 1):
        self.name = ticker.name
        self.buy_price = ticker.buy_price
        self.qty = qty
    
    def sell(self, sell_date):
        return Trade(self.name, self.buy_price, self.last_close_price_of(sell_date), 1)
    
    def last_close_price_of(self, date):
        try:
            
            # TODO: move this logic into a generic method in YF.py
            
            # If it is a Saturday, then range should be till Monday so that data will be correctly fetched
            data = yf.download(self.name, date , date + timedelta(days=2), auto_adjust=True)

            if not data.empty:
                return data['Close'][self.name].iloc[0]
            else:
                print(f"Last close price of {self.name} is not available for date {date}")
                return 0
        except Exception as e:
            print(f"An error occurred while fetching last close price: {e}")
            return 0
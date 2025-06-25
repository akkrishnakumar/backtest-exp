import yfinance as yf
import pandas as pd

class Holding:
    
    def _init_(self, ticker):
        self.name = ticker.name
        self.buy_price = ticker.buy_price
    
    def last_close_price_of(self, date):
        try:
            
            data = yf.download(self.name, date, next_date)
        
            if not data.empty:
                today_data = data.iloc[-1]
                return today_data['Close']
            else:
                print(f"Last close price of {self.name} is not available for date {date}")
                return pd.Series()
        except Exception as e:
            print(f"An error occurred while fetching last close price: {e}")
            return pd.Series()
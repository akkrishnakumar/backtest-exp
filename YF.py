import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from Ticker import Ticker, empty_ticker_from

def returns_of_12_minus_1_months(tickers, target_date):
        
    end_date = (target_date.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59) # last day of the previous month
    start_date = (end_date - relativedelta(months=12)).replace(day=1) # Start of the 12th month ago
    
    print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Convert with yf compatible tickers
    yf_tickers = [f"{ticker}.NS" for ticker in tickers]
    
    results = []
    
    try:
        data = yf.download(yf_tickers, start=start_date, end=end_date, auto_adjust=True, progress=False)
        
        if data.empty:
            print("No data retrieved for any of the tickers in the specified period.")
            for ticker in yf_tickers:
                results.append(empty_ticker_from(ticker))
            return results
        
        # Get returns of past 12 month excluding the most recent month
        for ticker in yf_tickers:
            
            if('Close', ticker) in data.columns:
                ticker_data = data['Close'][ticker].dropna() # Drop NaNs if any
            
                if ticker_data.empty or len(ticker_data) < 2: # Need at least 2 points for a return
                    print(f"  Warning: Insufficient data for {ticker} to calculate return. Skipping.")
                    results.append(empty_ticker_from(ticker))
                    continue
            
                beginning_price = ticker_data.iloc[0]
                ending_price = ticker_data.iloc[-1]
            
                price_return = int(((ending_price / beginning_price) - 1) * 100) # convert to simple int to readability
                results.append(Ticker(ticker, beginning_price, price_return))
        
            else:
                print(f"  Warning: No 'Close' data found for {ticker} in the batch download. Skipping.")
                results.append(empty_ticker_from(ticker))
        
    except Exception as e:
        print(f"An error occurred during batch download or processing: {e}")
        for ticker in tickers:
            results.append(empty_ticker_from(ticker))
    
    print("\n=======\n") 
    return results
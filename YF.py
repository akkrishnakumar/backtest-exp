import os
import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from CLI import println, br
from Ticker import Ticker, empty_ticker_from
from Backtest import Backtest

def returns_of_12_minus_1_months(tickers, curr_date):
        
    end_date = (curr_date.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59) # last day of the previous month
    start_date = (end_date - relativedelta(months=12)).replace(day=1) # Start of the 12th month ago
    
    # Convert with yf compatible tickers
    yf_tickers = [f"{ticker}.NS" for ticker in tickers]
    
    print("Searching from data cache...")
    data = fetch_from_cache(curr_date)
    
    if data is not None:
        print("Reading data from cache...")
        return Backtest(curr_date, extract_returns(yf_tickers, data, curr_date, end_date))
    
    else:
        try:
            print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {curr_date.strftime('%Y-%m-%d')}")

            # Download data up till current date
            downloaded_data = yf.download(yf_tickers, start=start_date, end=curr_date + timedelta(days=2), auto_adjust=True, progress=False)
            store_data_in_cache(curr_date, downloaded_data)
            return Backtest(curr_date, extract_returns(yf_tickers, downloaded_data, curr_date, end_date))
        
        except Exception as e:
            print(f"Error while trying to fetch data from YF: {e}")
            return []

def extract_returns(yf_tickers, data, curr_date, end_date):
    results = []
    try:
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
                ending_price = ticker_data.loc[end_date.strftime('%Y-%m-%d')]
                current_price = ticker_data.loc[curr_date.strftime('%Y-%m-%d')]
                
                price_return = int(((ending_price / beginning_price) - 1) * 100) # convert to simple int to readability
                
                results.append(Ticker(ticker, current_price, price_return))
        
            else:
                print(f"  Warning: No 'Close' data found for {ticker} in the batch download. Skipping.")
                results.append(empty_ticker_from(ticker))
                
    except Exception as e:
        print(f"An error occurred during batch download or processing: {e}")
        for ticker in yf_tickers:
            results.append(empty_ticker_from(ticker))
            
    print("\n=======\n") 
    return results   

def fetch_from_cache(target_date):
    data_cache = f".cache/{target_date.strftime('%Y-%m-%d')}.csv"
    if os.path.exists(data_cache):
        return pd.read_parquet(data_cache)
    else:
        return None

def store_data_in_cache(target_date, data):
    data_cache = f".cache/{target_date.strftime('%Y-%m-%d')}.csv"
    os.makedirs(".cache", exist_ok=True)
    data.to_parquet(data_cache, index=True)
import os
import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from CLI import println, debug
from Ticker import Ticker, empty_ticker_from
from Backtest import Backtest
from DateUtil import to_string, nearest_friday_of, next_day_of

def returns_of_12_minus_1_months(tickers, curr_date):
        
    end_date = nearest_friday_of((curr_date.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59)) # last day of the previous month
    start_date = (end_date - relativedelta(months=12)).replace(day=1) # Start of the 12th month ago
    
    # Convert with yf compatible tickers
    yf_tickers = [f"{ticker}.NS" for ticker in tickers]
     
    data = fetch_from_cache(curr_date)
    if data is not None:
        print("Reading data from cache...")
        return Backtest(curr_date, extract_returns(yf_tickers, data, curr_date, end_date))
    
    else:
        try:
            print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {curr_date.strftime('%Y-%m-%d')}")

            # Download data up till current date
            downloaded_data = yf.download(yf_tickers, start=start_date, end=curr_date, auto_adjust=True, progress=False)
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
                    debug(f"  Warning: Insufficient data for {ticker} to calculate return. Skipping.")
                    results.append(empty_ticker_from(ticker))
                    continue
                    
                # br()
                # println(ticker_data)
                beginning_price = ticker_data.iloc[0]
                # ending_price = ticker_data.loc[to_string(end_date)]
                # current_price = ticker_data.loc[to_string(curr_date)]
                ending_price = safe_read(ticker, ticker_data, end_date)
                current_price = safe_read(ticker, ticker_data, curr_date)
                
                price_return = int(((ending_price / beginning_price) - 1) * 100) # convert to simple int to readability
                
                results.append(Ticker(ticker, current_price, price_return))
        
            else:
                print(f"  Warning: No 'Close' data found for {ticker} in the batch download. Skipping.")
                results.append(empty_ticker_from(ticker))
                
    except Exception as e:
        print(f"An error occurred during batch download or processing: {e}")
        for ticker in yf_tickers:
            results.append(empty_ticker_from(ticker))
    
    
    return results   

def fetch_from_cache(target_date):
    data_cache = f".cache/{target_date.strftime('%Y-%m-%d')}.parquet"
    if os.path.exists(data_cache):
        return pd.read_parquet(data_cache)
    else:
        return None

def store_data_in_cache(target_date, data):
    data_cache = f".cache/{target_date.strftime('%Y-%m-%d')}.parquet"
    os.makedirs(".cache", exist_ok=True)
    data.to_parquet(data_cache, index=True)
    
# TODO: Improve logic    
def safe_read(ticker_name, ticker_data, date, retry=True):
    try:
        return ticker_data.loc[to_string(date)]
    except Exception as e: 
        debug(f"Error while trying to fetch data for {ticker_name} for date: {to_string(date)}")
        if retry == True:
            next_day = next_day_of(date)
            debug(f"Taking holidays into consideration, picking next date: {to_string(next_day)}")        
            return safe_read(ticker_name, ticker_data, next_day, False)
        else:
            debug(ticker_data)    
            return 0
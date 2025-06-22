import csv
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from YF import returns_of_12_minus_1_months

def read_nse_index(file_path):
    values = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None) # Skip the header row (first row)
            for row in reader:
                values.append(row[2])
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return values

def rank(ticker_returns):
    flat_data_for_df = []
    for row in ticker_returns:
        for ticker, gain in row.items():
            flat_data_for_df.append({'Ticker': ticker, 'Gain': gain})
    
    df = pd.DataFrame(flat_data_for_df)
    df_filtered = df.dropna(subset=['Gain'])
    df_sorted = df_filtered.sort_values(by='Gain', ascending=False)
    return df_sorted

def past_month_dates(num_of_months: 12):
    dates_list = []
    current_date = datetime.now()
    for i in range(num_of_months + 1):
        dates_list.append(current_date)
        current_date -= relativedelta(months=1)
    return sorted(dates_list)

if __name__ == "__main__":
    
    # Get stocks from NSE 500 - DONE!
    download_folder = "/Users/akhil/Downloads/"
    # nifty_500 = f"{download_folder}ind_nifty500list.csv"
    nifty_next_50 = f"{download_folder}ind_niftynext50list.csv"
    tickers = read_nse_index(nifty_next_50)
    
    # Backtest
    
    # Get dates of past 12 months
    lookback_dates = past_month_dates(12)
    
    # For each date in the past month, create a list of stocks ranked by momentum score of past 12-1 months
    backtest = {}
    for (i, target_date) in enumerate(lookback_dates):

        # Function to fetch 12 months data for each stock in the list and rank them according to returns
        returns = returns_of_12_minus_1_months(tickers, target_date)
    
        # Rank the stocks by momentum score
        ranked = rank(returns)
        
        # Store the top 50 stocks into the back test
        backtest[i] = ranked.head(10)
    
    print("\n=========")
    print("List of stocks per month ranked by momentum score. (Top 50)")
    print(backtest)
    
    # Store state of each monthly rebalance in a list - Portfolio(List(stocks, weights, price, qty) etc)
    # Iterate over portfolio and create PnL(current returns, Avg win, Avg loss, Biggest Drawdown, sharpe ration etc)
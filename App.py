import csv
import pandas as pd

from YF import returns_of_12_minus_1_months
from Strategy import Strategy_M_12_minus_1 as Strategy1
from CLI import println, br
from DateUtil import to_string, nearest_friday_of, past_month_dates, date_from

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

if __name__ == "__main__":
    
    # Get stocks from NSE 500 - DONE!
    download_folder = "/Users/akhil/Downloads/"
    # nifty_500 = f"{download_folder}ind_nifty500list.csv"
    # nifty_next_50 = f"{download_folder}ind_niftynext50list.csv"
    nifty_50 = f"{download_folder}ind_nifty50list.csv"
    tickers = read_nse_index(nifty_50)
    
    # Backtest
    
    # Get dates of past 12 months
    testing_date = date_from("2025-06-28")
    lookback_dates = past_month_dates(testing_date, 12)  

    # For each date in the past month, create a list of stocks ranked by momentum score of past 12-1 months
    backtests = []
    for (i, target_date) in enumerate(lookback_dates[:1]):
        # Function to fetch 12 months data for each stock in the list and rank them according to returns
        backtests.append(returns_of_12_minus_1_months(tickers, target_date))
    br("=")
    print("Back testing Strategy.... ")
    Strategy1(backtests).run()
    print("\nDone! ")
    br("=")
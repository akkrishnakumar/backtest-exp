import csv
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from YF import returns_of_12_minus_1_months
from Strategy import Strategy_M_12_minus_1 as Strategy1
from CLI import println, br

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

def past_month_dates(num_of_months: 12):
    dates_list = []
    current_date = datetime.now()
    for i in range(num_of_months + 1):
        selected_date = current_date.date()
        
        # Moving back to Friday if the date falls on a weekend
        if selected_date.weekday() == 5: # Saturday
            selected_date = selected_date - timedelta(days=1)
        elif selected_date.weekday() == 6: # Sunday
            selected_date = selected_date - timedelta(days=2)
            
        calc_date = datetime.combine(selected_date, current_date.time())
        dates_list.append(calc_date)
        
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

    # # TODO: Convert Backtest into a class. Then it is easy to add members to it
    # # For each date in the past month, create a list of stocks ranked by momentum score of past 12-1 months
    # backtests = []
    # for (i, target_date) in enumerate(lookback_dates):
    #     # Function to fetch 12 months data for each stock in the list and rank them according to returns
    #     backtests.append(returns_of_12_minus_1_months(tickers, target_date))
    
    # print("\n=========")
    # print("Back testing Strategy.... ")
    # Strategy1(backtests).run()
    # print("\nDone! ")
    # print("\n=========")
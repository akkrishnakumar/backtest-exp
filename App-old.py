import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# --- Configuration ---
# List of prominent NSE stocks for the portfolio universe
# You can expand this list or load it from a CSV for a larger universe
NSE_SYMBOLS = [
    "RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "BHARTIARTL.NS", "LICI.NS", "SBIN.NS",
    "KOTAKBANK.NS", "BAJFINANCE.NS", "ASIANPAINT.NS", "TITAN.NS", "MARUTI.NS",
    "LT.NS", "AXISBANK.NS", "NESTLEIND.NS", "ULTRACEMCO.NS", "WIPRO.NS"
]

# Strategy Parameters
TOP_N_STOCKS = 10           # Number of top momentum stocks to hold in the portfolio
LOOKBACK_MONTHS = 12        # Months for momentum calculation (12-month momentum)
HOLDING_MONTHS = 1          # Months for holding period (monthly rebalancing)
COMMISSION_PER_TRADE = 0.002 # 0.2% commission per trade (buy and sell combined)
INITIAL_CAPITAL = 1000000   # Rs. 1,000,000

# --- Data Collection Function ---
def fetch_data(symbols, start_date, end_date):
    """
    Fetches historical adjusted close price data for a list of symbols.
    Args:
        symbols (list): List of ticker symbols (e.g., ["RELIANCE.NS", "TCS.NS"])
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.
    Returns:
        pd.DataFrame: DataFrame with Adjusted Close prices for all symbols.
    """
    print(f"Fetching data for {len(symbols)} symbols from {start_date} to {end_date}...")
    data = yf.download(symbols, start=start_date, end=end_date, auto_adjust=True)['Close']
    print("Data fetch complete.")
    # print(data)
    return data

# --- Momentum Strategy Backtest Function ---
def backtest_momentum_portfolio(data, top_n, lookback_months, holding_months, commission, initial_capital):
    """
    Performs a multi-stock momentum portfolio backtest.

    Args:
        data (pd.DataFrame): DataFrame of Adjusted Close prices for all symbols.
        top_n (int): Number of top momentum stocks to select.
        lookback_months (int): Months for momentum calculation.
        holding_months (int): Months for holding period (rebalancing frequency).
        commission (float): Commission percentage per trade (e.g., 0.002 for 0.2%).
        initial_capital (float): Starting capital for the portfolio.

    Returns:
        pd.DataFrame: DataFrame containing portfolio equity, daily returns, etc.
    """
    # Ensure data is sorted by date and resampled to month-end for rebalancing points
    data = data.ffill().bfill() # Handle potential NaNs by forward/backward filling
    monthly_data = data.resample('ME').last() # Get month-end prices for rebalancing
    print(monthly_data)

    portfolio_returns = pd.Series(dtype=float)
    portfolio_value = pd.Series(dtype=float)
    current_portfolio_holdings = [] # Stores symbols currently held

    # Iterate through each rebalancing point (month-end)
    for i in range(len(monthly_data)):
        if i < lookback_months:
            continue # Need enough history for lookback period

        rebalance_date = monthly_data.index[i]
        portfolio_start_date_for_period = monthly_data.index[i] + pd.Timedelta(days=1) # Day after rebalance
        if i + holding_months >= len(monthly_data):
            portfolio_end_date_for_period = data.index[-1] # Use last available data if end of backtest
        else:
            portfolio_end_date_for_period = monthly_data.index[i + holding_months]

        # Define lookback start and end for momentum calculation
        momentum_start_date = monthly_data.index[i - lookback_months]
        momentum_end_date = monthly_data.index[i - 1] # Exclude the most recent month

        print(f"Rebalancing on {rebalance_date.strftime('%Y-%m-%d')}")

        # Calculate momentum for all stocks in the universe
        # Ensure we have data for the full lookback period for each stock
        valid_momentum_stocks = []
        momentum_values = {}

        for symbol in data.columns:
            # Get data for the lookback period
            lookback_prices = data[symbol][(data.index >= momentum_start_date) & (data.index <= momentum_end_date)]

            if len(lookback_prices) >= 0.8 * (lookback_months * 20): # At least 80% of expected bars
                # Calculate momentum as total return over the period
                start_price = lookback_prices.iloc[0]
                end_price = lookback_prices.iloc[-1]
                if start_price > 0: # Avoid division by zero
                    momentum = (end_price - start_price) / start_price
                    momentum_values[symbol] = momentum

        # Sort stocks by momentum and select top N
        sorted_momentum_stocks = sorted(momentum_values.items(), key=lambda item: item[1], reverse=True)
        new_portfolio_symbols = [s[0] for s in sorted_momentum_stocks[:top_n]]

        # Calculate turnover and apply commissions for rebalancing
        # This is a simplified commission model assuming full portfolio rebalancing cost
        num_new_trades = len(set(new_portfolio_symbols) - set(current_portfolio_holdings))
        num_old_trades = len(set(current_portfolio_holdings) - set(new_portfolio_symbols))
        total_transactions = num_new_trades + num_old_trades # Simplified, better to track individual buys/sells
        commission_cost_factor = (1 - commission) ** total_transactions # Very rough, assumes each stock buy/sell is a new transaction affecting entire capital

        # Get daily returns for the new portfolio during the holding period
        if not new_portfolio_symbols:
            daily_portfolio_period_returns = pd.Series(0.0, index=pd.to_datetime([])) # No stocks to hold
        else:
            period_data = data[new_portfolio_symbols][(data.index > rebalance_date) & (data.index <= portfolio_end_date_for_period)]
            if not period_data.empty:
                # Calculate daily returns for each stock
                daily_stock_returns = period_data.pct_change().dropna()
                # Equal weighting: sum daily returns and divide by number of stocks
                # Ensure no division by zero if daily_stock_returns is empty
                if not daily_stock_returns.empty:
                    daily_portfolio_period_returns = daily_stock_returns.mean(axis=1) # Mean of daily returns for selected stocks
                else:
                    daily_portfolio_period_returns = pd.Series(0.0, index=period_data.index)
            else:
                daily_portfolio_period_returns = pd.Series(0.0, index=pd.to_datetime([]))

        # Apply the commission cost. This is a simplification; ideally, commission is applied per trade.
        if not daily_portfolio_period_returns.empty and total_transactions > 0:
            daily_portfolio_period_returns.iloc[0] = daily_portfolio_period_returns.iloc[0] * commission_cost_factor

        portfolio_returns = pd.concat([portfolio_returns, daily_portfolio_period_returns])
        current_portfolio_holdings = new_portfolio_symbols # Update holdings for next period

    # Calculate cumulative returns and portfolio value
    portfolio_returns = portfolio_returns.loc[portfolio_returns.index.min():data.index.max()].fillna(0) # Ensure no gaps or future dates
    portfolio_cumulative_returns = (1 + portfolio_returns).cumprod()
    portfolio_value = initial_capital * portfolio_cumulative_returns

    # Add initial capital point to value series for plotting
    first_date = portfolio_returns.index.min()
    portfolio_value.loc[first_date - timedelta(days=1)] = initial_capital
    portfolio_value = portfolio_value.sort_index()

    # Calculate benchmark (Nifty 50) for comparison
    nifty_data = yf.download("^NSEI", start=data.index.min(), end=data.index.max(), auto_adjust=True)['Adj Close']
    nifty_returns = nifty_data.pct_change().dropna()
    nifty_cumulative_returns = (1 + nifty_returns).cumprod()
    nifty_value = initial_capital * nifty_cumulative_returns

    # Add initial capital point to Nifty value series
    nifty_value.loc[nifty_returns.index.min() - timedelta(days=1)] = initial_capital
    nifty_value = nifty_value.sort_index()


    # Combine into a single DataFrame for analysis
    backtest_results = pd.DataFrame({
        'Portfolio Value': portfolio_value,
        'Nifty Value': nifty_value
    }).ffill().bfill().dropna()

    return backtest_results.iloc[1:] # Remove the initial_capital placeholder row

# --- Performance Metrics Calculation ---
def calculate_metrics(returns_series, annual_risk_free_rate=0.04):
    """
    Calculates key performance metrics for a series of daily returns.
    Args:
        returns_series (pd.Series): Daily returns of the portfolio.
        annual_risk_free_rate (float): Annual risk-free rate (e.g., 0.04 for 4%).
    Returns:
        dict: Dictionary of performance metrics.
    """
    if returns_series.empty:
        return {
            "Total Return (%)": 0,
            "CAGR (%)": 0,
            "Max Drawdown (%)": 0,
            "Sharpe Ratio": 0,
            "Annual Volatility (%)": 0
        }

    total_return = (returns_series + 1).prod() - 1
    num_years = (returns_series.index[-1] - returns_series.index[0]).days / 365.25
    cagr = ((1 + total_return)**(1/num_years) - 1) if num_years > 0 else 0

    # Drawdown calculation
    cumulative_returns = (returns_series + 1).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns / peak) - 1
    max_drawdown = drawdown.min()

    # Sharpe Ratio
    daily_risk_free_rate = (1 + annual_risk_free_rate)**(1/252) - 1 # Assuming 252 trading days
    excess_returns = returns_series - daily_risk_free_rate
    annual_volatility = returns_series.std() * np.sqrt(252)
    sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252) if excess_returns.std() > 0 else 0

    return {
        "Total Return (%)": f"{total_return * 100:.2f}%",
        "CAGR (%)": f"{cagr * 100:.2f}%",
        "Max Drawdown (%)": f"{max_drawdown * 100:.2f}%",
        "Annual Volatility (%)": f"{annual_volatility * 100:.2f}%",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}"
    }

# --- Plotting Function ---
def plot_results(backtest_df, title="Portfolio Backtest"):
    """
    Plots the portfolio and benchmark equity curves.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(backtest_df.index, backtest_df['Portfolio Value'], label='Momentum Portfolio', color='blue')
    plt.plot(backtest_df.index, backtest_df['Nifty Value'], label='Nifty 50 Benchmark', color='orange', linestyle='--')
    plt.title(title, fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Value (INR)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    # --- Backtest Periods ---
    # 1-Year Period
    end_date_1yr = datetime.now()
    start_date_1yr = end_date_1yr - timedelta(days=365) # Approx 1 year

    print("\n--- Running Backtest for 1 Year Period ---")
    all_data_1yr = fetch_data(NSE_SYMBOLS, start_date_1yr.strftime('%Y-%m-%d'), end_date_1yr.strftime('%Y-%m-%d'))
    if all_data_1yr.empty:
        print("Could not fetch data for 1-year period. Skipping this backtest.")
    else:
        # print(all_data_1yr.columns)
        results_1yr = backtest_momentum_portfolio(all_data_1yr, TOP_N_STOCKS, LOOKBACK_MONTHS, HOLDING_MONTHS, COMMISSION_PER_TRADE, INITIAL_CAPITAL)
        # if not results_1yr.empty:
        #     print("\n--- 1-Year Backtest Performance ---")
        #     portfolio_returns_1yr = results_1yr['Portfolio Value'].pct_change().dropna()
        #     nifty_returns_1yr = results_1yr['Nifty Value'].pct_change().dropna()

        #     print("\nPortfolio Metrics:")
        #     for k, v in calculate_metrics(portfolio_returns_1yr).items():
        #         print(f"{k}: {v}")
        #     print("\nNifty 50 Benchmark Metrics:")
        #     for k, v in calculate_metrics(nifty_returns_1yr).items():
        #         print(f"{k}: {v}")

        #     plot_results(results_1yr, title="1-Year Momentum Portfolio vs. Nifty 50")
        # else:
        #     print("No valid results for 1-year backtest.")


    # 3-Year Period
    # end_date_3yr = datetime.now()
    # start_date_3yr = end_date_3yr - timedelta(days=3 * 365) # Approx 3 years

    # print("\n--- Running Backtest for 3 Year Period ---")
    # all_data_3yr = fetch_data(NSE_SYMBOLS, start_date_3yr.strftime('%Y-%m-%d'), end_date_3yr.strftime('%Y-%m-%d'))
    # if all_data_3yr.empty:
    #     print("Could not fetch data for 3-year period. Skipping this backtest.")
    # else:
    #     results_3yr = backtest_momentum_portfolio(all_data_3yr, TOP_N_STOCKS, LOOKBACK_MONTHS, HOLDING_MONTHS, COMMISSION_PER_TRADE, INITIAL_CAPITAL)
    #     if not results_3yr.empty:
    #         print("\n--- 3-Year Backtest Performance ---")
    #         portfolio_returns_3yr = results_3yr['Portfolio Value'].pct_change().dropna()
    #         nifty_returns_3yr = results_3yr['Nifty Value'].pct_change().dropna()

    #         print("\nPortfolio Metrics:")
    #         for k, v in calculate_metrics(portfolio_returns_3yr).items():
    #             print(f"{k}: {v}")
    #         print("\nNifty 50 Benchmark Metrics:")
    #         for k, v in calculate_metrics(nifty_returns_3yr).items():
    #             print(f"{k}: {v}")

    #         plot_results(results_3yr, title="3-Year Momentum Portfolio vs. Nifty 50")
    #     else:
    #         print("No valid results for 3-year backtest.")

#RP2gemini
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_data(tickers, start_date, end_date):
    """Fetches adjusted closing prices for given tickers."""
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)
        
        # Handle potential MultiIndex columns if fetching multiple tickers
        if isinstance(data.columns, pd.MultiIndex):
            adj_close = data['Adj Close']
        else: # Single ticker case
             adj_close = data[['Adj Close']] # Keep it as DataFrame
             
        # Check for missing data
        if adj_close.isnull().values.any():
            print("Warning: Missing data detected. Filling forward.")
            adj_close = adj_close.ffill()
        
        # Drop any remaining NaNs (e.g., at the start)
        adj_close = adj_close.dropna()
            
        if adj_close.empty:
             raise ValueError("No data fetched. Check tickers and date range.")
             
        return adj_close
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def calculate_daily_returns(price_data):
    """Calculates daily percentage returns."""
    return price_data.pct_change().dropna()

def calculate_rolling_volatility(daily_returns, window):
    """Calculates rolling annualized volatility."""
    # Calculate rolling standard deviation
    rolling_std = daily_returns.rolling(window=window).std()
    # Annualize it (assuming 252 trading days)
    annualized_volatility = rolling_std * (252 ** 0.5)
    return annualized_volatility.dropna()

def get_risk_parity_weights(volatility_series):
    """Calculates inverse volatility weights for a given date (row of volatilities)."""
    # Handle potential zero volatility by adding a small epsilon or setting weight to 0
    inv_volatility = 1.0 / volatility_series.replace(0, np.nan) # Avoid division by zero
    inv_volatility = inv_volatility.fillna(0) # Assets with zero vol get zero weight
    
    # Check if all inverse volatilities are zero (e.g., flat price period)
    if inv_volatility.sum() == 0:
        # Fallback to equal weight if all volatilities are zero/NaN
        num_assets = len(volatility_series)
        return pd.Series(1.0 / num_assets, index=volatility_series.index) if num_assets > 0 else pd.Series(dtype=float)
        
    weights = inv_volatility / inv_volatility.sum()
    return weights

def backtest_strategy(daily_returns, lookback_window=60, rebalance_frequency='M'):
    """
    Simulates Risk Parity and Equal-Weighted strategies with periodic rebalancing.

    Args:
        daily_returns (pd.DataFrame): DataFrame of daily returns for assets.
        lookback_window (int): Rolling window period for volatility calculation (in days).
        rebalance_frequency (str): Pandas offset string for rebalancing frequency ('M', 'Q', 'W').

    Returns:
        tuple: (risk_parity_portfolio_returns, equal_weighted_portfolio_returns, last_rp_weights)
    """
    num_assets = daily_returns.shape[1]
    tickers = daily_returns.columns

    # Determine rebalance dates (end of the period specified by frequency)
    rebalance_dates = daily_returns.resample(rebalance_frequency).last().index
    
    # Align rebalance dates with available data index
    rebalance_dates = rebalance_dates.intersection(daily_returns.index)
    if rebalance_dates.empty:
        print("Warning: No rebalance dates found within the data range.")
        # Return empty series or handle appropriately
        return pd.Series(dtype=float), pd.Series(dtype=float), pd.Series(dtype=float)

    # Calculate rolling volatility
    rolling_vol = calculate_rolling_volatility(daily_returns, lookback_window)

    # Ensure rolling_vol starts early enough for the first rebalance
    first_rebalance_date = rebalance_dates[0]
    required_start_date_for_vol = daily_returns.index[0] + pd.Timedelta(days=lookback_window)
    
    if first_rebalance_date < required_start_date_for_vol:
         print(f"Warning: Not enough data for the first rebalance on {first_rebalance_date}. "
               f"Need data back to {first_rebalance_date - pd.Timedelta(days=lookback_window)}. "
               f"Adjusting start date or lookback window might be needed.")
         # Trim rebalance dates if needed
         rebalance_dates = rebalance_dates[rebalance_dates >= required_start_date_for_vol]
         if rebalance_dates.empty:
             print("Error: No valid rebalance dates after considering lookback window.")
             return pd.Series(dtype=float), pd.Series(dtype=float), pd.Series(dtype=float)


    # Initialize weights
    # Start with equal weights before the first rebalance
    current_rp_weights = pd.Series(1.0 / num_assets, index=tickers)
    current_ew_weights = pd.Series(1.0 / num_assets, index=tickers)
    last_rp_weights = current_rp_weights.copy() # Store the last calculated weights

    # Initialize portfolio returns Series
    rp_portfolio_returns = pd.Series(index=daily_returns.index, dtype=float)
    ew_portfolio_returns = pd.Series(index=daily_returns.index, dtype=float)

    # Loop through each trading day
    for date in daily_returns.index:
        # Check if it's a rebalancing day (use date from rolling_vol's index alignment)
        # Rebalance at the *start* of the day *after* the rebalance date is calculated
        # So, if 'date' is the first day *after* a calculated rebalance_date, we apply new weights.
        # More practically: Check if the *previous* day was a rebalance signal day.
        
        # Find the most recent rebalance date <= current date
        applicable_rebalance_date = rebalance_dates[rebalance_dates <= date]
        if not applicable_rebalance_date.empty:
            last_signal_date = applicable_rebalance_date[-1]
            
            # Check if we are on the day the rebalance should happen based on signal
            # We use volatility calculated up to 'last_signal_date' to set weights for the period *after* it.
            # To avoid lookahead bias, ensure the vol data is available AT or BEFORE last_signal_date
            if last_signal_date in rolling_vol.index: 
                # Check if we haven't already updated weights based on this signal date
                # This assumes weights applied on 'last_signal_date' hold until the next rebalance date.
                # Let's simplify: If today is a rebalance date, calculate weights based on *previous* data.
                 if date in rebalance_dates and date in rolling_vol.index:
                     # Use volatility from the *previous* available day in rolling_vol
                     vol_date_to_use = rolling_vol.index[rolling_vol.index < date][-1] # Get latest vol before today
                     if vol_date_to_use in rolling_vol.index:
                         current_vol = rolling_vol.loc[vol_date_to_use]
                         current_rp_weights = get_risk_parity_weights(current_vol)
                         last_rp_weights = current_rp_weights.copy() # Store the weights used
                         # Equal weights are constant
                         current_ew_weights = pd.Series(1.0 / num_assets, index=tickers)

        # Calculate portfolio return for the current day using the *current* weights
        # Weights determined at rebalance points hold until the next rebalance
        rp_return_today = (current_rp_weights * daily_returns.loc[date]).sum()
        ew_return_today = (current_ew_weights * daily_returns.loc[date]).sum()

        rp_portfolio_returns.loc[date] = rp_return_today
        ew_portfolio_returns.loc[date] = ew_return_today
        
        # Fill NaNs that might occur at the beginning if weights aren't ready
        rp_portfolio_returns = rp_portfolio_returns.fillna(0)
        ew_portfolio_returns = ew_portfolio_returns.fillna(0)

    return rp_portfolio_returns, ew_portfolio_returns, last_rp_weights

def plot_cumulative_returns(rp_returns, ew_returns, title="Cumulative Returns Comparison"):
    """Plots cumulative returns for the strategies."""
    cumulative_returns = pd.DataFrame({
        "Risk Parity": (1 + rp_returns).cumprod(),
        "Equal Weighted": (1 + ew_returns).cumprod()
    })
    
    plt.figure(figsize=(12, 8))
    ax = cumulative_returns.plot(linewidth=2)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Returns (1 = Initial Investment)")
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout() # Adjust layout
    plt.show()

def main():
    # === Parameters ===
    tickers = ['SPY', 'TLT', 'GLD', 'QQQ'] # Example: Stocks, Bonds, Gold, Nasdaq
    start_date = '2018-01-01'
    end_date = '2023-12-31'
    lookback_window = 60  # Days for rolling volatility calculation
    rebalance_frequency = 'M' # 'M' for monthly, 'Q' for quarterly

    # === Data Fetching ===
    print(f"Fetching data for: {tickers} from {start_date} to {end_date}")
    price_data = fetch_data(tickers, start_date, end_date)

    if price_data.empty:
        print("Exiting due to data fetching issues.")
        return

    # === Calculations ===
    print("Calculating daily returns...")
    daily_returns = calculate_daily_returns(price_data)

    if daily_returns.empty:
        print("Exiting due to issues calculating returns (likely insufficient price data).")
        return
        
    print(f"Backtesting strategies with {lookback_window}-day lookback and {rebalance_frequency} rebalancing...")
    risk_parity_returns, equal_weighted_returns, last_rp_weights = backtest_strategy(
        daily_returns,
        lookback_window=lookback_window,
        rebalance_frequency=rebalance_frequency
    )

    # === Output & Plotting ===
    if not risk_parity_returns.empty and not equal_weighted_returns.empty:
        print("\n--- Backtest Results ---")
        
        # Performance Metrics (Example)
        rp_cumulative = (1 + risk_parity_returns).prod() - 1
        ew_cumulative = (1 + equal_weighted_returns).prod() - 1
        rp_annual_vol = risk_parity_returns.std() * np.sqrt(252)
        ew_annual_vol = equal_weighted_returns.std() * np.sqrt(252)
        
        print(f"Risk Parity Cumulative Return: {rp_cumulative:.2%}")
        print(f"Equal Weighted Cumulative Return: {ew_cumulative:.2%}")
        print(f"Risk Parity Annualized Volatility: {rp_annual_vol:.2%}")
        print(f"Equal Weighted Annualized Volatility: {ew_annual_vol:.2%}")
        
        print("\nLatest Risk Parity Weights (approximate for end period):")
        print(last_rp_weights.round(4))

        plot_title = f"Risk Parity ({rebalance_frequency} Reb, {lookback_window}d Vol) vs Equal Weighted"
        plot_cumulative_returns(risk_parity_returns, equal_weighted_returns, title=plot_title)
    else:
        print("Backtest did not produce results. Check data and parameters.")


if __name__ == "__main__":
    main()

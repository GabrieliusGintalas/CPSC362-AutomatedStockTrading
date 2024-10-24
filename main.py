from fetch_market_data import fetch_market_data, save_to_json
from user_input import get_user_symbol, get_user_date
from datetime import datetime
from historical_graph import plot_historical_graph
import pandas as pd
from SMAalgo import backtest_sma, save_trades_to_csv, plot_signals, analyze_crossovers

def main():
    # Get the user input for the symbol
    symbol = get_user_symbol()

    # Define the start date and end date
    start_date = '2021-01-01'
    
    # Get the user input for data range and validate the date
    while True:
        user_date = get_user_date()
        if user_date > datetime.strptime("01/31/2021", "%m/%d/%Y"):
            end_date = user_date.strftime('%Y-%m-%d')  # Convert to YYYY-MM-DD format for yfinance
            break
        else:
            print("Please enter a date after 01/31/2021.")

    # Fetch the market data
    print(f"Fetching data for {symbol} from {start_date} to {end_date}...")
    data = pd.DataFrame(fetch_market_data(symbol, start_date, end_date))
    
    # Print the data structure to debug
    print("\nData columns:", data.columns)
    print("\nFirst few rows of data:")
    print(data.head())
    
    # Ensure proper datetime index
    if not isinstance(data.index, pd.DatetimeIndex):
        if 'Date' in data.columns:
            data.set_index('Date', inplace=True)
        data.index = pd.to_datetime(data.index)

    # Plot the historical graph
    plot_historical_graph(data, symbol, start_date, end_date)

    # Backtest the SMA strategy
    print("\nRunning SMA backtest...")
    final_balance, trade_log, signals = backtest_sma(data, short_window=50, long_window=200)

    # Save the backtest results to CSV
    save_trades_to_csv(trade_log, final_balance)
    print(f"Backtest complete. Final balance: ${final_balance:.2f}")
    print("Trades saved to sma_crossover_trades.csv.")

    # Plot the trading signals
    print("\nGenerating trading signals visualization...")
    plot_signals(data, signals, symbol)

    # Analyze crossover points
    print("\nAnalyzing trading signals...")
    analyze_crossovers(data, signals)

    # Save the data to a JSON file
    json_filename = f"{symbol}_data.json"
    save_to_json(data, json_filename)
    print(f"\nData saved to {json_filename}")

if __name__ == "__main__":
    main()
from fetch_market_data import fetch_market_data, save_to_json
from user_input import get_user_symbol, get_user_date
from datetime import datetime
from historical_graph import plot_historical_graph
import pandas as pd  

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
    data = fetch_market_data(symbol, start_date, end_date)

    # Plot the historical graph
    plot_historical_graph(pd.DataFrame(data), symbol, start_date, end_date)

    # Save the data to a JSON file
    json_filename = f"{symbol}_data.json"
    save_to_json(data, json_filename)
    print(f"\nData saved to {json_filename}")

if __name__ == "__main__":
    main()
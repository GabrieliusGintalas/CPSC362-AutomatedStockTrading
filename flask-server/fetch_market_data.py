import yfinance as yf
import json
import os

def fetch_market_data(symbol, start_date, end_date):
    """Fetch historical data for a given symbol and filter required fields."""
    ticker = yf.Ticker(symbol)

    data = ticker.history(start=start_date, end=end_date)

    if data.empty:
        raise ValueError(f"No market data found for symbol '{symbol}' between {start_date} and {end_date}.")

    filtered_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()

    filtered_data['Date'] = filtered_data['Date'].apply(lambda x: x.isoformat())
    
    # Convert the filtered data to a JSON format
    json_data = filtered_data.to_dict(orient='records')
    
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, 'history.json')
    
    # Save the data to history.json
    with open(json_file_path, 'w') as f:
        json.dump(json_data, f, indent=4)

    return filtered_data


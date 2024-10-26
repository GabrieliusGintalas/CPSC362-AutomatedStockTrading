import yfinance as yf
import json

def fetch_market_data(symbol, start_date, end_date):
    """Fetch historical data for a given symbol and filter required fields."""
    ticker = yf.Ticker(symbol)

    #stock_info = ticker.info
    #company_name = stock_info.get("longName", "N/A")  # Fetches the company name if available
    
    #print(f"Symbol '{symbol}' refers to: {company_name}")

    data = ticker.history(start=start_date, end=end_date)

    # Select only the required columns: Date, Open, High, Low, Close, Volume
    filtered_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()

    # Convert the filtered data to a dictionary format for JSON serialization
    data_dict = filtered_data.to_dict(orient="records")
    return data_dict

def save_to_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=str)
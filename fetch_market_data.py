import yfinance as yf
import pandas as pd
import json

def fetch_market_data(symbol, start_date, end_date, json_filename):
    """
    Fetches market data for the given symbol and date range, then saves it to a JSON file.
    """
    try:
        data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        if data.empty:
            print("No data fetched.")
            return False
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        data_list = data.to_dict(orient='records')
        with open(json_filename, 'w') as json_file:
            json.dump(data_list, json_file, indent=4)
        print(f"Data for {symbol} saved to {json_filename}.")
        return True
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return False

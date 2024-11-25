import yfinance as yf
import json
import os
import pandas as pd

class MarketData:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def fetch_data(self):
        """Fetch historical data for a given symbol and filter required fields."""
        ticker = yf.Ticker(self.symbol)
        data = ticker.history(start=self.start_date, end=self.end_date)

        if data.empty:
            raise ValueError(f"No market data found for symbol '{self.symbol}' between {self.start_date} and {self.end_date}.")

        filtered_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()
        filtered_data['Date'] = filtered_data['Date'].apply(lambda x: x.isoformat())
        self.data = filtered_data

        return self.data

    def save_to_json(self, filename='history.json'):
        # Convert the filtered data to a JSON format
        json_data = self.data.to_dict(orient='records')

        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, filename)

        # Save the data to history.json
        with open(json_file_path, 'w') as f:
            json.dump(json_data, f, indent=4)

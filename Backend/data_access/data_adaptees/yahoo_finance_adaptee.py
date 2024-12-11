import yfinance as yf
import pandas as pd
import json
import os
from ..data_source_interface import DataSourceInterface

class YahooFinanceAdaptee(DataSourceInterface):
    def fetch_market_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
                
            filtered_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()
            filtered_data['Date'] = filtered_data['Date'].apply(lambda x: x.isoformat())
            return filtered_data
            
        except Exception as e:
            raise Exception(f"Error fetching data from Yahoo Finance: {str(e)}")

    def save_data(self, data: pd.DataFrame, filename: str) -> None:
        try:
            json_data = data.to_dict(orient='records')
            with open(filename, 'w') as f:
                json.dump(json_data, f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving data: {str(e)}")

    def load_data(self, filename: str) -> pd.DataFrame:
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File {filename} not found")
                
            with open(filename, 'r') as f:
                json_data = json.load(f)
            return pd.DataFrame(json_data)
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def get_live_price(self, symbol: str) -> float:
        try:
            ticker = yf.Ticker(symbol)
            # Get the latest price data
            current = ticker.history(period='1d')
            if current.empty:
                raise ValueError(f"No price data found for symbol {symbol}")
            return float(current['Close'].iloc[-1])
        except Exception as e:
            raise Exception(f"Error fetching live price from Yahoo Finance: {str(e)}") 
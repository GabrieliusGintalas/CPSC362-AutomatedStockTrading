from datetime import datetime
import pandas as pd
from .market_data_decorator import MarketDataDecorator

class ValidationDecorator(MarketDataDecorator):
    def fetch_market_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        self._validate_inputs(symbol, start_date, end_date)
        data = super().fetch_market_data(symbol, start_date, end_date)
        self._validate_data(data)
        return data

    def _validate_inputs(self, symbol: str, start_date: str, end_date: str) -> None:
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Invalid symbol")

        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            if end_dt < start_dt:
                raise ValueError("End date must be after start date")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {str(e)}")

    def _validate_data(self, data: pd.DataFrame) -> None:
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}") 
from abc import ABC, abstractmethod
import pandas as pd

class DataSourceInterface(ABC):
    @abstractmethod
    def fetch_market_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch market data for a given symbol between start and end dates"""
        pass

    @abstractmethod
    def save_data(self, data: pd.DataFrame, filename: str) -> None:
        """Save market data to storage"""
        pass

    @abstractmethod
    def load_data(self, filename: str) -> pd.DataFrame:
        """Load market data from storage"""
        pass 
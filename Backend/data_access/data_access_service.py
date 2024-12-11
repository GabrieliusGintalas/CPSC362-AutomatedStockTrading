from typing import Optional
import pandas as pd
from .data_source_interface import DataSourceInterface

class DataAccessService:
    def __init__(self, data_source: DataSourceInterface):
        self.data_source = data_source
        self._cache = {}

    def get_market_data(self, symbol: str, start_date: str, end_date: str, use_cache: bool = True) -> pd.DataFrame:
        """
        Get market data either from cache or data source
        """
        cache_key = f"{symbol}_{start_date}_{end_date}"
        
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
            
        data = self.data_source.fetch_market_data(symbol, start_date, end_date)
        
        if use_cache:
            self._cache[cache_key] = data
            
        return data

    def save_market_data(self, data: pd.DataFrame, symbol: str) -> None:
        """
        Save market data to storage
        """
        filename = f"{symbol}_market_data.json"
        self.data_source.save_data(data, filename)

    def load_market_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Load market data from storage
        """
        filename = f"{symbol}_market_data.json"
        try:
            return self.data_source.load_data(filename)
        except FileNotFoundError:
            return None

    def get_live_price(self, symbol: str) -> float:
        """
        Get live price from data source
        """
        return self.data_source.get_live_price(symbol)
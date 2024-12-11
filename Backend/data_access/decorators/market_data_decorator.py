from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
from ..data_source_interface import DataSourceInterface

class MarketDataDecorator(DataSourceInterface):
    def __init__(self, data_source: DataSourceInterface):
        self._data_source = data_source

    def fetch_market_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        return self._data_source.fetch_market_data(symbol, start_date, end_date)

    def save_data(self, data: pd.DataFrame, filename: str) -> None:
        self._data_source.save_data(data, filename)

    def load_data(self, filename: str) -> pd.DataFrame:
        return self._data_source.load_data(filename)

    def get_live_price(self, symbol: str) -> float:
        return self._data_source.get_live_price(symbol) 
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class TradingStrategyInterface(ABC):
    @abstractmethod
    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate trading signals based on the strategy"""
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of the strategy"""
        pass 

class SMAStrategy(TradingStrategyInterface):
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        data['SMA50'] = data['Close'].rolling(window=self.short_window).mean()
        data['SMA200'] = data['Close'].rolling(window=self.long_window).mean()
        data['signal'] = np.where(
            (data['SMA50'].shift(1) < data['SMA200'].shift(1)) & 
            (data['SMA50'] > data['SMA200']), 1, 0)
        data['signal'] = np.where(
            (data['SMA50'].shift(1) > data['SMA200'].shift(1)) & 
            (data['SMA50'] < data['SMA200']), -1, data['signal'])
        return data

    def get_strategy_name(self) -> str:
        return "SMA" 
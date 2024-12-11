from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class TradingAlgo(ABC):
    @abstractmethod
    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate trading signals based on the strategy"""
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of the strategy"""
        pass 

class SMAStrategy(TradingAlgo):
    def __init__(self, short_window=50, long_window=200):
        self.short_window = short_window
        self.long_window = long_window

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        data['SMA50'] = data['Close'].rolling(window=self.short_window, min_periods=self.short_window).mean()
        data['SMA200'] = data['Close'].rolling(window=self.long_window, min_periods=self.long_window).mean()
        data['signal'] = np.where(
            (data['SMA50'].shift(1) < data['SMA200'].shift(1)) & 
            (data['SMA50'] > data['SMA200']), 1, 0)
        data['signal'] = np.where(
            (data['SMA50'].shift(1) > data['SMA200'].shift(1)) & 
            (data['SMA50'] < data['SMA200']), -1, data['signal'])
        return data

    def get_strategy_name(self) -> str:
        return "SMA"

class BollingerBandsStrategy(TradingAlgo):
    def __init__(self, window=20, num_std_dev=2):
        self.window = window
        self.num_std_dev = num_std_dev

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        data['SMA20'] = data['Close'].rolling(window=self.window).mean()
        data['std_dev'] = data['Close'].rolling(window=self.window).std()
        data['Upper_BB'] = data['SMA20'] + (data['std_dev'] * self.num_std_dev)
        data['Lower_BB'] = data['SMA20'] - (data['std_dev'] * self.num_std_dev)
        data['signal'] = np.where(
            data['Close'] > data['Upper_BB'], -1, 
            np.where(data['Close'] < data['Lower_BB'], 1, 0))
        return data

    def get_strategy_name(self) -> str:
        return "BollingerBands"

class MACDStrategy(TradingAlgo):
    def __init__(self, short_ema=12, long_ema=26, signal_line=9):
        self.short_ema = short_ema
        self.long_ema = long_ema
        self.signal_line = signal_line

    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        data['EMA12'] = data['Close'].ewm(span=self.short_ema, adjust=False).mean()
        data['EMA26'] = data['Close'].ewm(span=self.long_ema, adjust=False).mean()
        data['MACD'] = data['EMA12'] - data['EMA26']
        data['Signal_Line'] = data['MACD'].ewm(span=self.signal_line, adjust=False).mean()
        data['signal'] = np.where(data['MACD'] > data['Signal_Line'], 1, -1)
        return data

    def get_strategy_name(self) -> str:
        return "MACD" 
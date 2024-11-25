import numpy as np

def calculate_sma_signals(data, short_window=50, long_window=200):
    """
    Calculate SMA crossover signals.
    """
    data['SMA50'] = data['Close'].rolling(window=short_window, min_periods=short_window).mean()
    data['SMA200'] = data['Close'].rolling(window=long_window, min_periods=long_window).mean()
    data['SMA_signal'] = np.where(
        (data['SMA50'].shift(1) < data['SMA200'].shift(1)) & (data['SMA50'] > data['SMA200']), 1, 0)
    data['SMA_signal'] = np.where(
        (data['SMA50'].shift(1) > data['SMA200'].shift(1)) & (data['SMA50'] < data['SMA200']), -1, data['SMA_signal'])
    return data

def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    """
    Calculate Bollinger Bands.
    """
    data['SMA20'] = data['Close'].rolling(window=window).mean()
    data['std_dev'] = data['Close'].rolling(window=window).std()
    data['Upper_BB'] = data['SMA20'] + (data['std_dev'] * num_std_dev)
    data['Lower_BB'] = data['SMA20'] - (data['std_dev'] * num_std_dev)
    data['BB_signal'] = np.where(
        data['Close'] > data['Upper_BB'], -1, np.where(data['Close'] < data['Lower_BB'], 1, 0))
    return data

def calculate_macd(data, short_ema=12, long_ema=26, signal_line=9):
    """
    Calculate MACD and generate signals.
    """
    data['EMA12'] = data['Close'].ewm(span=short_ema, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=long_ema, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_line, adjust=False).mean()
    data['MACD_signal'] = np.where(data['MACD'] > data['Signal_Line'], 1, -1)
    return data

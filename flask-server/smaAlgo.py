import numpy as np

def calculate_sma_signals(data, short_window=50, long_window=200):
    """
    Calculate SMA crossover signals.
    """
    data['SMA50'] = data['Close'].rolling(window=short_window, min_periods=short_window).mean()
    data['SMA200'] = data['Close'].rolling(window=long_window, min_periods=long_window).mean()
    data['SMA_signal'] = np.where((data['SMA50'].shift(1) < data['SMA200'].shift(1)) & (data['SMA50'] > data['SMA200']), 1, 0)
    data['SMA_signal'] = np.where((data['SMA50'].shift(1) > data['SMA200'].shift(1)) & (data['SMA50'] < data['SMA200']), -1, data['SMA_signal'])

    return data
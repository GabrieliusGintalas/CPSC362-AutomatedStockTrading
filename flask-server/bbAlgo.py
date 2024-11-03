import numpy as np

def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    """
    Calculate Bollinger Bands.
    """
    data['SMA20'] = data['Close'].rolling(window=window).mean()
    data['std_dev'] = data['Close'].rolling(window=window).std()
    data['Upper_BB'] = data['SMA20'] + (data['std_dev'] * num_std_dev)
    data['Lower_BB'] = data['SMA20'] - (data['std_dev'] * num_std_dev)
    data['BB_signal'] = np.where(data['Close'] > data['Upper_BB'], -1, np.where(data['Close'] < data['Lower_BB'], 1, 0))

    return data
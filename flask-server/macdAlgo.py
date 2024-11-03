import numpy as np

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
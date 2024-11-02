import pandas as pd
import csv
import numpy as np

# Constants
INITIAL_BALANCE = 100000
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

def calculate_sma_signals(data, short_window=50, long_window=200):
    """
    Calculate SMA crossover signals.
    """
    data['SMA50'] = data['Close'].rolling(window=short_window, min_periods=short_window).mean()
    data['SMA200'] = data['Close'].rolling(window=long_window, min_periods=long_window).mean()
    data['SMA_signal'] = np.where((data['SMA50'].shift(1) < data['SMA200'].shift(1)) & (data['SMA50'] > data['SMA200']), 1, 0)
    data['SMA_signal'] = np.where((data['SMA50'].shift(1) > data['SMA200'].shift(1)) & (data['SMA50'] < data['SMA200']), -1, data['SMA_signal'])

    return data

def calculate_signals(data, algorithm):
    """
    Calculate signals based on the selected algorithm.
    """
    if algorithm == 'SMA':
        data = calculate_sma_signals(data)
        data['signal'] = data['SMA_signal']
    elif algorithm == 'BollingerBands':
        data = calculate_bollinger_bands(data)
        data['signal'] = data['BB_signal']
    elif algorithm == 'MACD':
        data = calculate_macd(data)
        data['signal'] = data['MACD_signal']
    else:
        raise ValueError("Invalid algorithm. Choose 'SMA', 'BollingerBands', or 'MACD'.")
    
    return data

def backtest(data, symbol, algorithm):
    """
    Backtest a trading strategy based on the selected algorithm (SMA, Bollinger Bands, MACD).
    """
    balance = INITIAL_BALANCE
    shares = 0
    trade_log = []
    
    data = calculate_signals(data, algorithm)

    for i in range(len(data)):
        price = data['Close'].iloc[i]
        signal = data['signal'].iloc[i]
        date = pd.to_datetime(data['Date'].iloc[i]).strftime('%m/%d/%Y')

        # Buy signal
        if signal == 1 and shares == 0:
            shares = balance // price
            transaction_amount = shares * price
            balance -= transaction_amount
            trade_log.append({
                'date': date,
                'symbol': symbol,
                'action': 'BUY',
                'price': price,
                'shares': shares,
                'transaction_amount': transaction_amount,
                'gain/loss': None,
                'balance': balance
            })
        
        # Sell signal
        elif signal == -1 and shares > 0:
            transaction_amount = shares * price
            gain_loss = transaction_amount - (shares * trade_log[-1]['price'])
            balance += transaction_amount
            trade_log.append({
                'date': date,
                'symbol': symbol,
                'action': 'SELL',
                'price': price,
                'shares': shares,
                'transaction_amount': transaction_amount,
                'gain/loss': gain_loss,
                'balance': balance
            })
            shares = 0  # Reset shares after selling

    # Final sell if shares remain
    if shares > 0:
        price = data['Close'].iloc[-1]
        transaction_amount = shares * price
        gain_loss = transaction_amount - (shares * trade_log[-1]['price'])
        balance += transaction_amount
        trade_log.append({
            'date': date,
            'symbol': symbol,
            'action': 'SELL',
            'price': price,
            'shares': shares,
            'transaction_amount': transaction_amount,
            'gain/loss': gain_loss,
            'balance': balance
        })

    total_gain_loss = sum(trade['gain/loss'] for trade in trade_log if trade['gain/loss'] is not None)
    start_date = pd.to_datetime(data['Date'].iloc[0])
    end_date = pd.to_datetime(data['Date'].iloc[-1])
    total_days = (end_date - start_date).days
    total_years = total_days / 365.25
    total_return = (balance / INITIAL_BALANCE - 1) * 100
    annual_return = ((balance / INITIAL_BALANCE) ** (1 / total_years) - 1) * 100 if total_years > 0 else 0

    return balance, trade_log, total_gain_loss, annual_return, total_return

def save_trades_to_csv(trade_log, final_balance, symbol, algorithm):
    filename = f"{symbol}_{algorithm}_trades.csv"
    fieldnames = [
        'date', 'symbol', 'action', 'price', 'shares', 
        'transaction_amount', 'gain/loss', 'balance'
    ]
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for trade in trade_log:
            writer.writerow(trade)
        summary_writer = csv.writer(file)
        total_gain_loss = sum(trade['gain/loss'] for trade in trade_log if trade['gain/loss'] is not None)
        summary_writer.writerow([f"Total Gain/Loss: {total_gain_loss:.2f} | Final Balance: {final_balance:.2f}"])



        

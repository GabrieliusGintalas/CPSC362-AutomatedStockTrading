import pandas as pd
import csv
import numpy as np

# Constants
INITIAL_BALANCE = 100000
SHORT_WINDOW = 50
LONG_WINDOW = 200

def calculate_signals(data, short_window=50, long_window=200):
    """
    Calculate trading signals with precise crossover detection.
    """
    # Calculate SMAs
    data = data.copy()
    data['SMA50'] = data['Close'].rolling(window=short_window, min_periods=short_window).mean()
    data['SMA200'] = data['Close'].rolling(window=long_window, min_periods=long_window).mean()
    
    # Calculate difference between SMAs
    data['SMA_diff'] = data['SMA50'] - data['SMA200']
    
    # Generate signals based on crossover: 1 for Buy (crossing above), -1 for Sell (crossing below)
    data['signal'] = 0
    data['signal'] = np.where((data['SMA50'].shift(1) < data['SMA200'].shift(1)) & (data['SMA50'] > data['SMA200']), 1, 0)
    data['signal'] = np.where((data['SMA50'].shift(1) > data['SMA200'].shift(1)) & (data['SMA50'] < data['SMA200']), -1, data['signal'])
    
    # Calculate positions (signal changes)
    data['position'] = data['signal'].diff()
    
    return data

def backtest_sma(data, short_window=SHORT_WINDOW, long_window=LONG_WINDOW):
    """Backtest an SMA crossover strategy with flipped crossover logic."""
    balance = INITIAL_BALANCE
    shares = 0
    trade_log = []
    last_signal = 0  # Track the last crossover to avoid multiple trades on initial data.

    # Calculate the signals using the function
    data = calculate_signals(data, short_window, long_window)

    for i in range(len(data)):
        price = data['Close'].iloc[i]
        position = data['position'].iloc[i]
        signal = data['signal'].iloc[i]

        # Execute buy when SMA50 crosses above SMA200
        if signal == 1 and shares == 0 and last_signal != 1:  # Buy signal (SMA50 crosses above SMA200)
            shares = balance // price  # Buy as many shares as possible
            transaction_amount = shares * price
            balance -= transaction_amount
            trade_log.append({
                'date': data.index[i],
                'action': 'BUY',
                'price': price,
                'shares': shares,
                'transaction_amount': transaction_amount,
                'gain/loss': None,
                'balance': balance
            })
            last_signal = 1  # Update last signal to prevent repeated buys
            print(f"BUY on {data.index[i]}: Price = {price}")

        # Execute sell when SMA50 crosses below SMA200
        elif signal == -1 and shares > 0 and last_signal != -1:  # Sell signal (SMA50 crosses below SMA200)
            transaction_amount = shares * price
            gain_loss = transaction_amount - (shares * trade_log[-1]['price'])
            balance += transaction_amount
            trade_log.append({
                'date': data.index[i],
                'action': 'SELL',
                'price': price,
                'shares': shares,
                'transaction_amount': transaction_amount,
                'gain/loss': gain_loss,
                'balance': balance
            })
            shares = 0  # Reset shares after selling
            last_signal = -1  # Update last signal to prevent repeated sells
            print(f"SELL on {data.index[i]}: Price = {price}")

    # Sell any remaining shares at the last price (only if we bought them earlier)
    if shares > 0:
        price = data['Close'].iloc[-1]
        transaction_amount = shares * price
        gain_loss = transaction_amount - (shares * trade_log[-1]['price'])
        balance += transaction_amount
        trade_log.append({
            'date': data.index[-1],
            'action': 'SELL',
            'price': price,
            'shares': shares,
            'transaction_amount': transaction_amount,
            'gain/loss': gain_loss,
            'balance': balance
        })
        print(f"Final SELL on {data.index[-1]}: Price = {price}")

    return balance, trade_log

def save_trades_to_csv(trade_log, final_balance, data, symbol):
    filename = "sma_crossover_trades.csv"
    
    # Calculate totals and performance metrics
    total_gain_loss = sum(trade['gain/loss'] for trade in trade_log if trade['gain/loss'] is not None)
    start_date = data.index[0]
    end_date = data.index[-1]
    total_days = (end_date - start_date).days
    total_years = total_days / 365.25
    annual_return = (final_balance / INITIAL_BALANCE) ** (1 / total_years) - 1 if total_years > 0 else 0
    total_return = (final_balance / INITIAL_BALANCE - 1) * 100

    # Define the CSV fieldnames
    fieldnames = [
        'date', 
        'symbol', 
        'action', 
        'price', 
        'shares', 
        'transaction_amount', 
        'gain/loss', 
        'balance'
    ]
    
    # Open the file for writing
    with open(filename, mode='w', newline='') as file:
        # Initialize the DictWriter with the fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()

        # Record all the trades in the CSV
        for trade in trade_log:
            writer.writerow({
                'date'               : trade['date'],
                'symbol'             : symbol,
                'action'             : trade['action'],
                'price'              : trade['price'],
                'shares'             : trade['shares'],
                'transaction_amount' : trade['transaction_amount'],
                'gain/loss'          : trade['gain/loss'],
                'balance'            : trade['balance']
            })

    # Write the summary in one line without extra fields
    with open(filename, mode='a', newline='') as file:  # Open in append mode
        summary_writer = csv.writer(file)
        summary_writer.writerow([
            f"Gain/Loss for all trades: ${total_gain_loss:.2f} | Annual % Return: {annual_return * 100:.2f}% | Total % Return: {total_return:.2f}%"
        ])



        
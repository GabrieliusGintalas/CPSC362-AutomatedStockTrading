import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
import csv

# Constants
INITIAL_BALANCE = 100000
SHORT_WINDOW = 50
LONG_WINDOW = 200

def calculate_sma(data, window):
    """Calculate the Simple Moving Average (SMA) for a given window size."""
    return data['Close'].rolling(window=window).mean()

def backtest_sma(data, short_window, long_window):
    """Backtest the SMA cross-over strategy."""
    data['SMA_short'] = calculate_sma(data, short_window)
    data['SMA_long'] = calculate_sma(data, long_window)
    
    # Initialize variables for tracking trades
    balance = INITIAL_BALANCE
    shares = 0
    trade_log = []
    
    # Iterate over data to simulate trades
    for i in range(1, len(data)):
        if data['SMA_short'].iloc[i] > data['SMA_long'].iloc[i] and data['SMA_short'].iloc[i-1] <= data['SMA_long'].iloc[i-1]:
            # Buy signal
            price = data['Close'].iloc[i]
            shares_to_buy = balance // price
            balance -= shares_to_buy * price
            shares += shares_to_buy
            transaction = {
                "date": data.index[i].strftime('%Y-%m-%d'),
                "action": "BUY",
                "price": price,
                "shares": shares_to_buy,
                "transaction_amount": -shares_to_buy * price,
                "balance": balance,
                "gain/loss": None  # Gain/loss is not calculated at buying
            }
            trade_log.append(transaction)
        
        elif data['SMA_short'].iloc[i] < data['SMA_long'].iloc[i] and data['SMA_short'].iloc[i-1] >= data['SMA_long'].iloc[i-1]:
            # Sell signal
            if shares > 0:
                price = data['Close'].iloc[i]
                balance += shares * price
                gain_loss = shares * (price - transaction['price'])  # Assuming last buy
                transaction = {
                    "date": data.index[i].strftime('%Y-%m-%d'),
                    "action": "SELL",
                    "price": price,
                    "shares": -shares,
                    "transaction_amount": shares * price,
                    "balance": balance,
                    "gain/loss": gain_loss
                }
                shares = 0  # Reset shares after selling
                trade_log.append(transaction)
    
    # Sell any remaining shares at the last available price
    if shares > 0:
        last_price = data['Close'].iloc[-1]
        balance += shares * last_price
        trade_log.append({
            "date": data.index[-1].strftime('%Y-%m-%d'),
            "action": "SELL",
            "price": last_price,
            "shares": -shares,
            "transaction_amount": shares * last_price,
            "balance": balance,
            "gain/loss": shares * (last_price - data['Close'].iloc[-1])
        })
    
    # Return final balance and trade log
    return balance, trade_log

def save_trades_to_csv(trade_log, final_balance):
    """Save the trade log to a CSV file, including a summary."""
    filename = "sma_crossover_trades.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'date', 'action', 'price', 'shares', 'transaction_amount', 'gain/loss', 'balance'
        ])
        writer.writeheader()
        writer.writerows(trade_log)
        writer.writerow({
            "date": "SUMMARY",
            "action": "",
            "price": "",
            "shares": "",
            "transaction_amount": "",
            "gain/loss": sum(trade['gain/loss'] for trade in trade_log if trade['gain/loss'] is not None),
            "balance": final_balance
        })
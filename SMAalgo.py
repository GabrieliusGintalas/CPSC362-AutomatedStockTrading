import pandas as pd
import csv

# Constants
INITIAL_BALANCE = 100000
SHORT_WINDOW = 50
LONG_WINDOW = 200

def calculate_sma(data, window):
    """Calculate the Simple Moving Average (SMA) for a given window size."""
    return data['Close'].rolling(window=window).mean()


def backtest_sma(data, short_window, long_window):
    """Backtest an SMA crossover strategy."""
    balance = INITIAL_BALANCE
    shares = 0
    trade_log = []

    data = data.dropna(subset=['Close'])
    small_windows = calculate_sma(data, short_window)
    long_windows = calculate_sma(data, long_window)

    for i in range(long_window, len(data)):
        # Calculate SMAs for the current day
        short_sma = small_windows.iloc[i]
        long_sma = long_windows.iloc[i]
        price = data['Close'].iloc[i]

        if short_sma > long_sma and shares == 0:
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
            print(f"BUY on {data.index[i]}: Short SMA = {short_sma}, Long SMA = {long_sma}, Price = {price}")

        elif short_sma < long_sma and shares > 0:
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
            print(f"SELL on {data.index[i]}: Short SMA = {short_sma}, Long SMA = {long_sma}, Price = {price}")

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
        print(f"Final SELL on {data.index[-1]}: Short SMA = {short_sma}, Long SMA = {long_sma}, Price = {price}")

    return balance, trade_log



def save_trades_to_csv(trade_log, final_balance):
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
        

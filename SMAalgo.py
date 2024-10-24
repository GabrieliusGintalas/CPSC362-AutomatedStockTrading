import pandas as pd
import csv
from datetime import datetime

# Constants
INITIAL_BALANCE = 100000
STOP_LOSS_PERCENT = 0.05    # 5% stop-loss
TAKE_PROFIT_PERCENT = 0.10  # 10% take-profit
MIN_HOLDING_PERIOD = 10     # Minimum holding period in days

def get_price_column(data):
    if 'Adj Close' in data.columns:
        return 'Adj Close'
    else:
        return 'Close'

def calculate_sma(data, window):
    price_col = get_price_column(data)
    return data[price_col].rolling(window=window).mean()

def backtest_sma_strategy(
    data,
    symbol,
    short_window,
    long_window,
):
    balance = INITIAL_BALANCE
    shares = 0
    trade_log = []
    buy_price = None
    holding_period = 0
    price_col = get_price_column(data)
    data = data.dropna(subset=[price_col])
    data['Short_SMA'] = calculate_sma(data, short_window)
    data['Long_SMA'] = calculate_sma(data, long_window)
    data = data.dropna(subset=['Short_SMA', 'Long_SMA'])
    data['Signal'] = 0

    for i in range(1, len(data)):
        short_sma_prev = data['Short_SMA'].iloc[i - 1]
        long_sma_prev = data['Long_SMA'].iloc[i - 1]
        short_sma_curr = data['Short_SMA'].iloc[i]
        long_sma_curr = data['Long_SMA'].iloc[i]
        price = data[price_col].iloc[i]
        date = data.index[i]

        if shares > 0:
            holding_period += 1

            # Check for stop-loss or take-profit
            price_change = (price - buy_price) / buy_price
            if price_change >= TAKE_PROFIT_PERCENT:
                transaction_amount = shares * price
                gain_loss = (price - buy_price) * shares
                balance += transaction_amount
                trade_log.append({
                    'date': date.strftime('%m/%d/%Y'),
                    'symbol': symbol,
                    'action': 'SELL (Take Profit)',
                    'price': price,
                    'shares': shares,
                    'transaction_amount': transaction_amount,
                    'gain/loss': gain_loss,
                    'balance': balance
                })
                data.at[date, 'Signal'] = -1
                shares = 0
                buy_price = None
                holding_period = 0
                continue
            elif price_change <= -STOP_LOSS_PERCENT:
                transaction_amount = shares * price
                gain_loss = (price - buy_price) * shares
                balance += transaction_amount
                trade_log.append({
                    'date': date.strftime('%m/%d/%Y'),
                    'symbol': symbol,
                    'action': 'SELL (Stop Loss)',
                    'price': price,
                    'shares': shares,
                    'transaction_amount': transaction_amount,
                    'gain/loss': gain_loss,
                    'balance': balance
                })
                data.at[date, 'Signal'] = -1
                shares = 0
                buy_price = None
                holding_period = 0
                continue

            # Updated Sell Signal: Sell when short SMA crosses above long SMA
            if (
                short_sma_prev <= long_sma_prev and
                short_sma_curr > long_sma_curr and
                holding_period >= MIN_HOLDING_PERIOD
            ):
                transaction_amount = shares * price
                gain_loss = (price - buy_price) * shares
                balance += transaction_amount
                trade_log.append({
                    'date': date.strftime('%m/%d/%Y'),
                    'symbol': symbol,
                    'action': 'SELL',
                    'price': price,
                    'shares': shares,
                    'transaction_amount': transaction_amount,
                    'gain/loss': gain_loss,
                    'balance': balance
                })
                data.at[date, 'Signal'] = -1
                shares = 0
                buy_price = None
                holding_period = 0
        else:
            holding_period = 0

            # Updated Buy Signal: Buy when short SMA crosses below long SMA
            if (
                short_sma_prev >= long_sma_prev and
                short_sma_curr < long_sma_curr and
                shares == 0
            ):
                shares = int(balance / price)
                if shares > 0:
                    transaction_amount = shares * price
                    balance -= transaction_amount
                    buy_price = price
                    trade_log.append({
                        'date': date.strftime('%m/%d/%Y'),
                        'symbol': symbol,
                        'action': 'BUY',
                        'price': price,
                        'shares': shares,
                        'transaction_amount': -transaction_amount,
                        'gain/loss': None,
                        'balance': balance
                    })
                    data.at[date, 'Signal'] = 1
                    holding_period = 0

    # Sell remaining shares at the end
    if shares > 0:
        price = data[price_col].iloc[-1]
        date = data.index[-1]
        transaction_amount = shares * price
        gain_loss = (price - buy_price) * shares
        balance += transaction_amount
        trade_log.append({
            'date': date.strftime('%m/%d/%Y'),
            'symbol': symbol,
            'action': 'SELL (End of Period)',
            'price': price,
            'shares': shares,
            'transaction_amount': transaction_amount,
            'gain/loss': gain_loss,
            'balance': balance
        })
        data.at[date, 'Signal'] = -1
        shares = 0
        buy_price = None

    return balance, trade_log, data

def optimize_sma_windows(data, symbol):
    from itertools import product

    # Define ranges for SMA windows
    short_window_range = range(5, 51, 5)    # Short SMA from 5 to 50 in steps of 5
    long_window_range = range(20, 201, 20)  # Long SMA from 20 to 200 in steps of 20

    best_profit_per_trade = float('-inf')
    best_result = None

    for short_window, long_window in product(short_window_range, long_window_range):
        if short_window >= long_window:
            continue

        final_balance, trade_log, data_with_signals = backtest_sma_strategy(
            data.copy(), symbol, short_window, long_window
        )

        # Calculate gains/losses for closed trades
        gains_losses = [
            trade['gain/loss'] for trade in trade_log
            if trade['action'].startswith('SELL') and trade['gain/loss'] is not None
        ]
        total_gain_loss = sum(gains_losses)
        num_trades = len(gains_losses)

        if num_trades > 0:
            profit_per_trade = total_gain_loss / num_trades

            # Check if this combination yields higher profit per trade
            if profit_per_trade > best_profit_per_trade:
                best_profit_per_trade = profit_per_trade
                best_result = (final_balance, trade_log, data_with_signals, short_window, long_window, best_profit_per_trade)
                print(f"New best profit per trade: ${profit_per_trade:.2f} with short_window={short_window}, long_window={long_window}")

    if best_result:
        final_balance, trade_log, data_with_signals, short_window, long_window, best_profit_per_trade = best_result
        print(f"Optimal SMA windows for max profit per trade: short_window={short_window}, long_window={long_window}")
        return final_balance, trade_log, data_with_signals, short_window, long_window, best_profit_per_trade
    else:
        print("No profitable SMA window combination found.")
        return None, None, None, None, None, None

def save_trades_to_csv(trade_log, final_balance):
    """Save the trade log and summary statistics to a CSV file."""
    filename = "sma_crossover_trades.csv"
    fieldnames = [
        'date',
        'symbol',
        'action',
        'price',
        'shares',
        'transaction_amount',
        'gain/loss',
        'balance',
    ]
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for trade in trade_log:
            # Format monetary amounts
            formatted_trade = trade.copy()
            formatted_trade['price'] = f"${trade['price']:,.2f}"
            formatted_trade['transaction_amount'] = (
                f"${trade['transaction_amount']:,.2f}"
                if trade['transaction_amount'] is not None
                else ''
            )
            formatted_trade['gain/loss'] = (
                f"${trade['gain/loss']:,.2f}" if trade['gain/loss'] is not None else ''
            )
            formatted_trade['balance'] = f"${trade['balance']:,.2f}"
            writer.writerow(formatted_trade)

        # Final summary row
        total_gain_loss = sum(
            trade['gain/loss'] for trade in trade_log if trade['gain/loss'] is not None
        )
        total_return = (final_balance - INITIAL_BALANCE) / INITIAL_BALANCE * 100
        # Calculate annual return
        if trade_log:
            start_date = datetime.strptime(trade_log[0]['date'], '%m/%d/%Y')
            end_date = datetime.strptime(trade_log[-1]['date'], '%m/%d/%Y')
            days = (end_date - start_date).days
            years = days / 365.25
            if years > 0:
                annual_return = ((final_balance / INITIAL_BALANCE) ** (1 / years) - 1) * 100
            else:
                annual_return = 0.0
        else:
            annual_return = 0.0

        # Write summary rows with formatted amounts
        writer.writerow({
            'date': 'SUMMARY',
            'symbol': '',
            'action': '',
            'price': '',
            'shares': '',
            'transaction_amount': '',
            'gain/loss': f"${total_gain_loss:,.2f}",
            'balance': f"${final_balance:,.2f}",
        })
        writer.writerow({
            'date': '',
            'symbol': '',
            'action': 'Total Return (%)',
            'price': f"{total_return:.2f}%",
            'shares': '',
            'transaction_amount': '',
            'gain/loss': 'Annual Return (%)',
            'balance': f"{annual_return:.2f}%",
        })

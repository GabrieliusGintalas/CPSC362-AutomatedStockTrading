import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv

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
    
    # Generate signals
    data['signal'] = 0
    data['signal'] = np.where(data['SMA_diff'] > 0, 1, 0)
    
    # Calculate positions
    data['position'] = data['signal'].diff()
    
    return data

def backtest_sma(data, short_window=50, long_window=200):
    """
    Implement SMA crossover strategy with improved signal generation.
    """
    # Initial capital and shares
    initial_capital = 100000
    shares_per_trade = 100
    
    # Calculate signals
    signals = calculate_signals(data, short_window, long_window)
    
    # Initialize portfolio tracking
    portfolio = pd.DataFrame(index=signals.index)
    portfolio['holdings'] = 0.0
    portfolio['cash'] = initial_capital
    portfolio['total'] = initial_capital
    
    # Track trades
    trade_log = []
    position = 0
    
    for i in range(len(signals)):
        date = signals.index[i]
        price = signals['Close'].iloc[i]
        
        if signals['position'].iloc[i] != 0:
            if signals['position'].iloc[i] == 1:  # Buy signal
                if position == 0:  # Only buy if we don't have a position
                    shares = shares_per_trade
                    cost = shares * price
                    position = shares
                    
                    portfolio.loc[date, 'holdings'] = shares * price
                    portfolio.loc[date, 'cash'] -= cost
                    
                    trade_log.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'symbol': 'STOCK',
                        'action': 'BUY',
                        'price': price,
                        'shares': shares,
                        'amount': -cost,
                        'gain_loss': 0,
                        'balance': portfolio.loc[date, 'cash'] + portfolio.loc[date, 'holdings']
                    })
            
            elif signals['position'].iloc[i] == -1:  # Sell signal
                if position > 0:  # Only sell if we have a position
                    proceeds = position * price
                    gain_loss = proceeds - (position * signals['Close'].iloc[i-1])
                    
                    portfolio.loc[date, 'holdings'] = 0
                    portfolio.loc[date, 'cash'] += proceeds
                    position = 0
                    
                    trade_log.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'symbol': 'STOCK',
                        'action': 'SELL',
                        'price': price,
                        'shares': -shares_per_trade,
                        'amount': proceeds,
                        'gain_loss': gain_loss,
                        'balance': portfolio.loc[date, 'cash'] + portfolio.loc[date, 'holdings']
                    })
        
        # Update portfolio value for days without trades
        portfolio.loc[date, 'holdings'] = position * signals['Close'].iloc[i]
        portfolio.loc[date, 'total'] = portfolio.loc[date, 'cash'] + portfolio.loc[date, 'holdings']
    
    final_balance = portfolio['total'].iloc[-1]
    return final_balance, trade_log, signals

def save_trades_to_csv(trade_log, final_balance, filename='sma_crossover_trades.csv'):
    """
    Save trade log to CSV file with detailed information and summary statistics.
    """
    # Calculate summary statistics
    initial_capital = 100000
    total_gain_loss = sum(trade['gain_loss'] for trade in trade_log)
    total_return_pct = ((final_balance - initial_capital) / initial_capital) * 100
    
    # Calculate annualized return if there are trades
    if trade_log:
        first_trade_date = datetime.strptime(trade_log[0]['date'], '%Y-%m-%d')
        last_trade_date = datetime.strptime(trade_log[-1]['date'], '%Y-%m-%d')
        years = (last_trade_date - first_trade_date).days / 365.25
        if years > 0:
            annual_return_pct = ((1 + total_return_pct/100) ** (1/years) - 1) * 100
        else:
            annual_return_pct = total_return_pct
    else:
        annual_return_pct = 0

    # Write trades to CSV
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'date', 'symbol', 'action', 'price', 'shares', 
            'amount', 'gain_loss', 'balance'
        ])
        
        # Write header
        writer.writeheader()
        
        # Write all trades
        for trade in trade_log:
            writer.writerow({
                'date': trade['date'],
                'symbol': trade['symbol'],
                'action': trade['action'],
                'price': f"${trade['price']:.2f}",
                'shares': trade['shares'],
                'amount': f"${trade['amount']:.2f}",
                'gain_loss': f"${trade['gain_loss']:.2f}",
                'balance': f"${trade['balance']:.2f}"
            })
        
        # Add blank row before summary
        writer.writerow({
            'date': '',
            'symbol': '',
            'action': '',
            'price': '',
            'shares': '',
            'amount': '',
            'gain_loss': '',
            'balance': ''
        })
        
        # Write summary statistics
        writer.writerow({
            'date': 'SUMMARY',
            'symbol': '',
            'action': '',
            'price': '',
            'shares': '',
            'amount': f'Total Return: ${total_gain_loss:,.2f}',
            'gain_loss': f'Total Return %: {total_return_pct:.2f}%',
            'balance': f'Final Balance: ${final_balance:,.2f}'
        })
        
        writer.writerow({
            'date': '',
            'symbol': '',
            'action': '',
            'price': '',
            'shares': '',
            'amount': '',
            'gain_loss': f'Annual Return: {annual_return_pct:.2f}%',
            'balance': ''
        })

    print(f"\nTrade log saved to {filename}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Final Balance: ${final_balance:,.2f}")
    print(f"Total Return: ${total_gain_loss:,.2f} ({total_return_pct:.2f}%)")
    print(f"Annualized Return: {annual_return_pct:.2f}%")

def plot_signals(data, signals, symbol):
    """
    Plot the trading signals and moving averages.
    """
    plt.figure(figsize=(15, 7))
    
    # Plot price and moving averages
    plt.plot(data.index, data['Close'], label='Price', alpha=0.5)
    plt.plot(data.index, signals['SMA50'], label='50-day SMA', alpha=0.8)
    plt.plot(data.index, signals['SMA200'], label='200-day SMA', alpha=0.8)
    
    # Plot buy signals
    buy_signals = signals[signals['position'] == 1]
    plt.scatter(buy_signals.index, data.loc[buy_signals.index]['Close'], 
               marker='^', color='green', label='Buy', s=100)
    
    # Plot sell signals
    sell_signals = signals[signals['position'] == -1]
    plt.scatter(sell_signals.index, data.loc[sell_signals.index]['Close'], 
               marker='v', color='red', label='Sell', s=100)
    
    plt.title(f'{symbol} - SMA Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analyze_crossovers(data, signals, days_around=5):
    """
    Print detailed information about each crossover point.
    """
    crossovers = signals[signals['position'] != 0]
    
    print("\n=== Crossover Analysis ===")
    for idx, row in crossovers.iterrows():
        print(f"\nCrossover at {idx.strftime('%Y-%m-%d')}:")
        print(f"{'Day':12} {'Close':>10} {'SMA50':>10} {'SMA200':>10} {'Diff':>10}")
        print("-" * 55)
        
        # Get data around the crossover point
        start_date = idx - timedelta(days=days_around)
        end_date = idx + timedelta(days=days_around)
        window_data = signals.loc[start_date:end_date]
        
        for date, values in window_data.iterrows():
            print(f"{date.strftime('%Y-%m-%d')} {values['Close']:10.2f} {values['SMA50']:10.2f} "
                  f"{values['SMA200']:10.2f} {values['SMA_diff']:10.2f}")
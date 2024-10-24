import matplotlib.pyplot as plt
import pandas as pd

def plot_historical_graph(data, symbol, start_date, end_date):
    price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
    data.reset_index(inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data[price_col], label=f'{symbol} Price', color='blue', linewidth=1)
    plt.title(f"{symbol} Historical Price from {start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def plot_backtest_results(data, symbol, start_date, end_date):
    price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
    data.reset_index(inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data[price_col], label=f'{symbol} Price', color='blue', linewidth=1)

    # Plot SMAs
    plt.plot(data['Date'], data['Short_SMA'], label='Short SMA', color='red', linewidth=1)
    plt.plot(data['Date'], data['Long_SMA'], label='Long SMA', color='green', linewidth=1)

    # Plot buy signals
    buy_signals = data[data['Signal'] == 1]
    plt.scatter(buy_signals['Date'], buy_signals[price_col], label='Buy Signal', marker='^', color='green', s=100)

    # Plot sell signals
    sell_signals = data[data['Signal'] == -1]
    plt.scatter(sell_signals['Date'], sell_signals[price_col], label='Sell Signal', marker='v', color='red', s=100)

    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m/%d/%Y'))
    plt.xticks(rotation=45)

    plt.title(f"{symbol} Price with SMA and Trading Signals from {start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

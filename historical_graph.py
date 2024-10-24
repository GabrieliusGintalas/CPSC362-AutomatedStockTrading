import matplotlib.pyplot as plt
import pandas as pd
import time

def plot_historical_graph(data, symbol, start_date, end_date):
    """Plot historical graph from start_date to end_date."""
    # Create a copy of the data to avoid modifying the original
    data = data.copy()
    
    # Check if the index is already datetime
    if not isinstance(data.index, pd.DatetimeIndex):
        # Convert index to datetime if it's not already
        data.index = pd.to_datetime(data.index)

    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data['Close'], label='Close Price')

    # Format the x-axis as MM/DD/YYYY
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m/%d/%Y'))

    plt.title(f"{symbol} Price from {start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Show the plot without blocking
    plt.show()
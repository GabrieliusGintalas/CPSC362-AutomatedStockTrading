# Update the historical_graph.py with date formatting:
import matplotlib.pyplot as plt
import pandas as pd  


def plot_historical_graph(data, symbol, start_date, end_date):
    """Plot historical graph from start_date to end_date with MM/DD/YYYY format."""
    data['Date'] = pd.to_datetime(data['Date'])  # Ensure date is in datetime format
    data.set_index('Date', inplace=True)  # Set Date as index for plotting

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
    plt.show()

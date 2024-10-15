import matplotlib.pyplot as plt
import pandas as pd  

def plot_historical_graph(data, symbol, start_date, end_date):
    """Plot the historical graph for the stock data."""
    # Convert 'Date' column to datetime if it's not already
    data['Date'] = pd.to_datetime(data['Date'])

    # Set the 'Date' column as the index for easy plotting
    data.set_index('Date', inplace=True)

    # Plot the 'Close' price over time
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label=f'{symbol} Closing Price')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.title(f'{symbol} Stock Price from {start_date} to {end_date}')
    plt.legend()

    # Display the graph
    plt.grid(True)
    plt.show()

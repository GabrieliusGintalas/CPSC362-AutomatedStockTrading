import yfinance as yf

def fetch_market_data(symbol, start_date, end_date):
    """Fetch historical data for a given symbol and filter required fields."""
    ticker = yf.Ticker(symbol)

    # Fetch the historical data
    data = ticker.history(start=start_date, end=end_date)

    # Check if data is empty
    if data.empty:
        raise ValueError(f"No market data found for symbol '{symbol}' between {start_date} and {end_date}.")

    # Select only the required columns: Date, Open, High, Low, Close, Volume
    filtered_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()

    # Convert the 'Date' column to ISO format for JSON serialization
    filtered_data['Date'] = filtered_data['Date'].apply(lambda x: x.isoformat())

    return filtered_data


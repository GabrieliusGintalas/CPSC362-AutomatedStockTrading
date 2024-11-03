import yfinance as yf

def fetch_market_data(symbol, start_date, end_date):
    """Fetch historical data for a given symbol and filter required fields."""
    ticker = yf.Ticker(symbol)

    data = ticker.history(start=start_date, end=end_date)

    if data.empty:
        raise ValueError(f"No market data found for symbol '{symbol}' between {start_date} and {end_date}.")

    filtered_data = data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()

    filtered_data['Date'] = filtered_data['Date'].apply(lambda x: x.isoformat())

    return filtered_data


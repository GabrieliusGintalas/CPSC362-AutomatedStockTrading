# Import the necessary functions from the other Python files
from fetch_market_data import fetch_market_data, save_to_json, insert_into_mongodb
from user_input import get_user_input
from datetime import datetime

def main():
    # Get the user input for the symbol
    symbol = get_user_input()

    # Define the date range
    start_date = '2021-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')  # Get current date

    # Fetch the market data
    print(f"Fetching data for {symbol}...")
    data = fetch_market_data(symbol, start_date, end_date)

    # Print the fetched data for the user
    #print(f"\nData for {symbol}:")
    #for record in data:
    #    print(record)  # Print each record line by line

    # Save the data to a JSON file
    json_filename = f"{symbol}_data.json"
    save_to_json(data, json_filename)
    print(f"\nData saved to {json_filename}")

    # Insert the data into MongoDB
    insert_into_mongodb(data)

if __name__ == "__main__":
    main()


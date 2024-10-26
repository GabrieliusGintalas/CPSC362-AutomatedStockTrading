from flask import Flask, request, jsonify
from fetch_market_data import fetch_market_data
from datetime import datetime

app = Flask(__name__)

@app.route('/fetch_market_data', methods=['POST'])
def fetch_data():
    # Extract symbol and date range from the request
    data = request.json
    symbol = data.get('symbol')
    start_date = "2021-01-01"
    end_date = data.get('end_date')

    # Fetch market data using your Python function
    try:
        market_data = fetch_market_data(symbol, start_date, end_date)
        return jsonify(market_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


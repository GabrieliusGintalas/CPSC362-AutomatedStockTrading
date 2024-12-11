from datetime import datetime
from flask import Flask, request, jsonify

from models.market_data_adapter import MarketDataAdapter
from models.trading_strategy import TradingStrategy
app = Flask(__name__)

def configure_routes(app):
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        return response

    @app.route('/fetch_market_data', methods=['POST', 'OPTIONS'])
    def fetch_market_data():
        if request.method == 'OPTIONS':
            return jsonify({}), 200
            
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            symbol = data.get('symbol')
            end_date = data.get('end_date')
            start_date = '2021-01-01'

            if not symbol or not end_date:
                return jsonify({'error': 'Symbol and end_date are required.'}), 400

            market_data = MarketDataAdapter(symbol, start_date, end_date)
            data_df = market_data.fetch_data()
            market_data_json = data_df.to_dict(orient='records')

            return jsonify({
                'status': 'success',
                'data': market_data_json,
                'trade_log': [],
                'final_balance': 100000
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/run_backtest', methods=['POST'])
    def run_backtest():
        data = request.get_json()
        symbol = data.get('symbol')
        end_date = data.get('end_date')
        algorithm = data.get('algorithm')
        start_date = '2021-01-01'

        if not symbol or not end_date or not algorithm:
            return jsonify({'error': 'Symbol, end_date, and algorithm are required.'}), 400

        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            if end_dt < start_dt:
                return jsonify({'error': 'end_date must be after start_date.'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        try:
            # Fetch market data
            market_data = MarketDataAdapter(symbol, start_date, end_date)
            data_df = market_data.fetch_data()

            # Run backtest
            strategy = TradingStrategy(data_df, symbol, algorithm)
            final_balance, trade_log, total_gain_loss, annual_return, total_return = strategy.run_backtest()

            response = {
                'status': 'success',
                'trade_log': trade_log,
                'final_balance': final_balance,
                'total_gain_loss': total_gain_loss,
                'annual_return': annual_return,
                'total_return': total_return
            }
            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/get_last_closing_price', methods=['POST'])
    def get_last_closing_price():
        try:
            data = request.get_json()
            symbol = data.get('symbol')
            
            if not symbol:
                return jsonify({'error': 'Symbol is required.'}), 400

            # Create MarketData instance with today's date
            today = datetime.now().strftime('%Y-%m-%d')
            market_data = MarketDataAdapter(symbol, '2021-01-01', today)
            
            # Fetch the data and get the last closing price
            data_df = market_data.fetch_data()
            last_close = data_df['Close'].iloc[-1]

            return jsonify({
                'status': 'success',
                'price': float(last_close)
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500
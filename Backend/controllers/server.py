from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from models.market_data import MarketData
from models.trading_strategy import TradingStrategy

app = Flask(__name__)
CORS(app)


def configure_routes(app):
    @app.route('/fetch_market_data', methods=['POST'])
    def fetch_market_data():
        data = request.get_json()
        symbol = data.get('symbol')
        end_date = data.get('end_date')
        start_date = '2021-01-01'

    # Validate symbol and end_date
        if not symbol or not end_date:
            return jsonify({'error': 'Symbol and end_date are required.'}), 400

        # Validate date format and ensure end_date is after start_date
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            if end_dt < start_dt:
                return jsonify({'error': 'end_date must be after start_date.'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        try:
            market_data = MarketData(symbol, start_date, end_date)
            data_df = market_data.fetch_data()
            market_data_json = data_df.to_dict(orient='records')

            response = {'status': 'success', 'data': market_data_json}
            return jsonify(response), 200
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
            market_data = MarketData(symbol, start_date, end_date)
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

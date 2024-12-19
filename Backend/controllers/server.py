from datetime import datetime
from flask import request, jsonify

from data_access.models.market_data_adapter import MarketDataAdapter
from data_access.models.trading_strategy import TradingStrategy
from data_access.price_subscriber import price_subscriber

def configure_routes(app):
    @app.route('/fetch_market_data', methods=['POST'])
    def fetch_market_data():
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

    def price_update_callback(symbol: str, price: float):
        print(f"Price update for {symbol}: ${price:.2f}")
        # Here you could emit the price via websocket if needed
    
    @app.route('/get_last_closing_price', methods=['POST'])
    def get_last_closing_price():
        try:
            data = request.get_json()
            symbol = data.get('symbol')
            
            if not symbol:
                return jsonify({'error': 'Symbol is required.'}), 400

            from data_access.simulate_market_price import price_simulator
            
            # Subscribe to price updates
            price_subscriber.symbol = symbol
            price_subscriber.subscribe(price_update_callback)
            
            # Get initial price
            price = price_simulator.get_last_closing_price(symbol)
            print(f"Initial price for {symbol}: ${price:.2f}")

            return jsonify({
                'status': 'success',
                'price': float(price)
            })

        except Exception as e:
            print(f"Error in get_last_closing_price: {str(e)}")
            return jsonify({'error': str(e)}), 500
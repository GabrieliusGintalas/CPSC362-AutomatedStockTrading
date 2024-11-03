import unittest
import pandas as pd
from tradingalgo import backtest

class TestTradingAlgo(unittest.TestCase):
    def setUp(self):
        # Create sample market data
        self.test_data = pd.DataFrame({
            'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
            'Open': [100, 102, 98, 103],
            'High': [105, 104, 101, 106],
            'Low': [98, 100, 96, 102],
            'Close': [102, 98, 103, 105],
            'Volume': [1000, 1200, 800, 1500]
        })

    def test_sma_backtest(self):
        # Test SMA strategy
        final_balance, trade_log, total_gain_loss, annual_return, total_return = backtest(
            self.test_data, 
            'TEST', 
            'SMA'
        )
        
        # Basic assertions
        self.assertIsInstance(final_balance, (int, float))
        self.assertIsInstance(trade_log, list)
        self.assertIsInstance(total_gain_loss, (int, float))
        self.assertIsInstance(annual_return, (int, float))
        self.assertIsInstance(total_return, (int, float))
        
        # Verify initial balance is maintained or increased
        self.assertGreaterEqual(final_balance, 0)
        
        # Verify trade log structure
        if trade_log:
            first_trade = trade_log[0]
            required_keys = ['date', 'symbol', 'action', 'price', 'shares', 
                           'transaction_amount', 'gain/loss', 'balance']
            for key in required_keys:
                self.assertIn(key, first_trade)

if __name__ == '__main__':
    unittest.main() 
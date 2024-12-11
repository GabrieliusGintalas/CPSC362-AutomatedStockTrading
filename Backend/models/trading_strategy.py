import pandas as pd
import numpy as np
import csv
from models.strategy.trading_strategy_interface import SMAStrategy, BollingerBandsStrategy, MACDStrategy

class TradingStrategy:
    INITIAL_BALANCE = 100000

    def __init__(self, data, symbol, algorithm):
        self.data = data
        self.symbol = symbol
        self.algorithm = algorithm
        self.balance = self.INITIAL_BALANCE
        self.shares = 0
        self.trade_log = []
        self.total_gain_loss = 0
        self.annual_return = 0
        self.total_return = 0

    def calculate_signals(self):
        """
        Calculate signals based on the selected algorithm.
        """
        if self.algorithm == 'SMA':
            strategy = SMAStrategy()
        elif self.algorithm == 'BollingerBands':
            strategy = BollingerBandsStrategy()
        elif self.algorithm == 'MACD':
            strategy = MACDStrategy()
        else:
            raise ValueError("Invalid algorithm. Choose 'SMA', 'BollingerBands', or 'MACD'.")
        
        self.data = strategy.calculate_signals(self.data)

    def run_backtest(self):
        """
        Backtest a trading strategy based on the selected algorithm.
        """
        self.calculate_signals()

        for i in range(len(self.data)):
            price = self.data['Close'].iloc[i]
            signal = self.data['signal'].iloc[i]
            date = pd.to_datetime(self.data['Date'].iloc[i]).strftime('%m/%d/%Y')

            # Buy signal
            if signal == 1 and self.shares == 0:
                self.shares = self.balance // price
                transaction_amount = self.shares * price
                self.balance -= transaction_amount
                self.trade_log.append({
                    'date': date,
                    'symbol': self.symbol,
                    'action': 'BUY',
                    'price': price,
                    'shares': self.shares,
                    'transaction_amount': transaction_amount,
                    'gain/loss': None,
                    'balance': self.balance
                })

            # Sell signal
            elif signal == -1 and self.shares > 0:
                transaction_amount = self.shares * price
                gain_loss = transaction_amount - (self.shares * self.trade_log[-1]['price'])
                self.balance += transaction_amount
                self.trade_log.append({
                    'date': date,
                    'symbol': self.symbol,
                    'action': 'SELL',
                    'price': price,
                    'shares': self.shares,
                    'transaction_amount': transaction_amount,
                    'gain/loss': gain_loss,
                    'balance': self.balance
                })
                self.shares = 0  # Reset shares after selling

        # Final sell if shares remain
        if self.shares > 0:
            price = self.data['Close'].iloc[-1]
            transaction_amount = self.shares * price
            gain_loss = transaction_amount - (self.shares * self.trade_log[-1]['price'])
            self.balance += transaction_amount
            date = pd.to_datetime(self.data['Date'].iloc[-1]).strftime('%m/%d/%Y')
            self.trade_log.append({
                'date': date,
                'symbol': self.symbol,
                'action': 'SELL',
                'price': price,
                'shares': self.shares,
                'transaction_amount': transaction_amount,
                'gain/loss': gain_loss,
                'balance': self.balance
            })
            self.shares = 0

        self.total_gain_loss = sum(trade['gain/loss'] for trade in self.trade_log if trade['gain/loss'] is not None)
        start_date = pd.to_datetime(self.data['Date'].iloc[0])
        end_date = pd.to_datetime(self.data['Date'].iloc[-1])
        total_days = (end_date - start_date).days
        total_years = total_days / 365.25
        self.total_return = (self.balance / self.INITIAL_BALANCE - 1) * 100
        self.annual_return = ((self.balance / self.INITIAL_BALANCE) ** (1 / total_years) - 1) * 100 if total_years > 0 else 0

        return self.balance, self.trade_log, self.total_gain_loss, self.annual_return, self.total_return

    def save_trades_to_csv(self):
        filename = f"{self.symbol}_{self.algorithm}_trades.csv"
        fieldnames = [
            'date', 'symbol', 'action', 'price', 'shares',
            'transaction_amount', 'gain/loss', 'balance'
        ]
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for trade in self.trade_log:
                writer.writerow(trade)
            summary_writer = csv.writer(file)
            summary_writer.writerow([f"Total Gain/Loss: {self.total_gain_loss:.2f} | Final Balance: {self.balance:.2f}"])

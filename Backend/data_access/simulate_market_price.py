from data_access.models.market_data_adapter import MarketDataAdapter
import random

class MarketPriceSimulator:
    def __init__(self):
        self._last_prices = {}  # Cache for storing last prices per symbol
        self._base_prices = {}  # Store the initial closing prices

    def get_last_closing_price(self, symbol):
        # If we don't have a base price, get it once from the adapter
        if symbol not in self._base_prices:
            market_data = MarketDataAdapter(symbol, None, None)
            price = market_data.live_price()  # Get initial price
            self._base_prices[symbol] = price
            self._last_prices[symbol] = price
            return price
        
        # If we already have a price, return the simulated one
        return self.simulate_price(symbol)

    def simulate_price(self, symbol):
        if symbol not in self._last_prices:
            return self.get_last_closing_price(symbol)
        
        # Simulate price movement of ±0.01%
        change_percent = (random.random() - 0.5) * 0.0005  # Generate number between -0.01% and +0.01%
        new_price = self._last_prices[symbol] * (1 + change_percent)
        self._last_prices[symbol] = new_price
        
        return new_price

# Create a global instance
price_simulator = MarketPriceSimulator()
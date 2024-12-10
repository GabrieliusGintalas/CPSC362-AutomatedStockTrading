from data_access.data_access_service import DataAccessService
from data_access.yahoo_finance_adapter import YahooFinanceAdapter
from data_access.decorators.validation_decorator import ValidationDecorator

class MarketData:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        
        # Create base data source with decorators
        base_source = YahooFinanceAdapter()
        validated_source = ValidationDecorator(base_source)
        self.data_service = DataAccessService(validated_source)

    def fetch_data(self):
        """Fetch market data using the decorated data access service"""
        return self.data_service.get_market_data(
            self.symbol,
            self.start_date,
            self.end_date
        )

    def save_data(self):
        """Save current market data"""
        if hasattr(self, 'data') and self.data is not None:
            self.data_service.save_market_data(self.data, self.symbol)

    def load_data(self):
        """Load saved market data"""
        return self.data_service.load_market_data(self.symbol)
    
    def live_price(self):
        """Fetch live price using the decorated data access service"""
        return self.data_service.get_live_price(self.symbol)

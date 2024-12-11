class PriceSubscriber:
    def __init__(self, symbol: str):
        self.symbol = symbol
        from data_access.price_publisher import price_publisher
        self.publisher = price_publisher
        
    def subscribe(self, callback):
        """Subscribe to price updates for the symbol"""
        self.publisher.subscribe(self.symbol, callback)
        
    def unsubscribe(self, callback):
        """Unsubscribe from price updates for the symbol"""
        self.publisher.unsubscribe(self.symbol, callback)

# Create a global instance
price_subscriber = PriceSubscriber(None) 
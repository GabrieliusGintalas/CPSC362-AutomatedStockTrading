from typing import Dict, List, Callable

class PricePublisher:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PricePublisher, cls).__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[str, float], None]]] = {}
    
    def subscribe(self, symbol: str, callback: Callable[[str, float], None]):
        if symbol not in self._subscribers:
            self._subscribers[symbol] = []
        self._subscribers[symbol].append(callback)
    
    def unsubscribe(self, symbol: str, callback: Callable[[str, float], None]):
        if symbol in self._subscribers and callback in self._subscribers[symbol]:
            self._subscribers[symbol].remove(callback)
    
    def notify(self, symbol: str, price: float):
        if symbol in self._subscribers:
            for callback in self._subscribers[symbol]:
                callback(symbol, price)

# Create a global instance
price_publisher = PricePublisher() 
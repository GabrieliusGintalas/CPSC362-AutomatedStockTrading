# Automated Stock Trading System

## Setup Instructions
1. How to start frontend
- cd trading-website
- npm start

2. How to start backend
- cd flask-server
- python3 -m venv .venv 
- source .venv/bin/activate
- pip install flask yfinance
- python3 server.py

Or simply run:
- ./run.sh (auto setup for all the front end and back-end code and ran locally)

## Design Patterns Implementation

### 1. Adapter Pattern
Location: `/Backend/data_access/`
- `models/market_data_adapter.py`: Main adapter class that converts data source interfaces
- `data_adaptees/yahoo_finance_adaptee.py`: Concrete adaptee for Yahoo Finance
- `data_source_interface.py`: Interface that defines data access methods

### 2. Decorator Pattern
Location: `/Backend/data_access/decorators/`
- `market_data_decorator.py`: Base decorator class
- `validation_decorator.py`: Adds data validation
- `caching_decorator.py`: Adds caching functionality

### 3. Strategy Pattern
Location: `/Backend/data_access/models/strategy_pattern/`
- `tradingAlgos.py`: Contains different trading strategy implementations (SMA, MACD, Bollinger Bands)

### 4. Publisher-Subscriber Pattern
Location: `/Backend/data_access/`
- `price_publisher.py`: Manages price update subscriptions
- `simulate_market_price.py`: Simulates price changes
- `price_subscriber.py`: Handles price update subscriptions

## SOLID Principles Implementation

### 1. Single Responsibility Principle (SRP)
Location: `/Backend/data_access/models/strategy_pattern/tradingAlgos.py`
- Each trading algorithm class has a single responsibility
- Example: SMAStrategy only handles SMA calculations and signals
- TradingAlgo base class defines a single interface for calculating signals

### 2. Open-Closed Principle (OCP)
Location: `/Backend/data_access/decorators/market_data_decorator.py`
- MarketDataDecorator allows extending functionality without modifying existing code
- New decorators can be added by inheriting from the base decorator class
- Example: ValidationDecorator and CachingDecorator extend functionality without changing base code

### 3. Liskov Substitution Principle (LSP)
Location: `/Backend/data_access/models/strategy_pattern/tradingAlgos.py`
- All strategy classes (SMA, BollingerBands, MACD) can be used interchangeably
- Each maintains the contract defined by TradingAlgo base class
- Example: TradingStrategy can use any algorithm that implements TradingAlgo interface

### 4. Interface Segregation Principle (ISP)
Location: `/Backend/data_access/models/market_data_adapter.py`
- MarketDataAdapter implements only the methods it needs
- Each method has a specific purpose without unnecessary dependencies
- Separate interfaces for different functionalities (data fetching, live prices)

### 5. Dependency Inversion Principle (DIP)
Location: `/Backend/data_access/models/trading_strategy.py`
- TradingStrategy depends on abstractions (strategy interfaces)
- Strategy selection is done through dependency injection
- Data access layer uses interfaces instead of concrete implementations

The most complete example of all SOLID principles working together can be found in the data access layer:

## Architecture
The system follows MVC architecture:
- Model: Trading algorithms and data access layer
- View: React frontend components
- Controller: Flask server endpoints

## Testing
Run tests using:
./runtests.sh

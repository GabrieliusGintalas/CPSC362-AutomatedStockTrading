#!/bin/bash

# Exit on any error
set -e

echo "Setting up test environment..."

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install flask flask_cors yfinance pytest pandas numpy

# Run the tests
echo "Running unit tests..."
cd flask-server
python -m pytest test_trading_algo.py -v

echo "Running integration tests..."
python -m pytest test_server_integration.py -v

# Deactivate virtual environment
deactivate

echo "Testing completed!"

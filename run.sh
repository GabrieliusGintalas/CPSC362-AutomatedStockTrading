#!/bin/bash

if [ ! -d "myenv" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv myenv
else
    echo "Virtual environment already exists."
fi
echo "Activating virtual environment..."
source myenv/bin/activate
echo "Python version in virtual environment: $(python3 --version)"
if ! python3 -c "import yfinance, matplotlib, pandas" &> /dev/null; then
    echo "Installing required packages..."
    pip install yfinance matplotlib pymongo pandas
else
    echo "Required packages are already installed."
fi
echo "Running the main Python script..."
python3 main.py
python3 --version
echo "Deactivating virtual environment..."
deactivate

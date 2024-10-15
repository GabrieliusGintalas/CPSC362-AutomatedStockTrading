#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "myenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv myenv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source myenv/bin/activate

# Install required packages if not already installed
if ! python3 -c "import yfinance, matplotlib, pandas" &> /dev/null; then
    echo "Installing required packages..."
    pip install yfinance matplotlib pymongo pandas
else
    echo "Required packages are already installed."
fi

# Run the main Python script
echo "Running the main Python script..."
python3 main.py

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate




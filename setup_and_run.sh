#!/bin/bash

# Set up the custom MongoDB data directory
MONGO_DATA_DIR=~/CPSC362-AutomatedStockTrading/data
MONGO_LOG=~/CPSC362-AutomatedStockTrading/mongodb.log

# Create the data directory if it doesn't exist
if [ ! -d "$MONGO_DATA_DIR" ]; then
    echo "Creating MongoDB data directory..."
    mkdir -p $MONGO_DATA_DIR
fi

# Always stop any running system-wide MongoDB service to avoid conflicts
if systemctl is-active --quiet mongod; then
    echo "Stopping system-wide MongoDB service to avoid conflicts..."
    sudo systemctl stop mongod
fi

# Check if MongoDB is already running with the custom dbPath. If not, start it.
if ! pgrep mongod > /dev/null; then
    echo "Starting MongoDB with custom data directory..."
    mongod --dbpath $MONGO_DATA_DIR --fork --logpath $MONGO_LOG
else
    echo "MongoDB is already running with custom dbPath."
fi

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
if ! python3 -c "import yfinance" &> /dev/null; then
    echo "Installing required packages..."
    pip install yfinance pymongo
else
    echo "Required packages are already installed."
fi

# Run the main Python script
echo "Running the main Python script..."
python3 main.py

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

# Stop MongoDB after the script completes
echo "Stopping MongoDB..."
mongod --shutdown --dbpath $MONGO_DATA_DIR




#!/bin/bash

# Exit on any error
set -e

echo "Setting up test environment..."

# Navigate to your_project directory
cd ../Backend || { echo "Failed to navigate to Backend directory"; exit 1; }

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run the tests
echo "Running unit tests..."
python -m unittest discover tests -v

# Deactivate virtual environment
deactivate

echo "Testing completed!"


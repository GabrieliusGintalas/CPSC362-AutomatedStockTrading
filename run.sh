#!/bin/bash

# Kill any existing processes on port 3000 and 5000
echo "Cleaning up existing processes..."
taskkill /F /IM python.exe /T 2>nul || true
taskkill /F /IM node.exe /T 2>nul || true

# Start the backend first
echo "Starting the backend..."
cd Backend || { echo "Failed to navigate to Backend directory"; exit 1; }

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install required packages from Backend directory
echo "Installing required packages..."
pip install -r requirements.txt

# Start the Flask app from Backend directory
python app.py &
backend_pid=$!

# Wait for backend to start
sleep 5

# Start the frontend
echo "Starting the frontend..."
cd ../trading-website || { echo "Failed to navigate to trading-website directory"; exit 1; }
npm install
npm start &
frontend_pid=$!

# Function to handle script termination and cleanup
cleanup() {
    echo "Stopping the frontend and backend..."
    taskkill /F /PID $frontend_pid 2>nul || true
    taskkill /F /PID $backend_pid 2>nul || true
    deactivate
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup INT

# Wait for both processes to end
wait $frontend_pid $backend_pid


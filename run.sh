#!/bin/bash

# Kill any existing processes on port 3000 and 5000
echo "Cleaning up existing processes..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:5000 | xargs kill -9 2>/dev/null || true

# Start the frontend
echo "Starting the frontend..."
cd trading-website || { echo "Failed to navigate to trading-website directory"; exit 1; }
npm install
npm start &
frontend_pid=$!


# Wait for frontend to start
sleep 5

# Start the backend
echo "Starting the backend..."
cd ../Backend || { echo "Failed to navigate to Backend directory"; exit 1; }

# Create and activate virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Start the Flask app
python3 app.py &
backend_pid=$!

# Function to handle script termination and cleanup
cleanup() {
  echo "Stopping the frontend and backend..."
  kill $frontend_pid
  kill $backend_pid
  deactivate
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup INT

# Wait for both processes to end
wait $frontend_pid $backend_pid


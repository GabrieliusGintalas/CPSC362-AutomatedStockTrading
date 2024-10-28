#!/bin/bash

# Start the frontend
echo "Starting the frontend..."
cd trading-website || { echo "Failed to navigate to trading-website directory"; exit 1; }
npm start &
frontend_pid=$!

# Wait for frontend to start
sleep 5

# Start the backend
echo "Starting the backend..."
cd ../flask-server || { echo "Failed to navigate to flask-server directory"; exit 1; }
python3 -m venv .venv
source .venv/bin/activate
pip install flask flask_cors yfinance
python3 server.py &
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

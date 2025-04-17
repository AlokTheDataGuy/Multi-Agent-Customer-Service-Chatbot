#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if we need to build the frontend
if [ "$1" == "build" ]; then
    echo "Building frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
fi

# Start the backend and frontend servers
if [ "$1" == "backend" ] || [ "$2" == "backend" ]; then
    echo "Starting backend server..."
    cd backend
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
fi

if [ "$1" == "frontend" ] || [ "$2" == "frontend" ]; then
    echo "Starting frontend server..."
    cd frontend
    npm run dev
fi

# If no specific service is specified, start both
if [ "$1" != "backend" ] && [ "$1" != "frontend" ] && [ "$1" != "build" ] && [ "$2" != "backend" ] && [ "$2" != "frontend" ]; then
    echo "Starting both backend and frontend servers..."

    # Start backend in background
    cd backend
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..

    # Start frontend
    cd frontend
    npm run dev

    # Kill backend when frontend is stopped
    kill $BACKEND_PID
fi
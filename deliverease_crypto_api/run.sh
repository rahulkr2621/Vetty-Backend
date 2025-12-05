#!/bin/bash
# Start script for development environment

set -e

echo "Starting Deliverease Crypto API Development Environment..."

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please update .env with your settings"
fi

# Run application
echo "Starting API server..."
echo "API will be available at http://localhost:8000"
echo "API Docs at http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

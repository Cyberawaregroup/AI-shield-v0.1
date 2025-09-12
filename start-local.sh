#!/bin/bash

# Threat Intelligence Platform Local Startup Script
echo "🚀 Starting Threat Intelligence Platform (Local Mode)..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ and try again."
    echo "📥 Download from: https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    echo "📥 Download from: https://nodejs.org/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "📝 Please edit .env file with your API keys before continuing."
        echo "🔑 Required keys: OPENAI_API_KEY, HIBP_API_KEY, ABUSEIPDB_API_KEY"
        echo "⚠️  For now, you can leave them empty to test basic functionality."
        read -p "Press Enter to continue..."
    else
        echo "❌ env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs uploads

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "📦 Installing Python packages..."
pip install -r requirements-local.txt
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Start the backend (in background)
echo "🚀 Starting FastAPI backend..."
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start the frontend
echo "🚀 Starting React frontend..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 Threat Intelligence Platform is starting up!"
echo ""
echo "📱 Frontend: http://localhost:5173 (or 3000)"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "  Stop backend: kill $BACKEND_PID"
echo "  Stop frontend: kill $FRONTEND_PID"
echo "  Stop all: pkill -f 'uvicorn\|npm'"
echo ""
echo "🔍 If you see errors:"
echo "  - Check that ports 8000 and 5173 are not in use"
echo "  - Make sure Python 3.11+ and Node.js 18+ are installed"
echo "  - Check the terminal for error messages"
echo ""
echo "Happy threat hunting! 🛡️"

# Wait for user to stop
echo "Press Ctrl+C to stop all services..."
wait

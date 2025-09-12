#!/bin/bash
# Frontend Chatbot Integration Setup Script

echo "🚀 Setting up Frontend Chatbot Integration"
echo "=========================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are available"

# Install dependencies
echo "📦 Installing frontend dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/healthz > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "⚠️  Backend is not running. Please start the backend first:"
    echo "   cd backend && python main.py"
    echo ""
    echo "   Or use the startup scripts:"
    echo "   ./start-local.sh"
    echo "   ./start-local.bat (Windows)"
fi

echo ""
echo "🎉 Frontend setup complete!"
echo ""
echo "To start the frontend development server:"
echo "  npm run dev"
echo ""
echo "The chatbot will be available at:"
echo "  http://localhost:5173"
echo ""
echo "Demo credentials:"
echo "  Email: demo@example.com"
echo "  Password: demo123"
echo ""
echo "Features available:"
echo "  ✅ Real-time AI chatbot powered by HuggingFace"
echo "  ✅ Cybersecurity-focused responses"
echo "  ✅ Session management and chat history"
echo "  ✅ Authentication system"
echo "  ✅ Error handling and loading states"
echo "  ✅ AI confidence scores and metadata display"

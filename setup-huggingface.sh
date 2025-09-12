#!/bin/bash
# Setup script for HuggingFace chatbot integration

echo "🤖 Setting up HuggingFace Chatbot Integration"
echo "============================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

# Update .env with HF token
echo "🔑 Setting HuggingFace token..."
if grep -q "HF_TOKEN=" .env; then
    sed -i 's/HF_TOKEN=.*/HF_TOKEN=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/' .env
    echo "✅ HF_TOKEN updated in .env"
else
    echo "HF_TOKEN=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" >> .env
    echo "✅ HF_TOKEN added to .env"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Test the integration
echo "🧪 Testing chatbot integration..."
cd ..
python test_chatbot.py

echo ""
echo "🎉 Setup complete! Your chatbot is now using HuggingFace GPT-OSS models."
echo ""
echo "To start the application:"
echo "  cd backend && python main.py"
echo ""
echo "Or use the provided startup scripts:"
echo "  ./start-local.sh"
echo "  ./start-local.bat (Windows)"

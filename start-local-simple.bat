@echo off
chcp 65001 >nul
echo 🚀 Starting Threat Intelligence Platform (Local Mode - Simple)...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.11+ and try again.
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ and try again.
    echo 📥 Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from template...
    if exist env.example (
        copy env.example .env >nul
        echo 📝 Please edit .env file with your API keys before continuing.
        echo 🔑 Required keys: OPENAI_API_KEY, HIBP_API_KEY, ABUSEIPDB_API_KEY
        echo ⚠️  For now, you can leave them empty to test basic functionality.
        pause
    ) else (
        echo ❌ env.example not found. Please create .env file manually.
        pause
        exit /b 1
    )
)

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist logs mkdir logs
if not exist uploads mkdir uploads

REM Install Python dependencies
echo 🐍 Installing Python dependencies...
cd backend
if not exist venv (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

echo 📦 Installing Python packages (using pre-compiled wheels)...
echo 🔧 This may take a few minutes on first run...
pip install --upgrade pip
pip install --only-binary=all fastapi uvicorn[standard] pydantic pydantic-settings sqlmodel httpx aiofiles python-dotenv python-multipart

cd ..

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install

REM Start the backend (in background)
echo 🚀 Starting FastAPI backend...
start "Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a moment for backend to start
echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start the frontend
echo 🚀 Starting React frontend...
start "Frontend" cmd /k "npm run dev"

echo.
echo 🎉 Threat Intelligence Platform is starting up!
echo.
echo 📱 Frontend: http://localhost:5173 (or 3000)
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 📋 Useful commands:
echo   Stop backend: Close the "Backend" command window
echo   Stop frontend: Close the "Frontend" command window
echo   View backend logs: Check the Backend command window
echo   View frontend logs: Check the Frontend command window
echo.
echo 🔍 If you see errors:
echo   - Check that ports 8000 and 5173 are not in use
echo   - Make sure Python 3.11+ and Node.js 18+ are installed
echo   - Check the command windows for error messages
echo.
echo Happy threat hunting! 🛡️
pause

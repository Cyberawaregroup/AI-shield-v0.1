@echo off
chcp 65001 >nul
echo 🚀 Starting Threat Intelligence Platform...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install it and try again.
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

REM Start services
echo 🐳 Starting services with Docker Compose...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 30 /nobreak >nul

REM Check service health
echo 🔍 Checking service health...
curl -f http://localhost:8000/healthz >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is healthy!
) else (
    echo ❌ Backend health check failed. Check logs with: docker-compose logs backend
)

curl -f http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend is running!
) else (
    echo ❌ Frontend health check failed. Check logs with: docker-compose logs frontend
)

echo.
echo 🎉 Threat Intelligence Platform is starting up!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 💾 Database: localhost:5432
echo 🔴 Redis: localhost:6379
echo.
echo 📋 Useful commands:
echo   View logs: docker-compose logs -f
echo   Stop services: docker-compose down
echo   Restart: docker-compose restart
echo   Rebuild: docker-compose up --build -d
echo.
echo 🔍 Check logs for any errors:
echo   docker-compose logs backend
echo   docker-compose logs frontend
echo   docker-compose logs postgres
echo.
echo Happy threat hunting! 🛡️
pause

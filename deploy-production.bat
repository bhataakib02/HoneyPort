@echo off
echo.
echo 🛡️  AetherionBot Production Deployment
echo ======================================
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please configure .env file with your credentials
    echo    1. Edit .env file with your Telegram bot token and chat ID
    echo    2. Configure other environment variables as needed
    echo    3. Run this script again after configuration
    echo.
    echo Press Enter after configuring .env file...
    pause
)

echo 🔨 Building Docker images...
echo.

REM Build all services
docker-compose build --no-cache
if %errorlevel% neq 0 (
    echo ❌ Docker build failed. Check error messages above.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting AetherionBot services...
echo.

REM Start services
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ Failed to start services. Check error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ AetherionBot deployed successfully!
echo.

REM Wait for services to start
echo ⏳ Waiting for services to initialize...
timeout /t 10 /nobreak >nul

REM Show service status
echo.
echo 📊 Service Status:
docker-compose ps

echo.
echo 🎯 Access Your AetherionBot:
echo    🎨 Dashboard:  http://localhost:5173
echo    📚 API Docs:   http://localhost:8001/docs  
echo    🛡️ Honeypot:   Port 2222
echo.

echo 🔧 Management Commands:
echo    View logs:     docker-compose logs -f
echo    Stop all:      docker-compose down
echo    Restart:       docker-compose restart
echo    Update:        docker-compose pull ^&^& docker-compose up -d
echo.

echo 🛡️ Security Recommendations:
echo    ✅ Change default ports in production
echo    ✅ Configure SSL/HTTPS certificates
echo    ✅ Set up firewall rules
echo    ✅ Monitor logs regularly
echo    ✅ Update Docker images regularly
echo.

echo Press Enter to show recent logs or Ctrl+C to exit...
pause >nul

echo.
echo 📋 Recent logs:
docker-compose logs --tail=50

pause

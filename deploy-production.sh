#!/bin/bash

echo "🛡️  AetherionBot Production Deployment"
echo "======================================"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
   	exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo ""
    warning_msg="⚠️  IMPORTANT: Please configure .env file with your credentials"
    
    # Create the warning message with color and formatting
    printf "\033[33m%s\033[0m\n" "$warning_msg"
    echo "   1. Edit .env file with your Telegram bot token and chat ID"
    echo "   2. Configure other environment variables as needed"
    echo "   3. Run this script again after configuration"
    echo ""
    
    # Make .env file editable
    chmod 644 .env
    
    echo "Press Enter after configuring .env file..."
    read -r
fi

echo "🔨 Building Docker images..."
echo ""

# Build all services
docker-compose build --no-cache

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed. Check error messages above."
    exit 1
fi

echo ""
echo "🚀 Starting AetherionBot services..."
echo ""

# Start services
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services. Check error messages above."
    exit 1
fi

echo ""
echo "✅ AetherionBot deployed successfully!"
echo ""

# Wait a few seconds for services to fully start
echo "⏳ Waiting for services to initialize..."
sleep 10

# Show service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎯 Access Your AetherionBot:"
echo "   🎨 Dashboard:  http://localhost:5173"
echo "   📚 API Docs:   http://localhost:8001/docs"
echo "   🛡️ Honeypot:   Port 2222"
echo ""

echo "🔧 Management Commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop all:      docker-compose down"
echo "   Restart:       docker-compose restart"
echo "   Update:        docker-compose pull && docker-compose up -d"
echo ""

echo "🛡️ Security Recommendations:"
echo "   ✅ Change default ports in production"
echo "   ✅ Configure SSL/HTTPS certificates"
echo "   ✅ Set up firewall rules"
echo "   ✅ Monitor logs regularly"
echo "   ✅ Update Docker images regularly"
echo ""

read -p "Press Enter to show recent logs (Ctrl+C to exit)..."
echo ""
echo "📋 Recent logs:"
docker-compose logs --tail=50

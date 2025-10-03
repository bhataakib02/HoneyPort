#!/bin/bash

# AIML Honeypot Deployment Script
# Industrial-grade AI/ML honeypot with real-time monitoring

echo "🚀 AIML Honeypot Deployment Script"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your Telegram bot token and chat ID"
    echo "   1. Get bot token from https://t.me/BotFather"
    echo "   2. Get chat ID by messaging your bot and checking logs"
    echo "   3. Update the .env file with your credentials"
    echo ""
fi

# Build Docker images
echo "🔨 Building Docker images..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Failed to build Docker images"
    exit 1
fi

echo "✅ Docker images built successfully"
echo ""

# Start services
echo "🚀 Starting AIML Honeypot services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services"
    exit 1
fi

echo "✅ Services started successfully"
echo ""

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Checking service status..."
docker-compose ps

echo ""
echo "🎉 AIML Honeypot deployed successfully!"
echo ""
echo "📱 Service URLs:"
echo "   🖥️  Dashboard:  http://localhost:5173"
echo "   🔌 Honeypot:   localhost:2222"
echo "   🤖 Backend API: http://localhost:8000"
echo "   📚 API Docs:    http://localhost:8000/docs"
echo ""
echo "🧪 Test the honeypot:"
echo "   nc localhost 2222"
echo "   echo 'ls -la' | nc localhost 2222"
echo "   ssh -p 2222 test@localhost"
echo ""
echo "📈 Monitor threats:"
echo "   Watch the dashboard at http://localhost:5173"
echo "   Check Telegram for real-time alerts"
echo ""
echo "🔧 Management commands:"
echo "   docker-compose logs -f         # View all logs"
echo "   docker-compose logs -f honeypot # View honeypot logs"
echo "   docker-compose restart         # Restart all services"
echo "   docker-compose down            # Stop all services"
echo ""




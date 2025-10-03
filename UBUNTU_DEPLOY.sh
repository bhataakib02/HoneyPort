#!/bin/bash

echo "🛡️ AetherionSecBot Ubuntu Deployment"
echo "===================================="
echo ""

# Your Telegram Configuration
TELEGRAM_BOT_TOKEN="8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds"
TELEGRAM_CHAT_ID="6433268037"

echo "🤖 Bot: t.me/AetherionSecBot"
echo "📱 Chat ID: $TELEGRAM_CHAT_ID"
echo ""

# Update system
sudo apt update && sudo apt install curl git docker.io docker-compose -y

# Configure Docker
sudo usermod -aG docker $USER

# Clone repository (remove existing if present)
if [ -d "HoneyPort" ]; then
    echo "📁 Removing existing HoneyPort directory..."
    rm -rf HoneyPort
fi
git clone https://github.com/bhataakib02/HoneyPort.git && cd HoneyPort

# Configure environment
echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" > .env
echo "TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID" >> .env

# Verify docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found in HoneyPort directory"
    echo "📁 Current directory contents:"
    ls -la
    exit 1
fi

# Deploy
echo "🔨 Building Docker containers..."
docker-compose build --no-cache
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services
sleep 20

# Test Telegram
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d "chat_id=$TELEGRAM_CHAT_ID" \
  -d "text=🛡️ *AetherionSecBot Deployed Successfully!*" \
  -d "parse_mode=Markdown" > /dev/null

# Show results
VM_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ AetherionSecBot deployed!"
echo "🎨 Dashboard: http://$VM_IP:5173"
echo "📚 API Docs: http://$VM_IP:8001/docs"
echo "🛡️ Honeypot: ssh user@$VM_IP -p 2222"
echo "📱 Telegram: t.me/AetherionSecBot"
echo ""

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

# Clone repository
git clone https://github.com/bhataakib02/HoneyPort.git && cd HoneyPort

# Configure environment
echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" > .env
echo "TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID" >> .env

# Deploy
docker-compose build --no-cache && docker-compose up -d

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

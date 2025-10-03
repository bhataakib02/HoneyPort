#!/bin/bash

echo "🛡️ AetherionSecBot Complete Ubuntu Deployment"
echo "============================================="
echo ""

# Your Telegram Configuration
TELEGRAM_BOT_TOKEN="8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds"
TELEGRAM_CHAT_ID="6433268037"
BOT_USERNAME="t.me/AetherionSecBot"

echo "🤖 Bot Configuration:"
echo "   ✅ Bot Token: $TELEGRAM_BOT_TOKEN"
echo "   ✅ Chat ID: $TELEGRAM_CHAT_ID"
echo "   🎯 Bot Link: $BOT_USERNAME"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as sudo/root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Run as regular user with sudo privileges."
    exit 1
fi

print_status "Starting AetherionSecBot deployment on Ubuntu..."

# Step 1: Update system packages
print_status "Updating Ubuntu system packages..."
sudo apt update && sudo apt upgrade -y

if [ $? -ne 0 ]; then
    print_error "Failed to update system packages"
    exit 1
fi

print_success "System packages updated"

# Step 2: Install essential packages
print_status "Installing essential packages (curl, git)..."
sudo apt install -y curl git wget python3-pip

print_success "Essential packages installed"

# Step 3: Install Docker
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    
    # Install Docker using official method
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo rm get-docker.sh
    
    print_success "Docker installed successfully"
else
    print_status "Docker already installed: $(docker --version | cut -d' ' -f3 | cut -d',' -f1)"
fi

# Step 4: Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_status "Installing Docker Compose..."
    sudo apt install -y docker-compose
    print_success "Docker Compose installed"
else
    print_status "Docker Compose already installed: $(docker-compose --version | cut -d' ' -f3 | cut -d',' -f1)"
fi

# Step 5: Configure Docker permissions
print_status "Configuring Docker permissions..."
sudo usermod -aG docker $USER

if [ $? -eq 0 ]; then
    print_success "User added to docker group"
    print_warning "Note: You may need to logout/login for Docker permissions to take effect"
else
    print_error "Failed to add user to docker group"
fi

# Step 6: Clone repository (remove existing if present)
print_status "Cloning AetherionBot repository..."
if [ -d "HoneyPort" ]; then
    print_status "Removing existing HoneyPort directory..."
    rm -rf HoneyPort
fi

git clone https://github.com/bhataakib02/HoneyPort.git
if [ $? -ne 0 ]; then
    print_error "Failed to clone repository"
    exit 1
fi

cd HoneyPort
print_success "Repository cloned successfully"

# Step 7: Configure environment variables
print_status "Configuring environment with your Telegram credentials..."
cat > .env << EOF
# AetherionSecBot Configuration
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID

# Additional Configuration
VERCEL_TOKEN=$TELEGRAM_BOT_TOKEN
VERCEL_PROJECT_ID=fancy_honeypot
SECRET_KEY=aetherion-secret-key-2025
JWT_SECRET=aetherion-jwt-secret-2025
API_KEY=aetherion-api-key-updated
EOF

print_success "Environment configured with Telegram credentials"

# Step 8: Test Telegram connectivity
print_status "Testing Telegram bot connectivity..."
telegram_response=$(curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe")

if echo "$telegram_response" | grep -q '"ok":true'; then
    print_success "✅ Telegram bot is accessible and online"
    bot_name=$(echo "$telegram_response" | grep -o '"first_name":"[^"]*"' | cut -d'"' -f4)
    echo "   🤖 Bot Name: $bot_name"
else
    print_warning "⚠️ Could not verify Telegram bot connectivity"
fi

# Step 9: Build Docker containers
print_status "Building Docker containers for AetherionSecBot..."
docker-compose build --no-cache

if [ $? -ne 0 ]; then
    print_error "Docker build failed"
    exit 1
fi

print_success "Docker containers built successfully"

# Step 10: Start services
print_status "Starting AetherionSecBot services..."
docker-compose up -d

if [ $? -ne 0 ]; then
    print_error "Failed to start services"
    exit 1
fi

print_success "Services started successfully"

# Step 11: Wait for services to initialize
print_status "Waiting for services to initialize (30 seconds)..."
sleep 30

# Step 12: Get VM IP address
VM_IP=$(hostname -I | awk '{print $1}')
if [ -z "$VM_IP" ]; then
    VM_IP="localhost"
fi

# Step 13: Check service status
print_status "Checking service status..."
docker-compose ps

# Step 14: Test endpoints
print_status "Testing service endpoints..."

# Test API
if curl -s http://localhost:8001/stats > /dev/null; then
    print_success "✅ API endpoint responding"
else
    print_warning "⚠️ API endpoint not responding yet"
fi

# Test Dashboard
if curl -s -I http://localhost:5173 | grep -q "200 OK"; then
    print_success "✅ Dashboard endpoint responding"
else
    print_warning "⚠️ Dashboard endpoint not responding yet"
fi

# Test Telegram integration
print_status "Sending test message to your Telegram..."
test_message="🛡️ *AetherionSecBot is online!*\n\n✅ Deployment successful!\n📱 Dashboard: http://$VM_IP:5173\n📚 API Docs: http://$VM_IP:8001/docs\n🛡️ Honeypot: ssh user@$VM_IP -p 2222"

curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d "chat_id=$TELEGRAM_CHAT_ID" \
  -d "text=$test_message" \
  -d "parse_mode=Markdown" > /dev/null

if [ $? -eq 0 ]; then
    print_success "✅ Test message sent to Telegram successfully"
else
    print_warning "⚠️ Could not send test message to Telegram"
fi

# Step 15: Display success information
echo ""
echo "🎉 ================================================="
print_success "AetherionSecBot deployed successfully!"
echo "================================================="
echo ""
echo "🤖 TELEGRAM BOT:"
echo "   🎯 Bot URL: $BOT_USERNAME"
echo "   📱 Chat ID: $TELEGRAM_CHAT_ID"
echo "   💬 Send '/start' to begin"
echo ""
echo "🌐 WEB ACCESS:"
echo "   🎨 Dashboard: http://$VM_IP:5173"
echo "   📚 API Docs: http://$VM_IP:8001/docs"
echo "   🛡️ Honeypot: ssh user@$VM_IP -p 2222"
echo ""
echo "🔧 MANAGEMENT COMMANDS:"
echo "   📊 Status: docker-compose ps"
echo "   📋 Logs: docker-compose logs -f"
echo "   🔄 Restart: docker-compose restart"
echo "   🛑 Stop: docker-compose down"
echo ""

# Step 16: Show quick test commands
echo "🧪 TEST YOUR DEPLOYMENT:"
echo "📱 Test Telegram:"
echo "   curl -X POST \"https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage\" -d \"chat_id=$TELEGRAM_CHAT_ID\" -d \"text=🛡️ Test from AetherionSecBot!\""
echo ""
echo "🛡️ Test Honeypot:"
echo "   nc $VM_IP 2222"
echo "   ssh user@$VM_IP -p 2222"
echo ""

print_status "🚀 AetherionSecBot Cyber Deception Engine is ready!"
echo ""
echo "💡 Pro Tip: Use 'docker-compose logs -f' to monitor threat activity in real-time"
echo ""

read -p "Press Enter to view recent logs (Ctrl+C to exit)..."
echo ""
docker-compose logs --tail=20

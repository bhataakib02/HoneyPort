#!/bin/bash

echo "🛡️  AetherionBot Ubuntu VM Deployment Script"
echo "============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

print_status "Starting Ubuntu VM deployment for AetherionBot..."

# Step 1: Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential packages
print_status "Installing essential packages..."
sudo apt install -y git curl wget python3-pip

print_success "System packages updated"

# Step 2: Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo rm get-docker.sh
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    print_warning "Please logout and login again for Docker group permissions to take effect"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    print_status "Installing Docker Compose..."
    sudo apt install -y docker-compose
fi

# Verify Docker installation
if command -v docker &> /dev/null; then
    print_success "Docker $(docker --version | cut -d' ' -f3 | cut -d',' -f1) installed"
else
    print_error "Docker installation failed"
    exit 1
fi

# Step 3: Clone repository
if [ ! -d "HoneyPort" ]; then
    print_status "Cloning AetherionBot repository..."
    git clone https://github.com/bhataakib02/HoneyPort.git
else
    print_status "HoneyPort directory already exists, skipping clone"
fi

cd HoneyPort

# Step 4: Configure environment
if [ ! -f .env ]; then
    print_status "Setting up environment variables..."
    cp env.example .env
    
    print_warning "IMPORTANT: Please configure your Telegram credentials!"
    echo ""
    echo "Edit .env file with:"
    echo "   TELEGRAM_BOT_TOKEN=your_bot_token_here"
    echo "   TELEGRAM_CHAT_ID=your_chat_id_here"
    echo ""
    echo "📱 Get bot token from: https://t.me/BotFather"
    echo "💬 Get chat ID by messaging your bot"
    echo ""
    
    read -p "Press Enter when you've configured .env file..."
fi

# Step 5: Get VM IP address
VM_IP=$(hostname -I | awk '{print $1}')
print_status "Your VM IP address: $VM_IP"
echo ""
echo "Access URLs after deployment:"
echo "   🎨 Dashboard: http://$VM_IP:5173"
echo "   📚 API Docs:  http://$VM_IP:8001/docs"
echo "   🛡️ Honeypot:  ssh user@$VM_IP -p 2222"
echo ""

# Step 6: Deploy services
print_status "Building and starting AetherionBot services..."
docker-compose build --no-cache

if [ $? -ne 0 ]; then
    print_error "Docker build failed. Please check the error messages above."
    exit 1
fi

docker-compose up -d

if [ $? -ne 0 ]; then
    print_error "Failed to start services. Please check the error messages above."
    exit 1
fi

# Wait for services to start
print_status "Waiting for services to initialize..."
sleep 15

# Check service status
print_status "Checking service status..."
docker-compose ps

# Test endpoints
print_status "Testing endpoints..."

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

echo ""
print_success "🎉 AetherionBot deployed successfully on Ubuntu VM!"
echo ""

# Display access information
echo "📋 ACCESS INFORMATION:"
echo "====================="
echo "🎨 Dashboard:  http://$VM_IP:5173"
echo "📚 API Docs:   http://$VM_IP:8001/docs"
echo "🛡️ Honeypot:   ssh user@$VM_IP -p 2222"
echo ""

# Display management commands
echo "🔧 MANAGEMENT COMMANDS:"
echo "======================="
echo "View logs:        docker-compose logs -f"
echo "Stop services:    docker-compose down"
echo "Restart:          docker-compose restart"
echo "Update:           docker-compose pull && docker-compose up -d"
echo ""

# Display security recommendations
echo "🛡️ SECURITY RECOMMENDATIONS:"
echo "============================"
echo "✅ Configure firewall: sudo ufw enable"
echo "✅ Allow ports: sudo ufw allow 8001,5173,2222/tcp"
echo "✅ Monitor logs: docker-compose logs -f"
echo "✅ Set up backup scripts for data"
echo ""

# Test honeypot connectivity
print_status "Testing honeypot connection..."
if nc -z localhost 2222 2>/dev/null; then
    print_success "✅ Honeypot accepting connections on port 2222"
else
    print_warning "⚠️ Honeypot might still be starting up"
fi

echo ""
print_status "🚀 Deployment complete! Your AetherionBot is ready to deceive attackers."
echo ""
echo "💡 Pro tip: Use 'docker-compose logs -f' to monitor activity in real-time"
echo ""

read -p "Press Enter to view recent logs (Ctrl+C to exit)..."
echo ""
docker-compose logs --tail=20

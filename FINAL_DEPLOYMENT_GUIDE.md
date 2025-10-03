# 🛡️ Complete AetherionSecBot Deployment Guide

**Enterprise-Grade AI/ML Honeypot System**  
**Your Telegram Bot**: `t.me/AetherionSecBot`  
**Bot Token**: `8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds`  
**Chat ID**: `6433268037`

---

## 🚀 **SUPER QUICK DEPLOYMENT (Ubuntu VM)**

### **Single Command Deployment:**
```bash
curl -sSL https://raw.githubusercontent.com/bhataakib02/HoneyPort/main/UBUNTU_DEPLOY.sh | bash
```

### **Alternative Direct Command:**
```bash
sudo apt update && sudo apt install curl git docker.io docker-compose -y && sudo usermod -aG docker $USER && git clone https://github.com/bhataakib02/HoneyPort.git && cd HoneyPort && echo "TELEGRAM_BOT_TOKEN=8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds" > .env && echo "TELEGRAM_CHAT_ID=6433268037" >> .env && docker-compose build --no-cache && docker-compose up -d && sleep 20 && curl -s -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/sendMessage" -d "chat_id=6433268037" -d "text=🛡️ AetherionSecBot Deployed!" && echo "✅ Deployed! Dashboard: http://$(hostname -I | awk '{print $1}'):5173"
```

---

## 📋 **MANUAL STEP-BY-STEP DEPLOYMENT**

### **Step 1: System Preparation**
```bash
# Update Ubuntu system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install curl git docker.io docker-compose -y

# Configure Docker permissions
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker is running
sudo systemctl start docker
sudo systemctl enable docker
```

### **Step 2: Clone Repository**
```bash
# Remove existing directory if present
rm -rf HoneyPort

# Clone the repository
git clone https://github.com/bhataakib02/HoneyPort.git
cd HoneyPort
```

### **Step 3: Configure Environment**
```bash
# Create environment file with your Telegram credentials
echo "TELEGRAM_BOT_TOKEN=8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds" > .env
echo "TELEGRAM_CHAT_ID=6433268037" >> .env

# Verify configuration
cat .env
```

### **Step 4: Deploy Services**
```bash
# Build Docker containers
docker-compose build --no-cache

# Start all services
docker-compose up -d

# Wait for services to initialize
sleep 30

# Check service status
docker-compose ps
```

### **Step 5: Verify Deployment**
```bash
# Get VM IP address
VM_IP=$(hostname -I | awk '{print $1}')
echo "Your VM IP: $VM_IP"

# Test all services
echo "🧪 Testing Services..."

# Test Dashboard
curl -I http://localhost:5173 && echo "✅ Dashboard: Running"

# Test API
curl http://localhost:8001/health && echo "✅ API: Running"

# Test Telegram Bot
curl -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/sendMessage" \
  -d "chat_id=6433268037" \
  -d "text=🎉 AetherionSecBot Test from Ubuntu VM!" \
  && echo "✅ Telegram: Working"

# Show access information
echo ""
echo "🎯 ACCESS YOUR AETHERIONBOT:"
echo "🎨 Dashboard: http://$VM_IP:5173"
echo "📚 API Docs: http://$VM_IP:8001/docs"
echo "🛡️ Honeypot: ssh user@$VM_IP -p 2222"
echo "📱 Telegram: t.me/AetherionSecBot"
```

---

## 🔧 **TROUBLESHOOTING GUIDE**

### **Docker Networking Issues**
If Docker bridges are DOWN and dashboard is inaccessible:

```bash
# Stop all containers
docker-compose down

# Clean up Docker networks
docker network prune -f
docker system prune -f

# Restart Docker service
sudo systemctl restart docker

# Verify Docker is working
docker version

# Start services again
docker-compose up -d

# Check Docker interfaces
ip a show docker0
```

### **Port Access Issues**
If services aren't accessible externally:

```bash
# Check if containers are running
docker ps

# Check port mappings
docker port dashboard
docker port backend
docker port honeypot

# Check firewall (if enabled)
sudo ufw status
sudo ufw allow 5173
sudo ufw allow 8001
sudo ufw allow 2222
```

### **Telegram Bot Issues**
If Telegram alerts aren't working:

```bash
# Test Telegram API directly
curl -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/getMe"

# Check environment variables in container
docker exec backend env | grep TELEGRAM

# Verify .env file
cat .env
```

---

## 📊 **MONITORING & MANAGEMENT**

### **Check System Status**
```bash
# View all running containers
docker-compose ps

# Check container logs
docker-compose logs dashboard
docker-compose logs backend
docker-compose logs honeypot

# Monitor resource usage
docker stats

# Check disk usage
docker system df
```

### **View Threat Analytics**
```bash
# Check threat sessions
curl http://localhost:8001/sessions

# View system statistics
curl http://localhost:8001/stats

# Check threat intelligence
curl http://localhost:8001/threats
```

### **Service Management**
```bash
# Restart services
docker-compose restart

# Restart specific service
docker-compose restart dashboard

# View real-time logs
docker-compose logs -f

# Stop all services
docker-compose down

# Remove everything
docker-compose down --rmi all
```

---

## 🌍 **VM NETWORK CONFIGURATION**

### **VM IP Address Discovery**
```bash
# Show network interfaces
ip a

# Show routing table
ip route

# Test network connectivity
ping google.com

# Show listening ports
sudo netstat -tlnp | grep -E ':(5173|8001|2222)'
```

### **External Access Setup**
If accessing from another machine on the network:

```bash
# Get VM IP
VM_IP=$(hostname -I | awk '{print $1}')

# Configure port forwarding (if using NAT)
# Use VM settings: Host Port 5173 → Guest Port 5173
# Use VM settings: Host Port 8001 → Guest Port 8001  
# Use VM settings: Host Port 2222 → Guest Port 2222

echo "🎯 Access AetherionBot from host machine:"
echo "Dashboard: http://$VM_IP:5173"
echo "API: http://$VM_IP:8001/docs"
echo "Honeypot: ssh user@$VM_IP -p 2222"
```

---

## 🚨 **SECURITY CONFIGURATION**

### **Environment Variables (Already Configured)**
```bash
# Your Telegram configuration
TELEGRAM_BOT_TOKEN=8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds
TELEGRAM_CHAT_ID=6433268037
```

### **Firewall Configuration (Optional)**
```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow AetherionBot ports
sudo ufw allow 5173    # Dashboard
sudo ufw allow 8001     # API
sudo ufw allow 2222     # Honeypot

# Check firewall status
sudo ufw status verbose
```

---

## 📱 **TELEGRAM BOT USAGE**

### **Sending Alerts**
Your Telegram bot will automatically send alerts for:
- **HIGH** and **CRITICAL** threat detection
- System deployment confirmation
- Honeypot activity alerts

### **Manual Testing**
Send test messages:
```bash
# Test message
curl -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/sendMessage" \
  -d "chat_id=6433268037" \
  -d "text=🧪 AetherionSecBot Test Message"
```

### **Bot Commands**
Send `/start` to `t.me/AetherionSecBot` to:
- Initialize the bot
- Receive welcome message
- Get system status

---

## 🔄 **UPDATING THE SYSTEM**

### **Update from GitHub**
```bash
# Navigate to project directory
cd /path/to/HoneyPort

# Pull latest changes
git pull origin main

# Rebuild and restart services
docker-compose build --no-cache
docker-compose up -d
```

### **Backup Configuration**
```bash
# Backup important data
cp .env .env.backup
cp honeypot/data/sessions.json sessions.backup.json
cp honeypot/data/threat_intelligence.json threats.backup.json
```

---

## 📋 **DEPLOYMENT CHECKLIST**

Before deployment:
- [ ] Ubuntu VM with at least 2GB RAM
- [ ] Internet connection for package downloads
- [ ] Docker and Docker Compose installed
- [ ] Git access to repository

During deployment:
- [ ] Repository cloned successfully
- [ ] Environment variables configured
- [ ] Docker containers built without errors
- [ ] All services started properly

After deployment:
- [ ] Dashboard accessible via browser
- [ ] API documentation accessible
- [ ] Telegram bot responding
- [ ] Honeypot accepting SSH connections
- [ ] Threat alerts working

---

## 🎯 **FINAL ACCESS SUMMARY**

**Your AetherionSecBot System Access:**

| Service | URL/Command |
|---------|-------------|
| 🎨 Dashboard | `http://VM_IP:5173` |
| 📚 API Docs | `http://VM_IP:8001/docs` |
| 🛡️ Honeypot SSH | `ssh user@VM_IP -p 2222` |
| 📱 Telegram Bot | `t.me/AetherionSecBot` |

**System Features:**
- ✅ Advanced AI/ML Threat Detection
- ✅ Real-time Dashboard Interface  
- ✅ Professional Analytics & Reporting
- ✅ Telegram Alert Integration
- ✅ SSH Honeypot Simulation
- ✅ Geographic Threat Analysis
- ✅ Threat Intelligence Database

---

## 🎉 **SUCCESS!**

**Your AetherionSecBot AI/ML Honeypot System is now deployed and ready for professional threat detection!**

Send `/start` to **`t.me/AetherionSecBot`** to begin monitoring threats! 🛡️✨

---

*Deployment Guide v1.0 - AetherionSecBot Enterprise Security System*

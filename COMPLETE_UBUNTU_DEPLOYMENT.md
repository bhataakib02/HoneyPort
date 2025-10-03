# 🛡️ Complete Ubuntu VM Deployment Guide

> **From Fresh Ubuntu VM to Live AetherionSecBot System**

---

## **STEP 1: UBUNTU VM SETUP** 🛠️

### **Fresh Ubuntu VM Terminal Setup:**
```bash
# Open Terminal in Ubuntu
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install curl git docker.io docker-compose -y

# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

---

## **STEP 2: DEPLOY AETHERIONBOT** 🚀

### **Option A: One Command Deployment:**
```bash
curl -sSL https://raw.githubusercontent.com/bhataakib02/HoneyPort/main/UBUNTU_DEPLOY.sh | bash
```

### **Option B: Manual Deployment:**
```bash
# Clone repository
git clone https://github.com/bhataakib02/HoneyPort.git
cd HoneyPort

# Configure Telegram (yours is pre-configured)
echo "TELEGRAM_BOT_TOKEN=8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds" > .env
echo "TELEGRAM_CHAT_ID=6433268037" >> .env

# Deploy services
docker-compose build --no-cache
docker-compose up -d

# Wait for startup
sleep 30
```

---

## **STEP 3: VERIFY DEPLOYMENT** ✅

### **Check Service Status:**
```bash
# Check Docker containers
docker ps

# Check your VM IP
ip a

# Test services locally
curl -I http://localhost:5173
curl -I http://localhost:8001/health
```

### **Expected Output:**
- 3 containers running: `dashboard`, `backend`, `honeypot`
- Your VM IP: `10.0.2.15` (or similar)
- Services responding on localhost

---

## **STEP 4: TEST ALL FUNCTIONALITY** 🧪

### **Test 1: Dashboard Access**
```bash
# Get your VM IP
VM_IP=$(hostname -I | awk '{print $1}')

# Test dashboard
curl -I http://$VM_IP:5173
echo "Dashboard: http://$VM_IP:5173"
```

**🎯 Open in browser:** `http://10.0.2.15:5173` (replace with your VM IP)

### **Test 2: API Documentation**
```bash
# Test API
curl http://$VM_IP:8001/health
echo "API Docs: http://$VM_IP:8001/docs"
```

**🎯 Open in browser:** `http://10.0.2.15:8001/docs`

### **Test 3: Telegram Bot**
```bash
# Test Telegram bot
curl -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/sendMessage" -d "chat_id=6433268037" -d "text=🎉 AetherionSecBot Live From Ubuntu VM!"

# Check Telegram: Go to t.me/AetherionSecBot and send /start
```

### **Test 4: Honeypot SSH**
```bash
# Test SSH honeypot
ssh user@localhost -p 2222
# Try commands: ls, pwd, whoami, cat /etc/passwd
```

---

## **STEP 5: DOCKER TROUBLESHOOTING** 🔧

### **If Dashboard Not Accessible:**

```bash
# Stop containers
docker-compose down

# Fix Docker networking
sudo systemctl restart docker
docker network prune -f

# Check Docker bridges
ip a show docker0

# Restart services
docker-compose up -d

# Check port mappings
docker port dashboard
docker port backend
```

### **If Port Access Issues:**

```bash
# Check if services are listening
sudo netstat -tlnp | grep -E ':(5173|8001|2222)'

# Check firewall
sudo ufw status

# Allow ports if needed
sudo ufw allow 5173
sudo ufw allow 8001
sudo ufw allow 2222
```

---

## **STEP 6: PRODUCTION VERIFICATION** 🎯

### **Complete System Test:**
```bash
# Test Dashboard
curl http://localhost:5173 && echo "✅ Dashboard Working"

# Test API Health
curl http://localhost:8001/health && echo "✅ API Working"

# Test Telegram Bot
curl -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/sendMessage" -d "chat_id=6433268037" -d "text=✅ Final Test - AetherionSecBot Operational!" && echo "✅ Telegram Working"

# Test Honeypot
nc localhost 2222 && echo "✅ Honeypot Working"

# Check threat detection
curl http://localhost:8001/sessions && echo "✅ Threat Detection Working"
```

### **Expected Final Results:**

```bash
# Get final access information
VM_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "🎯 YOUR AETHERIONSECBOT IS LIVE!"
echo "================================"
echo "🎨 Dashboard: http://$VM_IP:5173"
echo "📚 API Docs: http://$VM_IP:8001/docs"
echo "🛡️ Honeypot: ssh user@$VM_IP -p 2222"
echo "📱 Telegram: t.me/AetherionSecBot"
echo "================================"
```

---

## **STEP 7: MONITORING COMMANDS** 📊

### **View System Status:**
```bash
# Check containers: dashboard, backend, honeypot
docker-compose ps

# View logs
docker-compose logs dashboard
docker-compose logs backend
docker-compose logs honeypot

# Check resource usage
docker stats
```

### **View Threat Data:**
```bash
# Check detected threats
curl http://localhost:8001/sessions

# View system statistics
curl http://localhost:8001/stats

# Check threat intelligence
curl http://localhost:8001/threats
```

---

## **🎉 FINAL SUCCESS CHECKLIST** ✅

Before considering deployment complete:

- [ ] ✅ Ubuntu VM updated and Docker installed
- [ ] ✅ Repository cloned successfully
- [ ] ✅ Docker containers running (3 services)
- [ ] ✅ Dashboard accessible via browser
- [ ] ✅ API documentation accessible
- [ ] ✅ Telegram bot responding with test message
- [ ] ✅ SSH honeypot accepting connections
- [ ] ✅ Threat detection generating sessions
- [ ] ✅ All services accessible via VM IP

---

## **🚨 IF ANYTHING FAILS:**

### **Complete Reset Command:**
```bash
# Nuclear option - start fresh
docker-compose down --rmi all
docker system prune -f
rm -rf HoneyPort
git clone https://github.com/bhataakib02/HoneyPort.git
cd HoneyPort
echo "TELEGRAM_BOT_TOKEN=8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds" > .env
echo "TELEGRAM_CHAT_ID=6433268037" >> .env
docker-compose up -d
```

---

## **🎯 YOUR FINAL ACCESS:**

**Once deployment is successful:**
- **Dashboard**: `http://VM_IP:5173`
- **API Docs**: `http://VM_IP:8001/docs`
- **Telegram Bot**: `t.me/AetherionSecBot`
- **Honeypot SSH**: `ssh user@VM_IP -p 2222`

**Your AetherionSecBot is now ready for professional threat detection!** 🛡️✨

---

**📱 Your Telegram Bot: t.me/AetherionSecBot**  
**🤖 Token: 8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds**  
**💬 Chat ID: 6433268037**

---

*Complete Ubuntu VM Deployment Guide - Copy & Paste Ready*

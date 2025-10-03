# 🛡️ Ubuntu VM Deployment - Copy Commands

**Your Telegram Bot**: t.me/AetherionSecBot  
**Bot Token**: `8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds`  
**Chat ID**: `6433268037`

---

## 🚀 **FIXED SINGLE COMMAND DEPLOYMENT**

Copy this command and paste in Ubuntu terminal (handles existing directories):

```bash
curl -sSL https://raw.githubusercontent.com/bhataakib02/HoneyPort/main/UBUNTU_DEPLOY.sh | bash
```

> **✅ Fixed Issues**: Automatically removes existing HoneyPort directory, verifies docker-compose.yml exists, and fixes Docker configuration (backend port 8001, proper module references, environment variables).

---

## 🔥 **ALTERNATIVE DIRECT COMMAND**

If the above doesn't work, use this longer command:

```bash
sudo apt update && sudo apt install curl git docker.io docker-compose -y && sudo usermod -aG docker $USER && git clone https://github.com/bhataakib02/HoneyPort.git && cd HoneyPort && echo "TELEGRAM_BOT_TOKEN=8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds" > .env && echo "TELEGRAM_CHAT_ID=6433268037" >> .env && docker-compose build --no-cache && docker-compose up -d && sleep 20 && curl -s -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/sendMessage" -d "chat_id=6433268037" -d "text=🛡️ AetherionSecBot Deployed!" && echo "✅ Deployed! Dashboard: http://$(hostname -I | awk '{print $1}'):5173"
```

---

## 📋 **MANUAL STEP-BY-STEP** (if needed)

Copy and run these commands one by one:

```bash
# 1. Update Ubuntu
sudo apt update && sudo apt upgrade -y

# 2. Install Docker
sudo apt install curl git docker.io docker-compose -y

# 3. Configure Docker permissions
sudo usermod -aG docker $USER
newgrp docker

# 4. Clone repository
git clone https://github.com/bhataakib02/HoneyPort.git
cd HoneyPort

# 5. Configure Telegram
echo "TELEGRAM_BOT_TOKEN=8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds" > .env
echo "TELEGRAM_CHAT_ID=6433268037" >> .env

# 6. Deploy services
docker-compose build --no-cache
docker-compose up -d

# 7. Wait for services to start
sleep 30

# 8. Test Telegram bot
curl -s -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/sendMessage" -d "chat_id=6433268037" -d "text=🛡️ AetherionSecBot is online!"

# 9. Show access info
echo "✅ Deployment Complete!"
VM_IP=$(hostname -I | awk '{print $1}')
echo "🎨 Dashboard: http://$VM_IP:5173"
echo "📚 API Docs: http://$VM_IP:8001/docs"
echo "🛡️ Honeypot: ssh user@$VM_IP -p 2222"
echo "📱 Telegram: t.me/AetherionSecBot"
```

---

## 🧪 **TEST AFTER DEPLOYMENT**

Copy these test commands:

```bash
# Test Telegram Bot
curl -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds/sendMessage" -d "chat_id=6433268037" -d "text=🧪 Test message from Ubuntu VM"

# Test Dashboard
curl http://localhost:5173

# Test API
curl http://localhost:8001/stats

# Test Honeypot
nc localhost 2222
```

---

## 🔧 **MANAGEMENT COMMANDS**

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Remove everything
docker-compose down --rmi all
```

---

## 💡 **SUCCESS CHECKLIST**

After deployment, verify:
- ✅ Telegram bot responds: Send `/start` to `t.me/AetherionSecBot`
- ✅ Dashboard loads: Open `http://VM_IP:5173` in browser
- ✅ API works: `curl http://VM_IP:8001/stats`
- ✅ Honeypot accepts: `ssh user@VM_IP -p 2222`

---

## 🎯 **ACCESS YOUR AETHERIONBOT**

Replace `VM_IP` with your actual Ubuntu VM IP:

- **🎨 Dashboard**: `http://VM_IP:5173`
- **📚 API Docs**: `http://VM_IP:8001/docs`
- **📱 Telegram Bot**: `t.me/AetherionSecBot`
- **🛡️ Honeypot**: `ssh user@VM_IP -p 2222`

---

**🚀 Your AetherionSecBot will be ready in ~5 minutes!** 🛡️✨

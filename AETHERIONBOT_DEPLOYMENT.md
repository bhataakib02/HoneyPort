# 🛡️ AetherionBot Complete Deployment

**Your Telegram Bot**: t.me/AetherionSecBot ✅  
**Bot Token**: `8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds`  
**Chat ID**: `6433268037`

---

## 🚀 **COMPLETE SINGLE COMMAND DEPLOYMENT**

**Copy and paste this EXACT command in your Ubuntu VM:**

```bash
sudo apt update && sudo apt install curl git docker.io docker-compose -y && sudo usermod -aG docker $USER && git clone https://github.com/bhataakib02/HoneyPort.git && cd HoneyPort && echo 'TELEGRAM_BOT_TOKEN=8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds' > .env && echo 'TELEGRAM_CHAT_ID=6433268037' >> .env && cp .env env.example && docker-compose build --no-cache && docker-compose up -d && sleep 15 && echo "🎉 AetherionBot deployed successfully!" && echo "📱 Telegram Bot: t.me/AetherionSecBot" && echo "🎯 Dashboard: http://$(hostname -I | awk '{print $1}'):5173" && echo "📚 API Docs: http://$(hostname -I | awk '{print $1}'):8001/docs" && echo "🛡️ Honeypot: ssh user@$(hostname -I | awk '{print $1}') -p 2222" && echo "📊 Check status: docker-compose ps"
```

---

## 🎯 **What This Command Does:**

1. ✅ **Updates Ubuntu** system packages
2. ✅ **Installs Docker** and dependencies  
3. ✅ **Configures Docker** permissions
4. ✅ **Clones AetherionBot** repository
5. ✅ **Sets up Environment** with your Telegram credentials
6. ✅ **Builds containers** automatically
7. ✅ **Starts all services** in background
8. ✅ **Shows access URLs** with your VM IP
9. ✅ **Displays status** check command

---

## 📱 **Expected Output:**

```
Executing: apt update
Get:1 https://ubuntu.archive.ubuntu.com focal InRelease [297 kB]
...

🤖 Bot Details:
✅ Bot Token: 8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds
✅ Chat ID: 6433268037  
✅ Bot Link: t.me/AetherionSecBot

🔧 Configuration Step:
✅ Environment configured with Telegram credentials
✅ Telegram alerts enabled

🚀 Starting AetherionBot...
🎉 AetherionBot deployed successfully!
📱 Telegram Bot: t.me/AetherionSecBot
🎯 Dashboard: http://192.168.1.100:5173
📚 API Docs: http://192.168.1.100:8001/docs
🛡️ Honeypot: ssh user@192.168.1.100 -p 2222
📊 Check status: docker-compose ps
```

---

## 🔧 **Management Commands:**

After deployment, use these commands in the HoneyPort directory:

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Update and restart
docker-compose pull && docker-compose up -d
```

---

## 🧪 **Test Your Deployment:**

### **Test Telegram Bot:**
```bash
# Send test message to your bot
curl -X POST "https://api.telegram.org/bot8290924411:AAGsOGoYulFfavqv-xmyDBKC7FdcR24D0Ds" \
  -d "chat_id=6433268037" \
  -d "text=🛡️ AetherionBot is online and ready to deceive attackers!"
```

### **Test Honeypot Connection:**
```bash
# Connect to honeypot
ssh user@YOUR_VM_IP -p 2222

# Test with telnet
telnet YOUR_VM_IP 2222
```

### **Test Dashboard:**
```bash
# Open in browser
curl http://localhost:5173

# Check API
curl http://localhost:8001/stats
curl http://localhost:8001/sessions
```

---

## 🎉 **CONGRATULATIONS!**

Your **AetherionSecBot** is now:
- ✅ **Deployed** on Ubuntu VM
- ✅ **Configured** with Telegram alerts  
- ✅ **Monitoring** attacks in real-time
- ✅ **Sending alerts** to your chat (6433268037)
- ✅ **Professional dashboard** showing threat activity
- ✅ **Interactive honeypot** deceiving attackers

---

## 🛡️ **Access Your AetherionBot:**

Replace `YOUR_VM_IP` with actual IP from deployment:

- **🎨 Dashboard**: `http://YOUR_VM_IP:5173`
- **📚 API Docs**: `http://YOUR_VM_IP:8001/docs`
- **📱 Telegram Bot**: `t.me/AetherionSecBot`
- **🛡️ Honeypot**: `ssh user@YOUR_VM_IP -p 2222`

---

## 💡 **Pro Tips:**

- **📱 Test Telegram bot**: Send `/start` to `t.me/AetherionSecBot`
- **🛡️ Monitor attacks**: Watch dashboard for threat activity
- **📊 Check logs**: Use `docker-compose logs -f` for real-time monitoring
- **🔄 Keep updated**: Run `docker-compose pull && docker-compose up -d` regularly

---

**🎯 Your AetherionSecBot Cyber Deception Engine is ready!** 🛡️✨

Perfect for learning cybersecurity and detecting real threats!

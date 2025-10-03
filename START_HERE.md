# 🚀 AIML Honeypot - Start Here!

## ✅ What You Have Right Now

**Complete industrial-grade AI/ML honeypot system:**

- 🎯 **SSH/Telnet Honeypot** (port 2222)
- 🤖 **AI/ML Threat Detection** (IsolationForest)
- 📱 **Real-Time Telegram Alerts** (your bot: `AetherionBot`)
- 🖥️ **Live Dashboard** (React web interface)
- 🔄 **Auto-Learning** (ML model retrains hourly)
- 📦 **Dockerized** (runs everywhere)

## 🚀 1-Minute Quick Start

```bash
# Create .env file with your Telegram credentials
echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here" > .env
echo "TELEGRAM_CHAT_ID=your_telegram_chat_id_here" >> .env

# Build and start everything
docker-compose build
docker-compose up -d

# Wait 30 seconds, then test
nc localhost 2222
```

## 🧪 Test Your Honeypot NOW

**Terminal 1:**
```bash
nc localhost 2222
# Type: ls -la
# Type: cat /etc/passwd  
# Type: rm -rf /
```

**Terminal 2:**
```bash
# View dashboard
open http://localhost:5173
```

**Terminal 3:**
```bash
# Check your Telegram - you'll get real alerts!
```

## 📱 Your Telegram Bot Already Works!

**Bot:** `AetherionBot` (8290924411:...)
**Chat ID:** 6433268037

When you type suspicious commands like `rm -rf /`, you'll instantly get Telegram alerts!

## 🌐 Dashboard URLs

- **Main Dashboard:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 🔧 Management Commands

```bash
# View all logs
docker-compose logs -f

# View just honeypot logs  
docker-compose logs -f honeypot

# Restart everything
docker-compose restart

# Stop everything
docker-compose down

# Update and restart
docker-compose build && docker-compose up -d
```

## 🎯 What Makes This Special

✅ **Real AI** - Uses scikit-learn IsolationForest for anomaly detection
✅ **Real Learning** - ML model learns from every attack attempt
✅ **Real Alerts** - Telegram notifications for HIGH/CRITICAL threats
✅ **Real Dashboard** - Live React interface with charts and session replay
✅ **Real Production** - Dockerized, scalable, industrial-grade

## ✅ You're Ready!

**Test it now:** `nc localhost 2222` and watch your Telegram for alerts!

The dashboard will show live sessions, threat levels, and detailed command analysis.

**🚀 Your AIML honeypot is live and catching attackers!**




# 🚀 AIML Honeypot - Complete Deployment Guide

## 📋 What You Have Now

**A complete, industrial-grade AI/ML honeypot system with:**

✅ **AI-Powered Honeypot** (SSH/Telnet listener on port 2222)
✅ **Machine Learning** (IsolationForest for anomaly detection)
✅ **Real-Time Learning** (Auto retraining every hour)
✅ **Telegram Alerts** (Instant notifications for threats)
✅ **Interactive Dashboard** (React + Tailwind CSS)
✅ **Dockerized Infrastructure** (Easy deployment anywhere)
✅ **Sample Data** (Ready to test immediately)

## 🛠️ Your Telegram Configuration

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

## 🚀 Quick Start

### 1. **Ubuntu/Linux Deployment**

```bash
# Clone/download the project
cd ~
# Extract your project files

# Copy your Telegram credentials
cp env.example .env
nano .env
# Add the token and chat ID above

# Build and start
docker-compose build
docker-compose up -d

# Test the honeypot
nc localhost 2222
echo "ls -la" | nc localhost 2222

# View dashboard
open http://localhost:5173
```

### 2. **Windows Deployment (Docker Desktop)**

1. Install Docker Desktop for Windows
2. Open PowerShell/Terminal in project folder
3. Run the above commands (same as Linux)

## 🧪 Testing Your Honeypot

### Connect & Test Commands

```bash
# Method 1: Netcat
nc localhost 2222
# Type: ls -la, whoami, cat /etc/passwd

# Method 2: SSH (no key needed)
ssh -p 2222 test@localhost
# Enter any credentials, try commands

# Method 3: Telnet
telnet localhost 2222
```

### Test Telegram Alerts

```bash
# Send suspicious command via telnet
telnet localhost 2222
# Type: rm -rf /

# Check Telegram - you should receive an alert!
```

## 📊 Dashboard Usage

**Access:** http://localhost:5173

**Features:**
- Real-time session list
- Threat level visualization
- Command analysis details
- Statistics and charts
- IP tracking

## 🔧 Management Commands

```bash
# View logs
docker-compose logs -f honeypot
docker-compose logs -f backend
docker-compose logs -f dashboard

# Restart services
docker-compose restart

# Stop all services
docker-compose down

# Build fresh
docker-compose build --no-cache

# Train ML model manually
docker-compose run --rm backend python train_model.py
```

## 🚨 Integration Features

### AIML Honeypot Engine
- SSH/Telnet simulation (port 2222)
- Realistic command responses
- Full session logging
- IP tracking and analysis

### AI/ML Detection
- Command feature extraction
- IsolationForest anomaly detection
- Threat level classification (LOW/MEDIUM/HIGH/CRITICAL)
- Auto-retraining with new attack patterns

### Telegram Alerts
- Real-time threat notifications
- Rich formatting with emojis
- IP and command details
- Threat level indicators

### Dashboard Features
- React-based web interface
- Real-time updates
- Session replay and analysis
- Statistics and threat charts
- Mobile-responsive design

## 🌐 Service Endpoints

| Service | URL | Purpose |
|---------|-----|---------|
| Dashboard | http://localhost:5173 | Main monitoring interface |
| Honeypot | localhost:2222 | SSH/Telnet listener |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger documentation |

## 🔥 Advanced Features

### Real-Time ML Learning
- Model retrains automatically every hour
- Learns from new attack patterns
- Adapts detection thresholds

### Professional Logging
- JSON-formatted logs
- Session persistence
- TSV logs for analysis
- Comprehensive audit trails

### Threat Intelligence
- Command pattern analysis
- Attack vector detection
- Behavioral profiling
- Abnormal activity scoring

## 📈 Production Deployment

### Ubuntu Auto-Start
```bash
# Create systemd service
sudo tee /etc/systemd/system/aiml-honeypot.service > /dev/null <<EOF
[Unit]
Description=AIML Honeypot Stack
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/$USER/aiml-honeypot
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable aiml-honeypot
sudo systemctl start aiml-honeypot
```

### GitHub Integration
Your project is ready to push to GitHub:

1. Create GitHub repository
2. `git init`
3. `git add .`
4. `git commit -m "Industrial AIML Honeypot"`
5. `git remote add origin <your-repo-url>`
6. `git push -u origin main`

## 🛡️ Security Considerations

- Run in isolated VM/container
- Monitor resource usage
- Regular backups of session logs
- Update components periodically
- Configure firewall rules appropriately

## ❓ Troubleshooting

### Services Won't Start
```bash
docker-compose logs
docker system prune -f
docker-compose up -d
```

### No Telegram Alerts
Check `.env` file has correct token and chat ID

### Dashboard Won't Load
Check browser console for errors, verify backend is running

### ML Model Issues
```bash
docker-compose run --rm backend python train_model.py
docker-compose restart backend
```

## 🎯 What's Next?

1. **Push to GitHub** - Share your project
2. **Deploy on Ubuntu** - Run in production
3. **Add More Features** - HTTP, FTP honeypots
4. **Integrate More AI** - LSTM, Transformer models
5. **Expand Monitoring** - ELK stack, Grafana

---

**🎉 Congratulations! You now have a complete, professional-grade AI/ML honeypot system!**

Connect to `nc localhost 2222` and start testing your honeypot right now! 🚀




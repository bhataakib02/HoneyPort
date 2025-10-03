# 🐧 Ubuntu VM Deployment Guide

Deploy AetherionBot Cyber Deception Engine on Ubuntu Virtual Machine

## 📋 **Prerequisites**

- Ubuntu 20.04+ (or any Debian-based Linux)
- VM with at least **2GB RAM** and **20GB disk space**
- Internet connection
- SSH access (if remote deployment)

---

## 🚀 **One-Click Ubuntu Deployment**

### **📥 Step 1: Clone Repository**

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install git if not present
sudo apt install git -y

# Clone the AetherionBot repository
git clone https://github.com/bhataakib02/HoneyPort.git
cd HoneyPort
```

### **🐳 Step 2: Install Docker & Docker Compose**

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### **🔧 Step 3: Configure Environment**

```bash
# Copy environment template
cp env.example .env

# Edit environment file
nano .env

# Add your Telegram credentials:
# TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
# TELEGRAM_CHAT_ID=your_actual_chat_id_here
```

### **🚀 Step 4: Deploy AetherionBot**

```bash
# Make deployment script executable
chmod +x deploy-production.sh

# Run production deployment
./deploy-production.sh
```

**OR Manual Docker Deployment:**

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

---

## 🎯 **Access Your Deployed System**

After successful deployment, access your AetherionBot:

### **🌐 Web Interfaces:**
- **🎨 Dashboard**: `http://YOUR_VM_IP:5173`
- **📚 API Docs**: `http://YOUR_VM_IP:8001/docs`

### **🛡️ Honeypot Service:**
- **SSH Port**: `YOUR_VM_IP:2222`
- **Test Connection**: `ssh user@YOUR_VM_IP -p 2222`

### **📊 Example URLs:**
```
Dashboard:  http://192.168.1.100:5173
API Docs:   http://192.168.1.100:8001/docs
Honeypot:   ssh user@192.168.1.100 -p 2222
```

---

## 🔧 **VM-Specific Configuration**

### **🌐 Network Setup**

#### **For Local Testing:**
```bash
# Check VM IP address
ip addr show

# Example output: 192.168.1.100
# Use this IP in your browser
```

#### **For External Access:**
```bash
# Configure port forwarding in VM settings
# Map host ports to VM ports:
# - Host 5173 → VM 5173 (Dashboard)
# - Host 8001 → VM 8001 (API)
# - Host 2222 → VM 2222 (Honeypot)
```

### **⚡ Performance Optimization**

#### **Increase VM Resources:**
- **RAM**: Minimum 2GB (recommended: 4GB)
- **CPU**: At least 2 cores
- **Disk**: 20GB+ free space

#### **System Optimization:**
```bash
# Increase file descriptors limit
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize kernel parameters
echo "net.core.somaxconn = 65535" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## 🛠️ **Management Commands**

### **📊 Basic Operations:**

```bash
# Check all services status
docker-compose ps

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f dashboard
docker-compose logs -f honeypot

# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Stop and remove all containers
docker-compose down --rmi all
```

### **🔧 Maintenance:**

```bash
# Update all containers
docker-compose pull
docker-compose up -d

# Clean up unused Docker resources
docker system prune -a

# Check disk usage
docker system df
```

---

## 🧪 **Testing Your Deployment**

### **🎯 Test Dashboard:**

```bash
# Test dashboard accessibility
curl -I http://localhost:5173

# Expected response: HTTP/1.1 200 OK
```

### **🔌 Test API:**

```bash
# Test API endpoints
curl http://localhost:8001/sessions
curl http://localhost:8001/stats

# Test API documentation
curl http://localhost:8001/docs
```

### **🛡️ Test Honeypot:**

```bash
# Install SSH client
sudo apt install openssh-client -y

# Test honeypot connection
ssh -o StrictHostKeyChecking=no user@localhost -p 2222

# Send test commands
echo "whoami" | nc localhost 2222
echo "ls -la" | nc localhost 2222
```

---

## 🔒 **Security Configuration**

### **🛡️ Firewall Setup:**

```bash
# Install UFW firewall
sudo apt install ufw -y

# Allow SSH (replace with your port if changed)
sudo ufw allow ssh

# Allow AetherionBot ports
sudo ufw allow 8001/tcp  # API
sudo ufw allow 5173/tcp  # Dashboard
sudo ufw allow 2222/tcp  # Honeypot

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### **🔐 SSH Security:**

```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Use key-based authentication
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no

# Restart SSH service
sudo systemctl restart ssh
```

---

## 📊 **Monitoring & Logging**

### **📈 System Monitoring:**

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Monitor system resources
htop

# Monitor network usage
sudo nethogs

# Monitor disk I/O
sudo iotop
```

### **📋 Log Management:**

```bash
# View AetherionBot logs
docker-compose logs honeypot | tail -100
docker-compose logs backend | tail -100

# Set up log rotation
sudo nano /etc/logrotate.d/aetherionbot
```

---

## 🚨 Troubleshooting

### **❌ Common Issues:**

#### **Docker Permission Denied:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again, or run:
newgrp docker
```

#### **Port Already in Use:**
```bash
# Find process using port
sudo netstat -tulpn | grep :2222

# Kill process
sudo kill -9 <PID>
```

#### **Container Won't Start:**
```bash
# Check logs for errors
docker-compose logs <service_name>

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

#### **Out of Memory:**
```bash
# Check memory usage
free -h
docker stats

# Increase VM memory in settings
# Or optimize Docker:
echo '{"default-runtime":"io-docker-runc","features":{"buildkit":true}}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

---

## 🎉 **Success Checklist**

Your Ubuntu VM deployment is successful when:

- ✅ **Dashboard loads**: `http://YOUR_VM_IP:5173`
- ✅ **API responds**: `http://YOUR_VM_IP:8001/docs`
- ✅ **Honeypot accepts connections**: `ssh user@YOUR_VM_IP -p 2222`
- ✅ **Docker containers running**: `docker-compose ps`
- ✅ **No error logs**: `docker-compose logs`
- ✅ **Telegram alerts work** (if configured)

---

## 🚀 **Next Steps**

After successful deployment:

1. **🌐 Configure port forwarding** for external access
2. **🛡️ Set up firewall rules** for security
3. **📱 Configure Telegram alerts** for notifications
4. **📊 Set up monitoring** for system health
5. **🔄 Schedule updates** for regular maintenance

---

## 💡 **Pro Tips**

- **🔥 Use systemd** to auto-start Docker services on boot
- **📊 Set up Grafana** for advanced monitoring
- **🔐 Use HTTPS** in production with SSL certificates
- **🌍 Configure DNS** entries for easier access
- **📱 Monitor logs** regularly for threat detection

---

**🎯 Your AetherionBot is now ready to deceive attackers on Ubuntu VM!** 🛡️✨

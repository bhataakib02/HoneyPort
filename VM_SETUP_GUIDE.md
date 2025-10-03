# 🖥️ Ubuntu VM Quick Setup Guide

Quick setup guide for running AetherionBot on Ubuntu Virtual Machine

## ⚡ **VM Requirements**

- **OS**: Ubuntu 20.04 LTS or newer
- **RAM**: Minimum 2GB (recommended: 4GB)
- **CPU**: At least 2 cores
- **Disk**: 20GB free space
- **Network**: Bridged adapter recommended

---

## 🚀 **Super Quick Deploy (5 minutes)**

### **📥 Step 1: Clone & Deploy**
```bash
# One command deployment
curl -sSL https://raw.githubusercontent.com/bhataakib02/HoneyPort/main/ubuntu-deploy.sh | bash

# OR manual deployment
git clone https://github.com/bhataakib02/HoneyPort.git
cd HoneyPort
chmod +x ubuntu-deploy.sh
./ubuntu-deploy.sh
```

### **⚙️ Step 2: Configure**
```bash
# Edit Telegram credentials
nano .env

# Add your tokens:
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### **🎯 Step 3: Access**
- **Dashboard**: `http://YOUR_VM_IP:5173`
- **API**: `http://YOUR_VM_IP:8001/docs`
- **Honeypot**: `ssh user@YOUR_VM_IP -p 2222`

---

## 🛠️ **Manual VM Setup**

### **📋 VMware/VirtualBox Settings**
- **Network**: Bridged Adapter
- **Port Forwarding**: 5173, 8001, 2222
- **Shared Folders**: Optional

### **🌤️ Cloud VM Setup**
- **DigitalOcean**: $5 droplet minimum
- **AWS EC2**: t2.micro instance
- **Google Cloud**: e2-micro instance
- **Azure**: B1s burstable instance

---

## 📱 **VM Access URLs**

Replace `YOUR_VM_IP` with your actual VM IP address:

```bash
# Find your VM IP
ip addr show | grep "inet "

# Example URLs (replace with your IP):
http://192.168.1.100:5173     # Dashboard
http://192.168.1.100:8001/docs # API Docs
ssh user@192.168.1.100 -p 2222 # Honeypot
```

---

## 🔧 **VM Management**

### **📊 Check Status**
```bash
# Service status
docker-compose ps

# View logs
docker-compose logs -f

# System resources
htop
```

### **🔄 Restart Services**
```bash
# Restart everything
docker-compose restart

# Update and restart
docker-compose pull && docker-compose up -d
```

### **🛑 Stop Services**
```bash
# Stop all services
docker-compose down

# Stop and cleanup
docker-compose down --rmi all
```

---

## 🧪 **Testing Your VM Deployment**

### **🎨 Test Dashboard**
```bash
# Open in browser
curl http://localhost:5173

# Or use local browser
firefox http://localhost:5173
```

### **🔌 Test Honeypot**
```bash
# Connect to honeypot
ssh user@localhost -p 2222

# Send test commands
echo "whoami" | nc localhost 2222
echo "ls -la" | nc localhost 2222
echo "cat /etc/passwd" | nc localhost 2222
```

### **📊 Test API**
```bash
# Test endpoints
curl http://localhost:8001/sessions
curl http://localhost:8001/stats

# Check API docs
curl http://localhost:8001/docs
```

---

## 🛡️ **VM Security**

### **🔐 Basic Security**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install firewall
sudo apt install ufw -y

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 5173/tcp  # Dashboard
sudo ufw allow 8001/tcp  # API  
sudo ufw allow 2222/tcp  # Honeypot
sudo ufw enable
```

### **🔒 SSH Security**
```bash
# Disable root login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Key-based auth (optional)
ssh-keygen -t rsa
ssh-copy-id user@localhost
```

---

## 📈 **Performance Optimization**

### **⚡ VM Optimization**
- **Increase RAM** to 4GB+ for better performance
- **Use SSD storage** for faster I/O
- **Enable virtualization** features in VM settings
- **Allocate multiple CPU cores**

### **🚀 Docker Optimization**
```bash
# Limit Docker resource usage
echo '{"default-runtime":"io-docker-runc","features":{"buildkit":true}}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

---

## 💡 **VM Pro Tips**

### **📊 Monitoring**
- Use `htop` for real-time system monitoring
- Use `docker stats` for container monitoring
- Set up log rotation for long-running VMs

### **🔄 Maintenance**
- Schedule regular updates: `sudo apt update && sudo apt upgrade -y`
- Clean Docker regularly: `docker system prune -a`
- Backup important data and configurations

### **🌐 Network Access**
- Configure bridge mode for external access
- Set up port forwarding if behind NAT
- Use cloud VMs for better external access

---

## 🚨 **Troubleshooting VM Issues**

### **❌ Common Problems**

#### **Out of Memory:**
```bash
# Check memory usage
free -h
docker stats

# Increase VM memory allocation
# Or optimize containers
```

#### **Network Issues:**
```bash
# Check network configuration
ip addr show
sudo netstat -tulpn | grep :5173

# Test connectivity
ping 8.8.8.8
```

#### **Container Issues:**
```bash
# Check container logs
docker-compose logs honeypot
docker-compose logs backend

# Restart problematic container
docker-compose restart honeypot
```

---

## 🎉 **Success Checklist**

Your Ubuntu VM deployment is successful when:

- ✅ **VM boots successfully** with Ubuntu
- ✅ **Internet connection** working
- ✅ **Docker installation** complete
- ✅ **AetherionBot running** in containers
- ✅ **Dashboard accessible** via browser
- ✅ **API responding** with threat data
- ✅ **Honeypot accepting** SSH connections
- ✅ **Telegram alerts** working (if configured)

---

## 🚀 **Next Steps After Deployment**

1. **🌐 Configure external access** for remote monitoring
2. **📱 Set up Telegram bot** for alerts
3. **🛡️ Configure firewall** rules
4. **📊 Set up monitoring** dashboard
5. **🔄 Schedule maintenance** routines

---

**🎯 Your Ubuntu VM is now running AetherionBot Cyber Deception Engine!** 🛡️✨

Perfect for testing, development, and learning cybersecurity!

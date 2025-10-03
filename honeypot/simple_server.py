#!/usr/bin/env python3
"""
Simple AIML Honeypot Server - No complex dependencies
"""

import socket
import asyncio
import os
import json
import logging
from datetime import datetime
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleHoneypot:
    def __init__(self, host="0.0.0.0", port=2222):
        self.host = host
        self.port = port
        self.sessions_file = "data/sessions.json"
        self.commands_file = "data/commands.log"
        self._ensure_directories()

    def _ensure_directories(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump([], f)

    def analyze_threat_level(self, command):
        """Simple threat analysis"""
        suspicious_keywords = [
            "rm -rf", "cat /etc/passwd", "cat /etc/shadow", "wget", 
            "curl", "nc ", "systemctl", "su -", "sudo", "chmod +x", 
            "python -c", "bash -c", "sh -c", "/bin/bash", "find /",
            "kill -9", "iptables", "passwd", "id", "uname -a"
        ]
        
        command_lower = command.lower()
        threat_score = 0
        
        for keyword in suspicious_keywords:
            if keyword in command_lower:
                threat_score += 1
        
        # Calculate threat level
        if threat_score >= 3:
            return "CRITICAL", min(1.0, threat_score * 0.25)
        elif threat_score >= 2:
            return "HIGH", min(1.0, threat_score * 0.2)
        elif threat_score >= 1:
            return "MEDIUM", min(0.5, threat_score * 0.15)
        else:
            return "LOW", min(0.2, len(command) * 0.01)

    def log_session(self, ip, command, threat_level, score):
        """Log session to file"""
        session = {
            "session_id": f"{ip}_{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "ip": ip,
            "command": command,
            "threat_level": threat_level,
            "anomaly_score": score
        }
        
        try:
            # Load existing sessions
            with open(self.sessions_file, 'r') as f:
                sessions = json.load(f)
            
            sessions.append(session)
            
            # Save back (keep last 1000)
            if len(sessions) > 1000:
                sessions = sessions[-1000:]
            
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
            
            # Also append to commands.log
            with open(self.commands_file, 'a') as f:
                f.write(f"{ip}:{command}\n")
                
            logger.info(f"Session logged: {ip} -> {command} ({threat_level})")
            return session
            
        except Exception as e:
            logger.error(f"Error logging session: {e}")

    def generate_response(self, command):
        """Generate realistic command response"""
        command_lower = command.lower().strip()
        
        if command_lower == "ls":
            return "file1.txt  file2.txt  folder1/"
        elif command_lower == "ls -la":
            return """total 8
drwxr-xr-x 3 user user 4096 Jan 15 10:30 .
drwxr-xr-x 2 user user 4096 Jan 15 10:30 ..
-rw-r--r-- 1 user user  123 Jan 15 10:29 file1.txt
-rw-r--r-- 1 user user  456 Jan 15 10:30 file2.txt
drwxr-xr-x 2 user user 4096 Jan 15 10:30 folder1"""
        elif command_lower == "pwd":
            return "/home/user"
        elif command_lower == "whoami":
            return "user"
        elif command_lower == "uname -a":
            return "Linux demo-server 5.4.0-generic #106-Ubuntu SMP Thu Jan 6 23:58:14 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux"
        elif command_lower == "ps aux":
            return """USER       PID %CPU %MEM    VSZ   RSS TSTAT START   TIME COMMAND
user         1  0.0  0.1 225836  9216 ?        Ss   Jan15   0:02 /sbin/init
user        87 0.0 0.3 201532 24784 ?        Ss   Jan15   0:00 sshd: [listener]"""
        elif command_lower.startswith("cat /etc/passwd"):
            return """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin"""
        elif command_lower.startswith("rm -rf") or command_lower.startswith("rm -rf /"):
            return """rm: cannot remove '/': Permission denied
rm: cannot remove '/*': Permission denied"""
        else:
            return f"-bash: {command.split()[0] if command.split() else command}: command not found"

    async def handle_client(self, client_socket, addr):
        """Handle client connection"""
        ip = addr[0]
        logger.info(f"New connection from {ip}")
        
        try:
            # Send welcome
            welcome_msg = b"Welcome to Industrial SSH Server v2.4.7\r\nLast login: Mon Jan 15 10:30:45 2024\r\n[user@server ~]# "
            client_socket.send(welcome_msg)
            
            while True:
                # Receive command
                data = client_socket.recv(1024)
                if not data:
                    break
                
                command = data.decode('utf-8', errors='ignore').strip()
                if not command:
                    continue
                
                logger.info(f"Command from {ip}: {command}")
                
                # Analyze threat
                threat_level, score = self.analyze_threat_level(command)
                
                # Log session
                session = self.log_session(ip, command, threat_level, score)
                
                # Generate response
                response = self.generate_response(command)
                
                # Send response
                client_socket.send(f"{response}\r\n[user@server ~]# ".encode())
                
                # Send Telegram alert for high threats
                if threat_level in ["HIGH", "CRITICAL"]:
                    self.send_telegram_alert(command, ip, threat_level, score)
                    
        except Exception as e:
            logger.error(f"Client {ip} error: {e}")
        finally:
            client_socket.close()
            logger.info(f"Connection {ip} closed")

    def send_telegram_alert(self, command, ip, threat_level, score):
        """Send Telegram alert"""
        try:
            import requests
            
            # Load Telegram credentials from environment variables
            import os
            from dotenv import load_dotenv
            
            load_dotenv()
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            chat_id = os.getenv("TELEGRAM_CHAT_ID")
            
            # Check if Telegram credentials are configured
            if not bot_token or not chat_id:
                logger.warning("Telegram credentials not configured. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
                return
            
            emoji = "🚨" if threat_level == "CRITICAL" else "⚠️"
            message = f"""{emoji} AIML Honeypot Alert!

🌍 Source IP: {ip}
🔍 Threat Level: {threat_level}
💻 Command: {command}
📊 Score: {score:.3f}
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🤖 Detected by AIML Honeypot"""

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=payload, timeout=5)
            if response.json().get("ok"):
                logger.info(f"Telegram alert sent for {ip}")
            else:
                logger.error(f"Telegram alert failed: {response.json()}")
                
        except Exception as e:
            logger.error(f"Telegram alert error: {e}")

    async def run_server(self):
        """Start the honeypot server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        
        logger.info(f"🚀 Simple AIML Honeypot listening on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, addr = server.accept()
                asyncio.create_task(self.handle_client(client_socket, addr))
        except KeyboardInterrupt:
            logger.info("Shutting down honeypot...")
        finally:
            server.close()

    def run(self):
        """Main run method"""
        logger.info("Starting Simple AIML Honeypot...")
        asyncio.run(self.run_server())

if __name__ == "__main__":
    honeypot = SimpleHoneypot()
    honeypot.run()

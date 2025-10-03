#!/usr/bin/env python3
"""
Connection Handler for AIML Honeypot
Handles command responses and logging
"""

import asyncio
import os
import json
import csv
from datetime import datetime
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ConnectionHandler:
    """Handles connection processing and response generation"""
    
    def __init__(self):
        self.sessions_log = "/app/data/sessions.json"
        self.commands_log = "/app/data/commands.json"
        self.tsv_log = "/app/data/commands.tsv"
        self._ensure_log_files()

    def _ensure_log_files(self):
        """Ensure log files exist"""
        os.makedirs(os.path.dirname(self.sessions_log), exist_ok=True)
        
        # Initialize files if they don't exist
        for log_file in [self.sessions_log, self.commands_log]:
            if not os.path.exists(log_file):
                with open(log_file, 'w') as f:
                    json.dump([], f)

        # Initialize CSV/TSV if needed
        if not os.path.exists(self.tsv_log):
            with open(self.tsv_log, 'w') as f:
                f.write("timestamp\tip\tcommand\tthreat_level\tanomaly_score\n")

    async def log_command(self, command: str, ip: str, analysis: Dict[str, Any]):
        """Log command with analysis results"""
        try:
            timestamp = datetime.now().isoformat()
            session_id = f"{ip}_{int(datetime.now().timestamp())}"
            
            # Create session entry
            session_entry = {
                "session_id": session_id,
                "timestamp": timestamp,
                "ip": ip,
                "command": command,
                "analysis": analysis,
                "threat_level": analysis.get("threat_level", "UNKNOWN"),
                "anomaly_score": analysis.get("anomaly_score", 0.0)
            }
            
            # Append to JSON logs
            await self._append_to_json(self.sessions_log, session_entry)
            await self._append_to_json(self.commands_log, {
                "timestamp": timestamp,
                "ip": ip,
                "command": command,
                "threat_level": analysis.get("threat_level", "UNKNOWN"),
                "anomaly_score": analysis.get("anomaly_score", 0.0)
            })
            
            # Append to TSV for analysis
            await self._append_to_tsv(
                timestamp, ip, command, 
                analysis.get("threat_level", "UNKNOWN"),
                analysis.get("anomaly_score", 0.0)
            )
            
            logger.info(f"Logged command: {command} from {ip} (Threat: {analysis.get('threat_level')})")
            
        except Exception as e:
            logger.error(f"Error logging command: {e}")

    async def _append_to_json(self, file_path: str, data: Dict[str, Any]):
        """Append data to JSON log file"""
        try:
            # Read existing data
            with open(file_path, 'r') as f:
                logs = json.load(f)
            
            # Add new entry
            logs.append(data)
            
            # Keep only last 10000 entries to prevent file bloat
            if len(logs) > 10000:
                logs = logs[-10000:]
            
            # Write back
            with open(file_path, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error appending to {file_path}: {e}")

    async def _append_to_tsv(self, timestamp: str, ip: str, command: str, threat_level: str, score: float):
        """Append to TSV log for easy parsing"""
        try:
            with open(self.tsv_log, 'a') as f:
                # Escape tabs and newlines in command
                safe_command = command.replace('\t', '\\t').replace('\n', '\\n')
                f.write(f"{timestamp}\t{ip}\t{safe_command}\t{threat_level}\t{score}\n")
        except Exception as e:
            logger.error(f"Error appending to TSV: {e}")

    async def generate_response(self, command: str, analysis: Dict[str, Any]) -> str:
        """Generate realistic response based on command and threat level"""
        threat_level = analysis.get("threat_level", "LOW")
        
        # Get base response
        response = self._get_command_response(command.strip())
        
        # Add threat-based delays and additional output
        if threat_level in ["HIGH", "CRITICAL"]:
            # Add suspicious behavior indicators
            response += self._add_suspicious_output(command)
        elif threat_level == "MEDIUM":
            response += self._add_warning_output(command)
        
        # Add prompt
        response += "\n[root@server ~]# "
        
        return response

    def _get_command_response(self, command: str) -> str:
        """Get realistic response for command"""
        command_lower = command.lower()
        
        # File operations
        if command_lower.startswith("ls"):
            if "-la" in command_lower or "-a" in command_lower:
                return """total 84
drwxr-xr-x 22 root root  4096 Jan 15 10:30 .
drwxr-xr-x 23 root root  4096 Dec 23 08:15 ..
-rw-------  1 root root  1234 Jan 14 09:20 .bash_history
-rw-r--r--  1 root root  2043 Jan 01 00:00 .bashrc
drwxr-xr-x  2 root root  4096 Nov 30 12:45 backups
-rwxr-xr-x  1 root root  8192 Jan 02 15:20 cronjob.sh
drwxr-xr-x  3 root root  4096 Dec 15 14:30 data
-rw-r--r--  1 root root  1024 Jan 10 18:30 config.ini
-rwxr-xr-x  1 root root  4096 Dec 28 16:45 deploy.sh
drwxr-xr-x  2 root root  4096 Jan 05 11:20 logs
drwxrwxr-x  2 root root  4096 Dec 20 09:15 temp
-rwxr-xr-x  1 root root  2048 Jan 12 13:25 update.sh
-rwxr-xr-x  1 root root  512  Dec 18 07:30 watchdog.sh"""
            else:
                return """backups  config.ini  cronjob.sh  data  deploy.sh  logs  temp  update.sh  watchdog.sh"""
        
        elif command_lower == "pwd":
            return "/root"
        
        elif command_lower == "whoami":
            return "root"
        
        elif command_lower.startswith("uname"):
            return "Linux server 5.4.0-94-generic #106-Ubuntu SMP Thu Jan 6 23:58:14 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux"
        
        elif command_lower == "id":
            return "uid=0(root) gid=0(root) groups=0(root)"
        
        elif command_lower.startswith("ps aux"):
            return """USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 225836  9216 ?        Ss   Jan15   0:02 /sbin/init
root         2  0.0  0.0      0     0 ?        S    Jan15   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        I<   Jan15   0:00 [rcu_gp]
root         4  0.0  0.0      0     0 ?        I<   Jan15   0:00 [rcu_par_gp]
root         5  0.0  0.0      0     0 ?        I<   Jan15   0:00 [netns]
root        87 0.0 0.3 201532 24784 ?        Ss   Jan15   0:00 sshd: /usr/sbin/sshd [listener] 
root       234 0.0 0.1 185268  8504 ?        Ss   Jan15   0:00 crond"""
        
        elif command_lower.startswith("cat /etc/passwd"):
            return """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin"""
        
        elif command_lower.startswith("netstat"):
            return """Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN     
tcp6       0      0 :::22                    :::*                    LISTEN     
tcp6       0      0 :::80                    :::*                    LISTEN"""
        
        elif command_lower.startswith("curl") or command_lower.startswith("wget"):
            return """Connected to example.com (93.184.216.34:80)
HTTP/1.1 200 OK
Date: Mon, 15 Jan 2024 10:30:45 GMT
Server: nginx/1.18.0
Content-Type: text/html; charset=UTF-8

<html>
<head><title>Welcome to Example Server</title></head>
<body><h1>Server is running</h1></body>
</html>"""
        
        elif command_lower.startswith("python"):
            return "Python 3.8.10 (default, Jun 22 2022, 20:18:18)\n[GCC 9.4.0] on linux"
        
        elif command_lower.startswith("date"):
            return f"Mon Jan 15 {datetime.now().strftime('%H:%M:%S')} UTC 2024"
        
        elif command_lower.startswith("uptime"):
            return f" 10:30:45 up 23 days, 8:45, 1 user, load average: 0.08, 0.03, 0.00"
        
        elif command_lower.startswith("free"):
            return """              total        used        free      shared  buff/cache   available
Mem:        8053068     2048560     1234567       245678     4770941     3456789
Swap:       2097148           0     2097148"""
        
        elif command_lower.startswith("df"):
            return """Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       20G  8.5G   11G  45% /
/dev/sda2        8G  2.1G  5.9G  27% /var
tmpfs          3.9G     0  3.9G   0% /dev/shm"""
        
        elif command_lower.startswith("history"):
            return """   1  ls -la
   2  whoami  
   3  pwd
   4  date
   5  uptime
   6  ps aux"""
        
        elif command_lower.startswith("env"):
            return """PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TERM=xterm-256color
SHELL=/bin/bash
HOME=/root
USER=root
PWD=/root"""
        
        elif command_lower.startswith("echo"):
            # Echo back the message
            echo_msg = command[4:].strip()
            return f'"{echo_msg}"'
        
        elif command_lower.startswith("touch"):
            filename = command[5:].strip()
            return f"touch: creating file '{filename}': Permission denied"
        
        elif command_lower.startswith("mkdir"):
            return "mkdir: cannot create directory 'test': File exists"
        
        elif command_lower.startswith("rm"):
            return "rm: cannot remove '/root/test': No such file or directory"
        
        elif command_lower.startswith("su ") or command_lower.startswith("sudo"):
            return "Authenticate as super user:"
        
        else:
            # Generic response for unknown commands
            return f"-bash: {command.split()[0]}: command not found"

    def _add_suspicious_output(self, command: str) -> str:
        """Add suspicious indicators for high-threat commands"""
        indicators = [
            "\nWarning: Suspicious activity detected",
            "\nSystem integrity check initiated...",
            "\nAccess denied to secure component",
            "\n[ALERT] Security module activated",
            "\nMonitoring command execution..."
        ]
        
        # Add random indicator
        import random
        return random.choice(indicators)

    def _add_warning_output(self, command: str) -> str:
        """Add warning indicators for medium-threat commands"""
        warnings = [
            "\nNote: Command logged for security audit",
            "\nWarning: Unusual command pattern detected",
            "\nSystem monitoring active"
        ]
        
        # Add random warning
        import random
        return random.choice(warnings)

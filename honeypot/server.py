#!/usr/bin/env python3
"""
AIML Honeypot Server
Advanced SSH/Telnet honeypot with AI-powered threat detection
"""

import asyncio
import logging
import os
import sys
import signal
from datetime import datetime
from typing import List, Optional

# Add current directory to path
sys.path.append('/app')

from handlers import ConnectionHandler
from ai_analysis import AIAnalyzer
from telegram_alert import TelegramManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/honeypot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class HoneypotServer:
    """Advanced AI-powered honeypot server"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 2222):
        self.host = host
        self.port = port
        self.handler = ConnectionHandler()
        self.ai_analyzer = AIAnalyzer()
        self.telegram_manager = TelegramManager()
        self.server = None
        self.active_connections = []
        self.stats = {
            "connections": 0,
            "commands": 0,
            "threats": 0,
            "start_time": datetime.now().isoformat()
        }
        
        # Signal handlers for gracefulutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        if self.server:
            self.server.close()
            asyncio.create_task(self._shutdown())

    async def _shutdown(self):
        """Shutdown server gracefully"""
        logger.info("Closing active connections...")
        for connection in self.active_connections:
            try:
                connection.close()
            except:
                pass
        self.active_connections.clear()

    async def handle_client(self, reader, writer):
        """Handle new client connections"""
        client_addr = writer.get_extra_info('peername')
        connection_id = f"{client_addr[0]}:{client_addr[1]}"
        
        logger.info(f"New connection from {connection_id}")
        self.stats["connections"] += 1
        self.active_connections.append(writer)
        
        try:
            # Send welcome message
            welcome_msg = b"""Welcome to Industrial SSH Server v2.4.7
Last login: Mon Jan 15 10:30:45 2024 from 192.168.1.100
[root@server ~]# """
            writer.write(welcome_msg)
            await writer.drain()

            # Handle command loop
            while True:
                try:
                    # Read command
                    data = await reader.readline()
                    if not data:
                        break
                    
                    command = data.decode('utf-8', errors='ignore').strip()
                    if not command:
                        writer.write(b"[root@server ~]# ")
                        await writer.drain()
                        continue

                    logger.info(f"Command from {connection_id}: {command}")
                    self.stats["commands"] += 1

                    # Analyze command with AI
                    analysis = await self.ai_analyzer.analyze_command(command, client_addr[0])
                    
                    # Log command to files
                    await self.handler.log_command(command, client_addr[0], analysis)
                    
                    # Generate realistic response
                    response = await self.handler.generate_response(command, analysis)
                    
                    # Send response
                    writer.write(response.encode('utf-8'))
                    await writer.drain()
                    
                    # Send alert if high threat
                    if analysis["threat_level"] in ["HIGH", "CRITICAL"]:
                        await self.telegram_manager.send_alert(
                            command, client_addr[0], analysis["threat_level"], 
                            analysis["anomaly_score"]
                        )
                        self.stats["threats"] += 1
                        
                        # Send alert to backend API
                        await self._notify_backend(command, client_addr[0], analysis)

                except Exception as e:
                    logger.error(f"Error handling command from {connection_id}: {e}")
                    break

        except Exception as e:
            logger.error(f"Connection error from {connection_id}: {e}")
        finally:
            # Clean up connection
            if writer in self.active_connections:
                self.active_connections.remove(writer)
            writer.close()
            await writer.wait_closed()
            logger.info(f"Connection {connection_id} closed")

    async def _notify_backend(self, command: str, ip: str, analysis):
        """Notify backend API about high-threat command"""
        try:
            import requests
            data = {
                "command": command,
                "ip": ip,
                "threat_level": analysis["threat_level"],
                "anomaly_score": analysis["anomaly_score"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Try to notify backend (may not be available)
            response = requests.post(
                "http://backend:8000/analyze", 
                json=data,
                timeout=2
            )
            logger.info(f"Notified backend API: {response.status_code}")
            
        except Exception as e:
            logger.debug(f"Could not notify backend: {e}")

    async def start_server(self):
        """Start the honeypot server"""
        try:
            self.server = await asyncio.start_server(
                self.handle_client, 
                self.host, 
                self.port
            )
            
            addr = self.server.sockets[0].getsockname()
            logger.info(f"🚀 AIML Honeypot is listening on {addr[0]}:{addr[1]}")
            logger.info(f"📊 Starting with stats: {self.stats}")
            
            # Log startup info
            startup_msg = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                        🚀 AIML HONEYPOT                          ║
║                     Advanced AI/ML Honeypot                        ║
╠═══════════════════════════════════════════════════════════════════╣
║ Host: {self.host:<15} │ Port: {self.port:<5} │ Status: 🟢 ACTIVE    ║
║ AI Model: {'🔧 LOADED' if self.ai_analyzer.has_model() else '⚠️ NOT LOADED':<20} │ Alerts: {'✅ ENABLED' if self.telegram_manager.is_configured() else '❌ DISABLED':<15} ║
╚═══════════════════════════════════════════════════════════════════╝
            """
            logger.info(startup_msg)
            
            async with self.server:
                await self.server.serve_forever()
                
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise

    async def get_stats(self):
        """Get server statistics"""
        return {
            **self.stats,
            "active_connections": len(self.active_connections),
            "uptime": str(datetime.now() - datetime.fromisoformat(self.stats["start_time"])),
            "ai_model_loaded": self.ai_analyzer.has_model(),
            "telegram_configured": self.telegram_manager.is_configured()
        }

async def main():
    """Main server function"""
    server = HoneypotServer()
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        logger.info("Shutting down honeypot server...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure necessary directories exist
    os.makedirs("/app/data", exist_ok=True)
    os.makedirs("/app/models", exist_ok=True)
    os.makedirs("/app/logs", exist_ok=True)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

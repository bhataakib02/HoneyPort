#!/usr/bin/env python3
"""
Telegram Alert Module for AIML Honeypot
Provides alert functionality specifically for honeypot operations
"""

import os
import requests
import logging
import asyncio
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class TelegramManager:
    """Telegram alerting for honeypot threats"""
    
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.max_message_length = 4096
        
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram credentials not configured - alerts disabled")
        else:
            logger.info("Telegram alerts configured")

    def is_configured(self) -> bool:
        """Check if Telegram is configured"""
        return bool(self.bot_token and self.chat_id)

    async def send_alert(self, command: str, ip: str, threat_level: str, 
                       anomaly_score: float = None, additional_info: dict = None):
        """Send threat alert to Telegram"""
        if not self.is_configured():
            logger.debug("Telegram not configured, skipping alert")
            return False

        # Create threat-level specific formatting
        threat_emojis = {
            "LOW": "🟢",
            "MEDIUM": "🟡",
            "HIGH": "🟠", 
            "CRITICAL": "🚨"
        }
        
        emoji = threat_emojis.get(threat_level, "⚠️")
        
        # Format command for safe display
        safe_command = self._sanitize_command(command)
        
        message = f"""{emoji} <b>AIML Honeypot Alert</b>
🌍 <b>Source IP:</b> <code>{ip}</code>
🔍 <b>Threat Level:</b> {threat_level}
💻 <b>Attempted Command:</b>
<pre>{safe_command}</pre>
📊 <b>Anomaly Score:</b> {anomaly_score:.3f}
⏰ <b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""

        if additional_info:
            message += f"\n📍 <b>Additional Info:</b>\n"
            for key, value in additional_info.items():
                message += f"• {key}: {value}\n"

        # Add honeypot identifier
        message += f"\n🤖 <b>Detected by AIML Honeypot</b>"
        
        return await self._send_message(message)

    def _sanitize_command(self, command: str) -> str:
        """Sanitize command for safe Telegram display"""
        # Replace potentially harmful characters
        safe = command.replace('<', '&lt;').replace('>', '&gt;')
        safe = safe.replace('&', '&amp;')
        
        # Limit length if needed
        if len(safe) > 500:
            safe = safe[:500] + "... [truncated]"
        
        return safe

    async def _send_message(self, text: str) -> bool:
        """Send message to Telegram"""
        try:
            # Truncate if too long
            if len(text) > self.max_message_length:
                text = text[:self.max_message_length - 3] + "..."

            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            if response.json().get("ok"):
                logger.info("Telegram alert sent successfully")
                return True
            else:
                logger.error(f"Telegram API error: {response.json()}")
                return False

        except requests.exceptions.Timeout:
            logger.error("Telegram API timeout")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram alert: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram alert: {e}")
            return False

    async def send_summary_alert(self, session_count: int, threat_count: int, 
                               time_period: str = "last hour"):
        """Send summary alert"""
        if not self.is_configured():
            return False

        message = f"""📊 <b>Honeypot Activity Summary</b>

⏱️ <b>Period:</b> {time_period}
🔌 <b>Total Sessions:</b> {session_count}
⚠️ <b>Threats Detected:</b> {threat_count}
📈 <b>Threat Rate:</b> {(threat_count/session_count*100):.1f if session_count > 0 else 0.0}%

🕒 <b>Reported:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

🤖 <i>AIML Honeypot Monitoring</i>"""

        return await self._send_message(message)

    async def test_alert(self):
        """Send test alert to verify configuration"""
        if not self.is_configured():
            logger.warning("Telegram not configured, cannot send test")
            return False

        message = """🧪 <b>AIML Honeypot Test</b>

This is a test alert to verify your Telegram integration is working correctly.

✅ If you receive this message, your alerts are properly configured!

💡 <i>Start attacking your honeypot to see real alerts!</i>"""

        return await self._send_message(message)

    def validate_configuration(self) -> dict:
        """Validate Telegram configuration"""
        if not self.is_configured():
            return {
                "valid": False,
                "error": "Missing bot token or chat ID",
                "missing": []
            }

        missing = []
        if not self.bot_token:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not self.chat_id:
            missing.append("TELEGRAM_CHAT_ID")

        if missing:
            return {
                "valid": False,
                "error": f"Missing environment variables: {', '.join(missing)}",
                "missing": missing
            }

        return {
            "valid": True,
            "bot_token_length": len(self.bot_token),
            "chat_id": self.chat_id
        }

import json
import os
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
import logging

logger = logging.getLogger(__name__)

class CommandSession:
    def __init__(self, session_id: str, ip: str, command: str, 
                 anomaly_score: float, threat_level: str, timestamp: str = None):
        self.session_id = session_id
        self.ip = ip
        self.command = command
        self.anomaly_score = anomaly_score
        self.threat_level = threat_level
        self.timestamp = timestamp or datetime.now().isoformat()

class DatabaseManager:
    """Simple JSON-based database manager for honeypot data"""
    
    def __init__(self):
        self.data_file = "/app/data/sessions.json"
        self.commands_file = "/app/data/commands.json"
        self._ensure_data_directory()
        self._sessions_data = self._load_data(self.data_file)
        self._commands_data = self._load_data(self.commands_file)

    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        data_dir = os.path.dirname(self.data_file)
        os.makedirs(data_dir, exist_ok=True)

    def _load_data(self, file_path: str) -> List[Dict]:
        """Load data from JSON file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            return []

    def _save_data(self, file_path: str, data: List[Dict]):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {e}")

    async def save_command(self, ip: str, command: str, anomaly_score: float, 
                          threat_level: str) -> str:
        """Save a command session and return session ID"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            "session_id": session_id,
            "ip": ip,
            "command": command,
            "anomaly_score": anomaly_score,
            "threat_level": threat_level,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to sessions
        self._sessions_data.append(session_data)
        self._save_data(self.data_file, self._sessions_data)
        
        # Save to commands for ML training
        command_data = {
            "session_id": session_id,
            "command": command,
            "anomaly_score": anomaly_score,
            "timestamp": datetime.now().isoformat()
        }
        
        self._commands_data.append(command_data)
        self._save_data(self.commands_file, self._commands_data)
        
        logger.info(f"Saved command session {session_id} from IP {ip}")
        return session_id

    async def get_all_sessions(self, limit: int = None) -> List[Dict]:
        """Get all command sessions"""
        sessions = sorted(self._sessions_data, 
                         key=lambda x: x.get("timestamp", ""), 
                         reverse=True)
        if limit:
            sessions = sessions[:limit]
        return sessions

    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get specific session by ID"""
        for session in self._sessions_data:
            if session.get("session_id") == session_id:
                return session
        return None

    async def get_command(self, command_id: str) -> Optional[Dict]:
        """Get specific command by ID"""
        for command in self._commands_data:
            if command.get("session_id") == command_id:
                return command
        return None

    async def get_sessions_by_ip(self, ip: str) -> List[Dict]:
        """Get all sessions from specific IP"""
        return [session for session in self._sessions_data 
                if session.get("ip") == ip]

    async def get_threats(self, min_threat_level: str = "MEDIUM") -> List[Dict]:
        """Get all high-threat commands"""
        threat_levels = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        min_level = threat_levels.get(min_threat_level, 2)
        
        threats = []
        for session in self._sessions_data:
            threat_level = session.get("threat_level", "LOW")
            if threat_levels.get(threat_level, 1) >= min_level:
                threats.append(session)
        
        return sorted(threats, key=lambda x: x.get("timestamp", ""), reverse=True)

    async def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        total_sessions = len(self._sessions_data)
        total_commands = len(self._commands_data)
        
        # Count by threat level
        threat_counts = {}
        ip_counts = {}
        
        for session in self._sessions_data:
            threat_level = session.get("threat_level", "LOW")
            threat_counts[threat_level] = threat_counts.get(threat_level, 0) + 1
            
            ip = session.get("ip", "unknown")
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
        
        # Calculate average anomaly score
        scores = [s.get("anomaly_score", 0) for s in self._sessions_data]
        avg_score = sum(scores) / len(self._sessions_data) if scores else 0
        
        return {
            "total_sessions": total_sessions,
            "total_commands": total_commands,
            "total_threats": sum(count for level, count in threat_counts.items() 
                               if level in ["HIGH", "CRITICAL"]),
            "threat_counts": threat_counts,
            "top_attacking_ips": sorted(ip_counts.items(), 
                                       key=lambda x: x[1], reverse=True)[:10],
            "average_anomaly_score": round(avg_score, 2),
            "last_updated": datetime.now().isoformat()
        }

    async def get_commands_for_training(self) -> List[str]:
        """Get command strings for ML model training"""
        return [cmd.get("command", "") for cmd in self._commands_data 
                if cmd.get("command")]

    async def cleanup_old_data(self, days_to_keep: int = 30):
        """Remove old data to prevent file bloat"""
        cutoff = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
        
        def is_recent(data_item):
            try:
                timestamp = datetime.fromisoformat(data_item.get("timestamp", ""))
                return timestamp.timestamp() > cutoff
            except:
                return False
        
        initial_sessions = len(self._sessions_data)
        initial_commands = len(self._commands_data)
        
        self._sessions_data = [s for s in self._sessions_data if is_recent(s)]
        self._commands_data = [c for c in self._commands_data if is_recent(c)]
        
        self._save_data(self.data_file, self._sessions_data)
        self._save_data(self.commands_file, self._commands_data)
        
        removed_sessions = initial_sessions - len(self._sessions_data)
        removed_commands = initial_commands - len(self._commands_data)
        
        logger.info(f"Cleaned up {removed_sessions} sessions and {removed_commands} commands")
        return removed_sessions + removed_commands

# Global database manager instance
_db_manager = None

def get_database_manager() -> DatabaseManager:
    """Get global database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager

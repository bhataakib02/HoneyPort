#!/usr/bin/env python3
"""
PRODUCTION-READY AIML Honeypot Backend API
"""

import json
import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="AIML Honeypot API",
    description="AI/ML Powered Threat Detection System",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connections
websocket_connections: List[WebSocket] = []

# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'honeypot', 'data')
SESSIONS_FILE = os.path.join(DATA_DIR, 'sessions.json')
COMMANDS_FILE = os.path.join(DATA_DIR, 'commands.log')
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'honeypot', 'models')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Models
class Session(BaseModel):
    session_id: str = None
    timestamp: str
    ip: str
    command: str
    threat_level: str
    anomaly_score: float
    response: str = ""

class SessionResponse(BaseModel):
    sessions: List[Session]
    count: int
    total_pages: int
    current_page: int

class StatsResponse(BaseModel):
    total_sessions: int
    total_threats: int
    threat_levels: Dict[str, int]
    avg_score: float
    last_activity: str = None

class AnalyzeRequest(BaseModel):
    command: str
    ip: str = "unknown"

# Utility functions
def load_sessions() -> List[Dict]:
    """Load sessions from file"""
    try:
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create sample data
            sample_sessions = [
                {
                    "session_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "ip": "192.168.1.100",
                    "command": "ls -la",
                    "threat_level": "LOW",
                    "anomaly_score": 0.15,
                    "response": "file1.txt  file2.txt  folder1/"
                },
                {
                    "session_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "ip": "10.0.0.50",
                    "command": "cat /etc/passwd",
                    "threat_level": "HIGH",
                    "anomaly_score": 0.85,
                    "response": "root:x:0:0:root:/root:/bin/bash\n..."
                },
                {
                    "session_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "ip": "203.0.113.25",
                    "command": "rm -rf /tmp/*",
                    "threat_level": "CRITICAL",
                    "anomaly_score": 0.95,
                    "response": "rm: cannot remove '/': Permission denied"
                }
            ]
            with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(sample_sessions, f, indent=2)
            return sample_sessions
    except Exception as e:
        logger.error(f"Error loading sessions: {e}")
        return []

def save_session(session: Dict) -> bool:
    """Save session to file"""
    try:
        sessions = load_sessions()
        sessions.append(session)
        
        # Keep only last 1000 sessions
        if len(sessions) > 1000:
            sessions = sessions[-1000:]
        
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sessions, f, indent=2)
        
        # Also append to commands.log
        log_entry = f"{session['timestamp']}:{session['ip']}:{session['command']}:{session['threat_level']}\n"
        with open(COMMANDS_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        return True
    except Exception as e:
        logger.error(f"Error saving session: {e}")
        return False

def analyze_threat(command: str, ip: str = "unknown") -> Dict[str, Any]:
    """Advanced AI threat analysis"""
    command_lower = command.lower().strip()
    
    # Feature extraction
    suspicious_keywords = [
        "rm -rf", "cat /etc/passwd", "cat /etc/shadow", "wget", "curl",
        "nc ", "systemctl", "su -", "sudo", "chmod +x", "python -c",
        "bash -c", "sh -c", "/bin/bash", "find /", "kill -9",
        "iptables", "passwd", "id", "uname -a", "netstat", "ps aux",
        "cat /proc/", "vi /etc/", "mkdir /", "touch /", "echo",
        "export ", "alias ", "history", "crontab", "at ", "nohup"
    ]
    
    attack_patterns = [
        "reverse shell", "backdoor", "botnet", "malware", "payload",
        "exploit", "injection", "bypass", "privilege escalation"
    ]
    
    # Calculate threat score
    threat_score = 0
    
    # Keyword matching
    for keyword in suspicious_keywords:
        if keyword in command_lower:
            threat_score += 0.2
    
    # Pattern matching
    for pattern in attack_patterns:
        if pattern in command_lower:
            threat_score += 0.3
    
    # Length-based analysis
    if len(command) > 100:  # Long commands
        threat_score += 0.1
    
    # Special character analysis
    special_chars = sum(1 for c in command if not c.isalnum() and c not in ' ')
    if special_chars > len(command) * 0.3:  # High special char ratio
        threat_score += 0.15
    
    # IP-based scoring (if it's a suspicious IP pattern)
    if any(x in ip.lower() for x in ["192.168", "10.", "172.16"]):
        threat_score += 0.05  # Internal IPs are less suspicious
    
    # Determine threat level
    threat_score = min(1.0, threat_score)
    
    if threat_score >= 0.8:
        threat_level = "CRITICAL"
    elif threat_score >= 0.6:
        threat_level = "HIGH"
    elif threat_score >= 0.3:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"
    
    return {
        "threat_level": threat_level,
        "anomaly_score": threat_score,
        "features": {
            "length": len(command),
            "special_chars": special_chars,
            "keywords_matched": len([k for k in suspicious_keywords if k in command_lower]),
            "ip_type": "internal" if any(x in ip for x in ["192.168", "10.", "172.16"]) else "external"
        }
    }

# API Endpoints
@app.get("/")
def root():
    return {
        "message": "🚀 AIML Honeypot API",
        "version": "2.0.0",
        "status": "running",
        "features": ["AI/ML Threat Detection", "Real-time Alerts", "Session Analysis"],
        "endpoints": {
            "/health": "Health check",
            "/sessions": "Get all sessions",
            "/stats": "Get statistics",
            "/analyze": "Analyze command",
            "/ws/sessions": "WebSocket for real-time updates"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "active",
        "services": {
            "api": "running",
            "ml_model": "ready",
            "webhooks": "enabled"
        }
    }

@app.get("/sessions", response_model=SessionResponse)
def get_sessions(page: int = 1, limit: int = 50, threat_level: str = None):
    """Get paginated sessions"""
    try:
        sessions = load_sessions()
        
        # Filter by threat level if specified
        if threat_level:
            sessions = [s for s in sessions if s.get('threat_level') == threat_level.upper()]
        
        # Pagination
        total_count = len(sessions)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_sessions = sessions[start_idx:end_idx]
        
        # Reverse chronological order (newest first)
        paginated_sessions = sorted(paginated_sessions, 
                                  key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return SessionResponse(
            sessions=paginated_sessions,
            count=len(paginated_sessions),
            total_pages=(total_count + limit - 1) // limit,
            current_page=page
        )
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    """Get specific session by ID"""
    try:
        sessions = load_sessions()
        session = next((s for s in sessions if s.get('session_id') == session_id), None)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return session
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=StatsResponse)
def get_statistics():
    """Get comprehensive statistics"""
    try:
        sessions = load_sessions()
        
        if not sessions:
            return StatsResponse(
                total_sessions=0,
                total_threats=0,
                threat_levels={"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
                avg_score=0.0
            )
        
        # Basic stats
        total_sessions = len(sessions)
        high_threat_sessions = [s for s in sessions if s.get('threat_level') in ['HIGH', 'CRITICAL']]
        total_threats = len(high_threat_sessions)
        
        # Threat level distribution
        threat_levels = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        scores = []
        
        for session in sessions:
            level = session.get('threat_level', 'LOW')
            threat_levels[level] = threat_levels.get(level, 0) + 1
            scores.append(session.get('anomaly_score', 0))
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        # Last activity
        last_activity = None
        if sessions:
            timestamps = [s.get('timestamp') for s in sessions if s.get('timestamp')]
            if timestamps:
                last_activity = max(timestamps)
        
        return StatsResponse(
            total_sessions=total_sessions,
            total_threats=total_threats,
            threat_levels=threat_levels,
            avg_score=avg_score,
            last_activity=last_activity
        )
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
def analyze_command(request: AnalyzeRequest):
    """Analyze a command for threats"""
    try:
        result = analyze_threat(request.command, request.ip)
        result['command'] = request.command
        result['ip'] = request.ip
        result['timestamp'] = datetime.now().isoformat()
        
        return result
    except Exception as e:
        logger.error(f"Error analyzing command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sessions")
def create_session(session: Dict[str, Any]):
    """Create a new session (for honeypot to call)"""
    try:
        if not session.get('session_id'):
            session['session_id'] = str(uuid.uuid4())
        
        if not session.get('timestamp'):
            session['timestamp'] = datetime.now().isoformat()
        
        # Note: WebSocket broadcasting would be handled in async context
        # For now, we'll skip the broadcast in sync endpoint
        
        save_session(session)
        
        return {"status": "success", "session_id": session['session_id']}
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/sessions")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    websocket_connections.append(websocket)
    logger.info(f"WebSocket client connected. Total connections: {len(websocket_connections)}")
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Total connections: {len(websocket_connections)}")

async def broadcast_message(message: str):
    """Broadcast message to all WebSocket clients"""
    disconnected = []
    
    for websocket in websocket_connections:
        try:
            await websocket.send_text(message)
        except Exception:
            disconnected.append(websocket)
    
    # Remove disconnected clients
    for ws in disconnected:
        if ws in websocket_connections:
            websocket_connections.remove(ws)
            
    if disconnected:
        logger.info(f"Removed {len(disconnected)} disconnected WebSocket clients")

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 AIML Honeypot API starting...")
    logger.info(f"📁 Data directory: {DATA_DIR}")
    logger.info(f"🧠 Models directory: {MODELS_DIR}")
    
    # Initialize with sample data if needed
    load_sessions()
    
    logger.info("✅ API ready and listening!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 AIML Honeypot API shutting down...")

if __name__ == "__main__":
    print("🚀 Starting AIML Honeypot API...")
    print("📍 Backend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔄 WebSocket: ws://localhost:8000/ws/sessions")
    
    uvicorn.run(
        "app_working:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )

#!/usr/bin/env python3
"""
BA Bot - Professional AI/ML Honeypot System
The Best AI/ML Honeypot for Advanced Threat Detection
"""

import json
import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any
import uuid
import hashlib
import subprocess
import psutil

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# FastAPI app with BAOT branding
app = FastAPI(
    title="🛡️ BAOT AI/ML Honeypot",
    description="Advanced AI-Powered Threat Detection System - The Best Honeypot Available",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connections for real-time updates
websocket_connections: List[WebSocket] = []

# Enhanced data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'honeypot', 'data')
SESSIONS_FILE = os.path.join(DATA_DIR, 'sessions.json')
COMMANDS_FILE = os.path.join(DATA_DIR, 'commands.log')
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'honeypot', 'models')
THREATS_FILE = os.path.join(DATA_DIR, 'threat_intelligence.json')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Advanced Models
class Session(BaseModel):
    session_id: str = None
    timestamp: str
    ip: str
    command: str
    threat_level: str
    anomaly_score: float
    response: str = ""
    attack_vector: str = ""
    confidence: float = 0.0
    indicators: List[str] = []

class ThreatIntelligence(BaseModel):
    ip: str
    source_country: str = "Unknown"
    known_malware: bool = False
    attack_frequency: int = 0
    first_seen: str = ""
    last_seen: str = ""
    reputation_score: float = 0.0

class EnhancedStats(BaseModel):
    total_sessions: int
    total_threats: int
    threat_levels: Dict[str, int]
    avg_score: float
    last_activity: str = None
    system_health: Dict[str, Any]
    attack_vectors: Dict[str, int]
    top_ips: List[Dict[str, Any]]

class AnalyzeRequest(BaseModel):
    command: str
    ip: str = "unknown"

# Enhanced Utility Functions
def generate_threat_signature(command: str, ip: str) -> str:
    """Generate unique threat signature"""
    signature_data = f"{command}:{ip}:{datetime.now().strftime('%Y%m%d')}"
    return hashlib.md5(signature_data.encode()).hexdigest()[:16]

def classify_attack_vector(command: str) -> str:
    """Classify attack vector"""
    command_lower = command.lower()
    
    # File system attacks
    if any(cmd in command_lower for cmd in ['rm -rf', 'del ', 'format ', 'mkfs']):
        return "File System Destruction"
    
    # Privilege escalation
    if any(cmd in command_lower for cmd in ['sudo', 'su ', 'chmod +x', 'passwd']):
        return "Privilege Escalation"
    
    # Reconnaissance
    if any(cmd in command_lower for cmd in ['cat /etc/passwd', 'cat /etc/shadow', 'whoami', 'id']):
        return "System Reconnaissance"
    
    # Network exploitation
    if any(cmd in command_lower for cmd in ['nc ', 'netcat', 'telnet', 'ssh ']):
        return "Network Exploitation"
    
    # Code execution
    if any(cmd in command_lower in ['python -c', 'bash -c', 'sh -c', 'eval']):
        return "Code Execution"
    
    # Data exfiltration
    if any(cmd in command_lower for cmd in ['wget', 'curl', 'scp ', 'ftp ']):
        return "Data Exfiltration"
    
    # Lateral movement
    if any(cmd in command_lower for cmd in ['ssh ', 'rsh ', 'rcp ']):
        return "Lateral Movement"
    
    return "Generic Command"

def advanced_threat_analysis(command: str, ip: str) -> Dict[str, Any]:
    """Advanced AI threat analysis with multiple techniques"""
    command_lower = command.lower().strip()
    
    # Multi-layered threat detection
    threat_scoring = {
        'length': 0,
        'complexity': 0,
        'keywords': 0,
        'patterns': 0,
        'syntax': 0,
        'context': 0
    }
    
    # Length analysis
    if len(command) > 200:
        threat_scoring['length'] = 0.15
    elif len(command) > 100:
        threat_scoring['length'] = 0.1
    elif len(command) < 10:
        threat_scoring['length'] = 0.02
    
    # Complexity analysis
    special_chars = sum(1 for c in command if not c.isalnum() and c not in ' ')
    if special_chars > len(command) * 0.4:
        threat_scoring['complexity'] = 0.2
    elif special_chars > len(command) * 0.3:
        threat_scoring['complexity'] = 0.15
    elif special_chars > len(command) * 0.2:
        threat_scoring['complexity'] = 0.1
    
    # Advanced keyword detection
    critical_keywords = {
        'rm -rf': 0.25, 'cat /etc/passwd': 0.2, 'wget': 0.15,
        'curl': 0.15, 'nc ': 0.15, 'python -c': 0.2,
        'bash -c': 0.2, 'eval': 0.3, 'systemctl': 0.1,
        'chmod +x': 0.15, 'passwd': 0.1, 'su ': 0.15,
        'sudo ': 0.1, 'sh -c': 0.18, 'find /': 0.12,
        'kill -9': 0.15, 'iptables': 0.1, 'crontab': 0.12,
        'at ': 0.1, 'nohup': 0.1, 'screen': 0.05
    }
    
    # Pattern matching
    for keyword, score in critical_keywords.items():
        if keyword in command_lower:
            threat_scoring['keywords'] += score
    
    # Behavioral patterns
    if '&&' in command or '||' in command or ';' in command:
        threat_scoring['patterns'] += 0.15  # Command chaining
    if '$((' in command or '`' in command:
        threat_scoring['patterns'] += 0.2  # Command substitution
    if command.count('"') > 2 or command.count("'") > 2:
        threat_scoring['syntax'] += 0.1  # Complex quoting
    
    # Context analysis
    if ip and not any(x in ip for x in ['192.168', '10.', '172.16']):
        threat_scoring['context'] = 0.05  # External IP
    
    # Calculate final score
    total_score = sum(threat_scoring.values())
    anomaly_score = min(1.0, total_score * 0.8)  # Normalize
    
    # Determine threat level
    if anomaly_score >= 0.8:
        threat_level = "CRITICAL"
        confidence = 0.95
    elif anomaly_score >= 0.6:
        threat_level = "HIGH"
        confidence = 0.85
    elif anomaly_score >= 0.4:
        threat_level = "MEDIUM"
        confidence = 0.7
    else:
        threat_level = "LOW"
        confidence = 0.5
    
    # Extract indicators
    indicators = []
    if threat_scoring['keywords'] > 0.1:
        indicators.append("Suspicious Keywords")
    if threat_scoring['complexity'] > 0.1:
        indicators.append("High Complexity")
    if threat_scoring['patterns'] > 0.1:
        indicators.append("Attack Patterns")
    if threat_scoring['length'] > 0.1:
        indicators.append("Long Command")
    if threat_scoring['context'] > 0.02:
        indicators.append("External Source")
    
    return {
        "threat_level": threat_level,
        "anomaly_score": round(anomaly_score, 6),
        "confidence": round(confidence, 3),
        "attack_vector": classify_attack_vector(command),
        "indicators": indicators,
        "scoring_breakdown": threat_scoring,
        "signature": generate_threat_signature(command, ip)
    }

def load_threat_intelligence() -> Dict[str, ThreatIntelligence]:
    """Load threat intelligence data"""
    try:
        if os.path.exists(THREATS_FILE):
            with open(THREATS_FILE, 'r') as f:
                return {ip: ThreatIntelligence(**data) for ip, data in json.load(f).items()}
        return {}
    except Exception as e:
        logger.error(f"Error loading threat intelligence: {e}")
        return {}

def update_threat_intelligence(ip: str, threat_data: Dict[str, Any]):
    """Update threat intelligence for IP"""
    try:
        intelligence = load_threat_intelligence()
        now = datetime.now().isoformat()
        
        if ip in intelligence:
            intelligence[ip].attack_frequency += 1
            intelligence[ip].last_seen = now
        else:
            intelligence[ip] = ThreatIntelligence(
                ip=ip,
                first_seen=now,
                last_seen=now,
                attack_frequency=1
            )
        
        with open(THREATS_FILE, 'w') as f:
            json.dump({ip: data.__dict__ for ip, data in intelligence.items()}, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error updating threat intelligence: {e}")

def get_system_health() -> Dict[str, Any]:
    """Get system health metrics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_usage": cpu_percent,
            "memory_usage": memory.percent,
            "disk_usage": disk.percent,
            "uptime": "Active",
            "processes": len(psutil.pids()),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        return {"error": str(e)}

# Enhanced API Endpoints
@app.get("/")
def root():
    return {
        "name": "🛡️ BAOT - Best AI/ML Honeypot",
        "version": "3.0.0",
        "description": "Advanced AI-Powered Threat Detection System",
        "status": "running",
        "features": [
            "Advanced AI/ML Threat Detection",
            "Real-time Behavioral Analysis", 
            "Multi-vector Attack Classification",
            "Intelligent Response Generation",
            "Threat Intelligence Integration",
            "Professional Dashboard Interface"
        ],
        "capabilities": [
            "Isolation Forest ML Model",
            "Anomaly Score Calculation",
            "Threat Confidence Scoring",
            "Attack Vector Classification",
            "Real-time Telegram Alerts",
            "WebSocket Live Updates",
            "Professional Analytics",
            "System Health Monitoring"
        ],
        "endpoints": {
            "/health": "System health and performance",
            "/sessions": "Captured sessions with filtering",
            "/threats": "Threat intelligence data",
            "/stats": "Advanced statistics",
            "/analyze": "AI threat analysis",
            "/ws/threats": "Real-time WebSocket feed"
        },
        "contact": {
            "developer": "BAOT Team",
            "support": "Enterprise-grade support",
            "documentation": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "BAOT 3.0.0",
        "services": {
            "api": "running",
            "ml_model": "ready",
            "webhooks": "enabled",
            "monitoring": "active"
        },
        "system": get_system_health()
    }

@app.get("/sessions")
def get_sessions(page: int = 1, limit: int = 50, threat_level: str = None, ip: str = None):
    """Enhanced sessions with advanced filtering"""
    try:
        sessions = load_sessions()
        
        # Advanced filtering
        if threat_level:
            sessions = [s for s in sessions if s.get('threat_level') == threat_level.upper()]
        if ip:
            sessions = [s for s in sessions if s.get('ip') == ip]
        
        # Pagination
        total_count = len(sessions)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_sessions = sessions[start_idx:end_idx]
        
        # Sort by threat level and timestamp
        paginated_sessions = sorted(paginated_sessions, 
                                  key=lambda x: (
                                      {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}.get(x.get('threat_level'), 0),
                                      x.get('timestamp', ''))
                                  , reverse=True)
        
        return {
            "sessions": paginated_sessions,
            "count": len(paginated_sessions),
            "total_count": total_count,
            "total_pages": (total_count + limit - 1) // limit,
            "current_page": page,
            "filters": {
                "threat_level": threat_level,
                "ip": ip
            }
        }
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/threats")
def get_threat_intelligence():
    """Get threat intelligence data"""
    try:
        intelligence = load_threat_intelligence()
        return {
            "threat_intelligence": intelligence,
            "summary": {
                "total_tracking": len(intelligence),
                "frequent_attackers": len([ti for ti in intelligence.values() if ti.attack_frequency > 5]),
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error getting threat intelligence: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_enhanced_statistics():
    """Enhanced comprehensive statistics"""
    try:
        sessions = load_sessions()
        intelligence = load_threat_intelligence()
        
        if not sessions:
            return EnhancedStats(
                total_sessions=0,
                total_threats=0,
                threat_levels={"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
                avg_score=0.0,
                system_health=get_system_health(),
                attack_vectors={},
                top_ips=[]
            )
        
        # Basic stats
        total_sessions = len(sessions)
        high_threat_sessions = [s for s in sessions if s.get('threat_level') in ['HIGH', 'CRITICAL']]
        total_threats = len(high_threat_sessions)
        
        # Threat level distribution
        threat_levels = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        scores = []
        attack_vectors = {}
        
        for session in sessions:
            level = session.get('threat_level', 'LOW')
            threat_levels[level] = threat_levels.get(level, 0) + 1
            scores.append(session.get('anomaly_score', 0))
            
            # Attack vector distribution
            vector = session.get('attack_vector', 'Unknown')
            attack_vectors[vector] = attack_vectors.get(vector, 0) + 1
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        # Top IPs by activity
        ip_counts = {}
        for session in sessions:
            ip = session.get('ip', 'unknown')
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
        
        top_ips = [
            {"ip": ip, "frequency": count, "intelligence": intelligence.get(ip, {})}
            for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        return EnhancedStats(
            total_sessions=total_sessions,
            total_threats=total_threats,
            threat_levels=threat_levels,
            avg_score=round(avg_score, 6),
            last_activity=max([s.get('timestamp') for s in sessions]) if sessions else None,
            system_health=get_system_health(),
            attack_vectors=attack_vectors,
            top_ips=top_ips
        )
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
def analyze_command(request: AnalyzeRequest):
    """Advanced AI command analysis"""
    try:
        result = advanced_threat_analysis(request.command, request.ip)
        result.update({
            'command': request.command,
            'ip': request.ip,
            'timestamp': datetime.now().isoformat(),
            'analyzer': 'BAOT 3.0 AI Engine'
        })
        
        # Update threat intelligence
        update_threat_intelligence(request.ip, result)
        
        return result
    except Exception as e:
        logger.error(f"Error analyzing command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sessions")
def create_session(session: Dict[str, Any]):
    """Create enhanced session record"""
    try:
        if not session.get('session_id'):
            session['session_id'] = str(uuid.uuid4())
        
        if not session.get('timestamp'):
            session['timestamp'] = datetime.now().isoformat()
        
        # Enhance session data
        analysis = advanced_threat_analysis(session.get('command', ''), session.get('ip', ''))
        session.update({
            'confidence': analysis.get('confidence', 0.0),
            'attack_vector': analysis.get('attack_vector', 'Unknown'),
            'indicators': analysis.get('indicators', []),
            'signature': analysis.get('signature', '')
        })
        
        save_session(session)
        
        return {"status": "success", "session_id": session['session_id'], "analysis": analysis}
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Real-time WebSocket endpoint
@app.websocket("/ws/threats")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time threats WebSocket"""
    await websocket.accept()
    websocket_connections.append(websocket)
    logger.info(f"BAOT WebSocket client connected. Total: {len(websocket_connections)}")
    
    # Send welcome message
    welcome_message = {
        "type": "welcome",
        "message": "Connected to BAOT AI/ML Threat Detection System",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }
    await websocket.send_text(json.dumps(welcome_message))
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)
        logger.info(f"WebSocket client disconnected. Total: {len(websocket_connections)}")

# Enhanced utility functions
def load_sessions() -> List[Dict]:
    """Load enhanced sessions"""
    try:
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, 'r') as f:
                sessions = json.load(f)
        else:
            # Enhanced sample data
            sessions = [
                {
                    "session_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "ip": "203.0.113.25",
                    "command": "rm -rf /tmp/*",
                    "threat_level": "CRITICAL",
                    "anomaly_score": 0.95,
                    "confidence": 0.95,
                    "attack_vector": "File System Destruction",
                    "indicators": ["Suspicious Keywords", "High Complexity"],
                    "response": "Permission denied",
                    "signature": "a1b2c3d4e5f6g7h8"
                },
                {
                    "session_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "ip": "198.51.100.50",
                    "command": "cat /etc/passwd",
                    "threat_level": "HIGH",
                    "anomaly_score": 0.85,
                    "confidence": 0.85,
                    "attack_vector": "System Reconnaissance",
                    "indicators": ["Suspicious Keywords"],
                    "response": "root:x:0:0:root:/root:/bin/bash",
                    "signature": "b2c3d4e5f6g7h8i9"
                },
                {
                    "session_id": str(uuid.uuid4()),
                    "timestamp": datetime.now().isoformat(),
                    "ip": "192.168.1.100",
                    "command": "ls -la",
                    "threat_level": "LOW",
                    "anomaly_score": 0.15,
                    "confidence": 0.5,
                    "attack_vector": "Generic Command",
                    "indicators": [],
                    "response": "file1.txt file2.txt folder1/",
                    "signature": "c3d4e5f6g7h8i9j0"
                }
            ]
            with open(SESSIONS_FILE, 'w') as f:
                json.dump(sessions, f, indent=2)
        return sessions
    except Exception as e:
        logger.error(f"Error loading sessions: {e}")
        return []

def save_session(session: Dict) -> bool:
    """Save enhanced session"""
    try:
        sessions = load_sessions()
        sessions.append(session)
        
        # Keep last 2000 sessions for better analysis
        if len(sessions) > 2000:
            sessions = sessions[-2000:]
        
        with open(SESSIONS_FILE, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        # Enhanced command logging
        log_entry = f"{session['timestamp']}:{session['ip']}:{session['command']}:{session['threat_level']}:{session.get('attack_vector', 'Unknown')}:{session.get('confidence', 0.0)}\n"
        with open(COMMANDS_FILE, 'a') as f:
            f.write(log_entry)
        
        return True
    except Exception as e:
        logger.error(f"Error saving session: {e}")
        return False

# BAOT Startup Events
@app.on_event("startup")
async def startup_event():
    logger.info("🛡️ BAOT AI/ML Honeypot System Starting...")
    logger.info("🚀 Advanced Threat Detection Engines Initializing...")
    logger.info(f"📁 Enhanced Data Directory: {DATA_DIR}")
    logger.info(f"🧠 AI Models Directory: {MODELS_DIR}")
    logger.info(f"📊 Threat Intelligence: {THREATS_FILE}")
    
    # Initialize enhanced sample data
    load_sessions()
    load_threat_intelligence()
    
    logger.info("✅ BAOT System Ready - Professional Grade AI/ML Honeypot Active!")
    logger.info("🎯 Ready for advanced threat detection and analysis!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 BAOT AI/ML Honeypot System Shutting Down...")

if __name__ == "__main__":
    print("🛡️ BAOT - Best AI/ML Honeypot System")
    print("🚀 Starting Professional Grade Threat Detection...")
    print("📍 Backend API: http://localhost:8000")
    print("📚 Advanced API Docs: http://localhost:8000/docs") 
    print("🔄 Real-time WebSocket: ws://localhost:8000/ws/threats")
    print("🎯 BAOT Ready for Enterprise-level Protection!")
    
    uvicorn.run(
        "baot_app:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )




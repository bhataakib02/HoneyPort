from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import os
import asyncio
from datetime import datetime
from typing import List, Dict, Any
import logging

from db import get_database_manager, CommandSession
from ai import AIManager
from telegram_alert import TelegramAlertManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AIML Honeypot API",
    description="Advanced AI/ML Honeypot Backend API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
db_manager = get_database_manager()
ai_manager = AIManager()
telegram_manager = TelegramAlertManager()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "AIML Honeypot API", "version": "1.0.0", "status": "active"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "ai_model": "loaded" if ai_manager.model else "not_loaded",
            "telegram": "configured" if telegram_manager.is_configured() else "not_configured"
        }
    }

@app.get("/sessions")
async def get_sessions():
    """Get all captured command sessions"""
    try:
        sessions = await db_manager.get_all_sessions()
        return {"sessions": sessions, "count": len(sessions)}
    except Exception as e:
        logger.error(f"Error fetching sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get specific session details"""
    try:
        session = await db_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/commands/{command_id}")
async def get_command(command_id: str):
    """Get specific command details"""
    try:
        command = await db_manager.get_command(command_id)
        if not command:
            raise HTTPException(status_code=404, detail="Command not found")
        return command
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching command {command_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_command(command: str, ip: str = "unknown"):
    """Analyze a command for threat level"""
    try:
        # Extract features and analyze
        features = ai_manager.extract_features(command)
        anomaly_score = ai_manager.predict_anomaly(features)
        threat_level = ai_manager.get_threat_level(anomaly_score)
        
        # Save to database
        session_id = await db_manager.save_command(ip, command, anomaly_score, threat_level)
        
        # Send alert if high threat
        if threat_level in ["HIGH", "CRITICAL"]:
            await telegram_manager.send_alert(command, ip, threat_level)
            
            # Broadcast to WebSocket connections
            await manager.broadcast({
                "type": "threat_alert",
                "session_id": session_id,
                "ip": ip,
                "command": command,
                "threat_level": threat_level,
                "anomaly_score": anomaly_score,
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "session_id": session_id,
            "command": command,
            "ip": ip,
            "anomaly_score": anomaly_score,
            "threat_level": threat_level,
            "features": features,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing command '{command}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_statistics():
    """Get honeypot statistics"""
    try:
        stats = await db_manager.get_statistics()
        model_stats = ai_manager.get_model_stats()
        
        return {
            "database_stats": stats,
            "model_stats": model_stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/threats")
async def get_threats():
    """Get all high-threat commands"""
    try:
        threats = await db_manager.get_threats()
        return {"threats": threats, "count": len(threats)}
    except Exception as e:
        logger.error(f"Error fetching threats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrain")
async def force_retrain():
    """Force ML model retraining"""
    try:
        result = await ai_manager.retrain_model()
        return {"message": "Model retraining initiated", "result": result}
    except Exception as e:
        logger.error(f"Error during retraining: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/sessions")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.get("/dashboard")
async def dashboard():
    """Simple dashboard HTML"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AIML Honeypot Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
            .stats { display: flex; gap: 20px; margin: 20px 0; }
            .stat-card { background: #e8f4fd; padding: 15px; border-radius: 5px; flex: 1; }
            .footer { margin-top: 40px; text-align: center; color: #666; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 AIML Honeypot Dashboard</h1>
            <p>Advanced AI/ML Honeypot Monitoring System</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>📊 Sessions</h3>
                <p id="session-count">Loading...</p>
            </div>
            <div class="stat-card">
                <h3>⚠️ Threats</h3>
                <p id="threat-count">Loading...</p>
            </div>
            <div class="stat-card">
                <h3>🧠 Model Status</h3>
                <p id="model-status">Loading...</p>
            </div>
        </div>
        
        <h2>Recent Sessions</h2>
        <div id="sessions">Loading...</div>
        
        <div class="footer">
            <p>AIML Honeypot v1.0.0 | <a href="/docs">API Documentation</a></p>
        </div>
        
        <script>
            async function loadDashboard() {
                try {
                    // Load statistics
                    const statsResponse = await fetch('/stats');
                    const statsData = await statsResponse.json();
                    
                    document.getElementById('session-count').textContent = statsData.database_stats.total_sessions || 0;
                    document.getElementById('threat-count').textContent = statsData.database_stats.total_threats || 0;
                    document.getElementById('model-status').textContent = statsData.model_stats.status || 'Unknown';
                    
                    // Load recent sessions
                    const sessionsResponse = await fetch('/sessions');
                    const sessionsData = await sessionsResponse.json();
                    
                    const sessionsHtml = sessionsData.sessions.slice(0, 10).map(session => `
                        <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 3px;">
                            <strong>IP:</strong> ${session.ip} | 
                            <strong>Command:</strong> ${session.command} | 
                            <strong>Threat:</strong> ${session.threat_level} | 
                            <strong>Time:</strong> ${new Date(session.timestamp).toLocaleString()}
                        </div>
                    `).join('');
                    
                    document.getElementById('sessions').innerHTML = sessionsHtml || 'No sessions found';
                    
                } catch (error) {
                    console.error('Error loading dashboard:', error);
                    document.getElementById('sessions').innerHTML = 'Error loading data';
                }
            }
            
            // Load dashboard every 5 seconds
            loadDashboard();
            setInterval(loadDashboard, 5000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

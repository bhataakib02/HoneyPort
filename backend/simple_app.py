#!/usr/bin/env python3
"""
Simple FastAPI Backend - No complex imports
"""

import json
import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(title="AIML Honeypot Simple API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data file paths
sessions_file = "../honeypot/data/sessions.json"

@app.get("/")
def root():
    return {"message": "AIML Honeypot API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/sessions")
def get_sessions():
    """Get all captured sessions"""
    try:
        if not os.path.exists(sessions_file):
            return {"sessions": []}
        
        with open(sessions_file, 'r') as f:
            sessions = json.load(f)
        
        return {"sessions": sessions, "count": len(sessions)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/stats")
def get_stats():
    """Get basic statistics"""
    try:
        if not os.path.exists(sessions_file):
            return {
                "total_sessions": 0,
                "total_threats": 0,
                "threat_levels": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
            }
        
        with open(sessions_file, 'r') as f:
            sessions = json.load(f)
        
        total = len(sessions)
        high_threats = sum(1 for s in sessions if s.get("threat_level") in ["HIGH", "CRITICAL"])
        
        threat_levels = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        for session in sessions:
            level = session.get("threat_level", "LOW")
            if level in threat_levels:
                threat_levels[level] += 1
        
        return {
            "total_sessions": total,
            "total_threats": high_threats,
            "threat_levels": threat_levels,
            "avg_score": sum(s.get("anomaly_score", 0) for s in sessions) / total if total > 0 else 0
        }
    except Exception as e:
            return {"error": str(e)}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AIML Honeypot Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: white; margin: 0; padding: 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center; }
            .stat-number { font-size: 2em; font-weight: bold; margin: 10px 0; }
            .threat-low { color: #10b981; }
            .threat-medium { color: #f59e0b; }
            .threat-high { color: #f97316; }
            .threat-critical { color: #ef4444; }
            .sessions { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; }
            .session { padding: 10px; margin: 5px 0; background: rgba(255,255,255,0.1); border-radius: 5px; }
            .refresh-btn { 
                background: #3b82f6; color: white; border: none; padding: 10px 20px; 
                border-radius: 5px; cursor: pointer; margin-bottom: 20px;
            }
            .refresh-btn:hover { background: #2563eb; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 AIML Honeypot Dashboard</h1>
                <p>AI/ML Powered Threat Detection</p>
            </div>
            
            <button class="refresh-btn" onclick="loadData()">🔄 Refresh Data</button>
            
            <div class="stats">
                <div class="stat-card">
                    <div>📊 Total Sessions</div>
                    <div class="stat-number" id="total-sessions">0</div>
                </div>
                <div class="stat-card">
                    <div>⚠️ High Threats</div>
                    <div class="stat-number" id="high-threats">0</div>
                </div>
                <div class="stat-card">
                    <div>📈 Avg Score</div>
                    <div class="stat-number" id="avg-score">0.000</div>
                </div>
                <div class="stat-card">
                    <div>🕒 Last Updated</div>
                    <div class="stat-number" id="last-updated">Just now</div>
                </div>
            </div>

            <div class="sessions">
                <h2>📋 Recent Sessions</h2>
                <div id="sessions">Loading sessions...</div>
            </div>
        </div>

        <script>
            async function loadData() {
                try {
                    // Load stats
                    const statsResponse = await fetch('/stats');
                    const stats = await statsResponse.json();
                    
                    document.getElementById('total-sessions').textContent = stats.total_sessions || 0;
                    document.getElementById('high-threats').textContent = stats.total_threats || 0;
                    document.getElementById('avg-score').textContent = (stats.avg_score || 0).toFixed(3);
                    document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
                    
                    // Load sessions
                    const sessionsResponse = await fetch('/sessions');
                    const data = await sessionsResponse.json();
                    const sessions = data.sessions || [];
                    
                    const html = sessions.slice(0, 20).map(session => `
                        <div class="session">
                            <strong>${session.ip}</strong> | 
                            <code>${session.command}</code> | 
                            <span class="threat-${session.threat_level.toLowerCase()}">${session.threat_level}</span> | 
                            Score: ${(session.anomaly_score || 0).toFixed(3)} | 
                            ${new Date(session.timestamp).toLocaleString()}
                        </div>
                    `).join('');
                    
                    document.getElementById('sessions').innerHTML = html || 'No sessions found';
                    
                } catch (error) {
                    console.error('Error loading data:', error);
                    document.getElementById('sessions').innerHTML = 'Error loading data';
                }
            }
            
            // Load data immediately and every 5 seconds
            loadData();
            setInterval(loadData, 5000);
        </script>
    </body>`)
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Using port 8001 to avoid conflicts




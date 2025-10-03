#!/usr/bin/env python3
"""
AI Analysis Module for AIML Honeypot
Provides command analysis using ML models
"""

import os
import sys
import logging
import json
from datetime import datetime
from typing import Dict, Any, List

# Add backend to path to use AI manager
sys.path.append('/app/backend')
from backend.ai import AIManager

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """AI-powered command analyzer for honeypot"""
    
    def __init__(self):
        self.ai_manager = AIManager()
        self.analysis_cache = {}
        self.cache_size = 1000
        
        logger.info("AI Analyzer initialized")
        if not self.ai_manager.model:
            logger.warning("ML model not loaded - using heuristic analysis")

    def has_model(self) -> bool:
        """Check if ML model is loaded"""
        return self.ai_manager.model is not None

    async def analyze_command(self, command: str, ip: str) -> Dict[str, Any]:
        """Analyze command for threat level"""
        try:
            # Check cache first
            cache_key = f"{ip}:{command}"
            if cache_key in self.analysis_cache:
                return self.analysis_cache[cache_key]
            
            # Perform analysis
            analysis = self.ai_manager.validate_command(command)
            
            # Add IP-specific context
            analysis["ip"] = ip
            analysis["timestamp"] = datetime.now().isoformat()
            analysis["session_id"] = f"{ip}_{int(datetime.now().timestamp())}"
            
            # Determine if this is a known attack pattern
            analysis["attack_patterns"] = self._detect_attack_patterns(command)
            analysis["complexity_score"] = self._calculate_complexity(command)
            
            # Cache result
            self._cache_analysis(cache_key, analysis)
            
            logger.info(f"Analyzed command '{command}' -> {analysis['threat_level']}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing command '{command}': {e}")
            return self._fallback_analysis(command, ip)

    def _detect_attack_patterns(self, command: str) -> List[str]:
        """Detect known attack patterns in command"""
        patterns = []
        command_lower = command.lower()
        
        # Common attack patterns
        attack_patterns = {
            "privilege_escalation": ["sudo", "su -", "su root", "su -l", "su -"],
            "file_manipulation": ["rm -rf", "rm -rf /", "dd if=", "cat >", "echo >"],
            "system_enumeration": ["cat /etc/passwd", "cat /etc/shadow", "uname -a", "ps aux"],
            "network_scanning": ["nmap", "masscan", "zmap", "nc -z", "nc -v"],
            "command_injection": ["; ", "&&", "||", "|", "`", "$(", "${{"],
            "data_exfiltration": ["curl", "wget", "scp", "rsync", "nc-"],
            "service_disruption": ["kill -9", "killall", "systemctl stop", "service stop"],
            "malicious_scripting": ["python -c", "bash -c", "sh -c", "curl | sh"],
            "authentication_bypass": ["passwd", "ssh-copy-id", "ssh-keygen", "id_rsa"],
            "persistence": ["crontab", "systemctl enable", ".bashrc", ".profile"]
        }
        
        for pattern_type, keywords in attack_patterns.items():
            if any(keyword in command_lower for keyword in keywords):
                patterns.append(pattern_type)
        
        return patterns

    def _calculate_complexity(self, command: str) -> float:
        """Calculate command complexity score"""
        score = 0.0
        
        # Length factor
        if len(command) > 50:
            score += 0.2
        elif len(command) > 100:
            score += 0.4
        
        # Pipe chains
        score += command.count('|') * 0.1
        
        # Command chaining
        score += command.count(';') * 0.1
        score += command.count('&&') * 0.15
        score += command.count('||') * 0.15
        
        # Substitution and expansion
        score += command.count('$(') * 0.2
        score += command.count('`') * 0.15
        
        # Redirection
        score += command.count('>') * 0.05
        score += command.count('<') * 0.05
        score += command.count('2>&1') * 0.1
        
        # Argument complexity
        args = command.split()
        if len(args) > 5:
            score += 0.1
            
        return min(1.0, score)

    def _cache_analysis(self, cache_key: str, analysis: Dict[str, Any]):
        """Cache analysis result"""
        # Maintain cache size
        if len(self.analysis_cache) >= self.cache_size:
            # Remove oldest 20% of entries
            keys_to_remove = list(self.analysis_cache.keys())[:self.cache_size//5]
            for key in keys_to_remove:
                del self.analysis_cache[key]
        
        self.analysis_cache[cache_key] = analysis

    def _fallback_analysis(self, command: str, ip: str) -> Dict[str, Any]:
        """Fallback analysis when AI fails"""
        return {
            "command": command,
            "ip": ip,
            "anomaly_score": 0.5,  # Medium risk as fallback
            "threat_level": "MEDIUM",
            "risk_factors": ["analysis_error"],
            "timestamp": datetime.now().isoformat(),
            "analysis_method": "fallback"
        }

    async def batch_analyze(self, commands: List[str], ip: str) -> List[Dict[str, Any]]:
        """Analyze multiple commands from same IP"""
        results = []
        
        for command in commands:
            analysis = await self.analyze_command(command, ip)
            results.append(analysis)
        
        return results

    async def get_ip_risk_profile(self, ip: str, limit: int = 50) -> Dict[str, Any]:
        """Generate risk profile for IP based on historical commands"""
        # This would integrate with backend database in production
        # For now, return basic profile
        return {
            "ip": ip,
            "total_commands": 0,
            "high_threat_commands": 0,
            "common_patterns": [],
            "risk_score": 0.0,
            "last_seen": None
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded ML model"""
        return self.ai_manager.get_model_stats()

    async def force_retrain(self) -> Dict[str, Any]:
        """Force model retraining"""
        try:
            result = await self.ai_manager.retrain_model()
            logger.info("Model retraining completed")
            return result
        except Exception as e:
            logger.error(f"Model retraining failed: {e}")
            return {"status": "error", "message": str(e)}

    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get analyzer statistics"""
        return {
            "cache_size": len(self.analysis_cache),
            "model_loaded": self.has_model(),
            "analyzer_uptime": datetime.now().isoformat(),
            "model_stats": self.get_model_info()
        }




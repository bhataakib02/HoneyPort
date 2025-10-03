import joblib
import os
import numpy as np
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dotenv import load_dotenv
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()

logger = logging.getLogger(__name__)

class AIManager:
    """AI/ML Manager for honeypot threat detection"""
    
    def __init__(self):
        self.model_path = os.getenv("ML_MODEL_PATH", "/app/models/iforest.joblib")
        self.scaler_path = os.path.join(os.path.dirname(self.model_path), "scaler.joblib")
        self.vectorizer_path = os.path.join(os.path.dirname(self.model_path), "vectorizer.joblib")
        self.model_stats_path = os.path.join(os.path.dirname(self.model_path), "stats.json")
        
        self.model = None
        self.scaler = None
        self.vectorizer = None
        self.model_stats = {}
        
        self._ensure_model_directory()
        self._load_models()

    def _ensure_model_directory(self):
        """Ensure model directory exists"""
        model_dir = os.path.dirname(self.model_path)
        os.makedirs(model_dir, exist_ok=True)

    def _load_models(self):
        """Load existing ML models"""
        try:
            # Load IsolationForest model
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info(f"Loaded IsolationForest model from {self.model_path}")
            else:
                logger.info("No existing model found, will create new one")
                self.model = None

            # Load scaler
            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                logger.info(f"Loaded scaler from {self.scaler_path}")
            else:
                self.scaler = StandardScaler()

            # Load vectorizer
            if os.path.exists(self.vectorizer_path):
                self.vectorizer = joblib.load(self.vectorizer_path)
                logger.info(f"Loaded TF-IDF vectorizer from {self.vectorizer_path}")
            else:
                self.vectorizer = TfidfVectorizer(
                    max_features=100,
                    stop_words='english',
                    ngram_range=(1, 2)
                )

            # Load model stats
            if os.path.exists(self.model_stats_path):
                with open(self.model_stats_path, 'r') as f:
                    self.model_stats = json.load(f)
                logger.info("Loaded model statistics")
        except Exception as e:
            logger.error(f"Error loading models: {e}")

    def extract_features(self, command: str) -> Dict[str, Any]:
        """Extract comprehensive features from a command"""
        # Basic features
        features = {
            "length": len(command),
            "word_count": len(command.split()),
            "digit_count": sum(c.isdigit() for c in command),
            "special_char_count": sum(not c.isalnum() and not c.isspace() for c in command),
            "uppercase_count": sum(c.isupper() for c in command),
            "path_depth": command.count('/'),
            "has_numbers": bool(sum(c.isdigit() for c in command)),
        }

        # Command patterns
        suspicious_patterns = [
            "rm -rf", "sudo", "su -", "passwd", "shadow",
            "iptables", "netstat", "ps aux", "whoami", "id",
            "curl", "wget", "nc ", "netcat", "telnet",
            "ftp", "nmap", "hydra", "john", "hashcat",
            "python", "bash", "sh ", "chmod", "chown",
            "kill", "pkill", "killall", "systemctl",
            "journalctl", "cat /etc", "cat /proc", "ls -la",
            "find ", "grep ", "awk", "sed", "xargs", "..",
            "/dev/null", "2>&1", ">/dev/null", "&&", "||"
        ]

        # Check for suspicious patterns
        suspicious_score = 0
        detected_patterns = []
        
        for pattern in suspicious_patterns:
            if pattern in command.lower():
                suspicious_score += 1
                detected_patterns.append(pattern)

        features["suspicious_patterns"] = suspicious_score
        features["detected_patterns"] = detected_patterns

        # Entropy calculation (randomness measure)
        char_counts = {}
        for char in command:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        entropy = 0
        for count in char_counts.values():
            if count > 0:
                p = count / len(command)
                entropy -= p * np.log2(p)
        
        features["entropy"] = entropy

        # File/directory indicators
        features["has_file_path"] = "/" in command or "\\" in command
        features["has_url"] = "http://" in command or "https://" in command
        features["has_ip"] = any(part.replace('.', '').isdigit() and len(part.split('.')) == 4 
                               for part in command.split())

        return features

    def create_feature_vector(self, features: Dict[str, Any]) -> np.array:
        """Convert features dict to numeric vector"""
        # Base features (always numeric)
        numeric_features = [
            features["length"],
            features["word_count"],
            features["digit_count"],
            features["special_char_count"],
            features["uppercase_count"],
            features["path_depth"],
            features["suspicious_patterns"],
            features["entropy"],
            int(features["has_numbers"]),
            int(features["has_file_path"]),
            int(features["has_url"]),
            int(features["has_ip"])
        ]
        
        return np.array(numeric_features).reshape(1, -1)

    def predict_anomaly(self, features: Dict[str, Any]) -> float:
        """Predict anomaly score for command"""
        if self.model is None:
            # Fallback to simple heuristic
            return self._heuristic_score(features)
        
        try:
            feature_vector = self.create_feature_vector(features)
            
            # Scale features if scaler is available
            if self.scaler:
                feature_vector = self.scaler.transform(feature_vector)
            
            # Predict anomaly score (-1 = anomaly, 1 = normal, score = distance from decision boundary)
            if hasattr(self.model, 'decision_function'):
                score = self.model.decision_function(feature_vector)[0]
                # Normalize score to 0-1 range
                normalized_score = max(0, min(1, (score + self.model.offset_[0]) / (2 * self.model.offset_[0]) + 0.5))
                return 1 - normalized_score  # Higher score = more anomalous
            else:
                prediction = self.model.predict(feature_vector)[0]
                return 1 if prediction == -1 else 0
        except Exception as e:
            logger.error(f"Error predicting anomaly: {e}")
            return self._heuristic_score(features)

    def _heuristic_score(self, features: Dict[str, Any]) -> float:
        """Simple heuristic scoring when ML model is not available"""
        score = 0.0
        
        # Length penalty
        if features["length"] > 50:
            score += 0.2
        
        # Suspicious patterns
        score += features["suspicious_patterns"] * 0.15
        
        # Special characters
        if features["special_char_count"] > 5:
            score += 0.1
            
        # Entropy
        if features["entropy"] > 4:
            score += 0.2
            
        # File paths
        if features["has_file_path"]:
            score += 0.1
            
        return min(1.0, score)

    def get_threat_level(self, anomaly_score: float) -> str:
        """Convert anomaly score to threat level"""
        if anomaly_score >= 0.8:
            return "CRITICAL"
        elif anomaly_score >= 0.6:
            return "HIGH"
        elif anomaly_score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"

    async def train_model(self, commands: List[str]) -> Dict[str, Any]:
        """Train IsolationForest model on command data"""
        if not commands:
            logger.warning("No commands provided for training")
            return {"status": "error", "message": "No training data"}

        try:
            # Extract features for all commands
            feature_vectors = []
            for cmd in commands:
                features = self.extract_features(cmd)
                vector = self.create_feature_vector(features)
                feature_vectors.append(vector[0])
            
            if not feature_vectors:
                return {"status": "error", "message": "No valid features extracted"}

            X = np.array(feature_vectors)
            
            # Scale features
            self.scaler.fit(X)
            X_scaled = self.scaler.transform(X)
            
            # Train IsolationForest
            contamination = min(0.1, len(commands) * 0.01)  # Adaptive contamination
            self.model = IsolationForest(
                contamination=contamination,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_scaled)
            
            # Save models
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            # Update stats
            self.model_stats = {
                "training_samples": len(commands),
                "features": X.shape[1],
                "contamination": contamination,
                "last_trained": datetime.now().isoformat(),
                "model_version": "1.0"
            }
            
            with open(self.model_stats_path, 'w') as f:
                json.dump(self.model_stats, f, indent=2)
            
            logger.info(f"Model trained successfully with {len(commands)} commands")
            
            return {
                "status": "success",
                "training_samples": len(commands),
                "features": X.shape[1],
                "contamination": contamination,
                "model_path": self.model_path
            }
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return {"status": "error", "message": str(e)}

    async def retrain_model(self) -> Dict[str, Any]:
        """Retrain model with new data from database"""
        try:
            # Get commands from data files
            commands_file = "/app/data/commands.json"
            if not os.path.exists(commands_file):
                return {"status": "error", "message": "No command data found"}
            
            with open(commands_file, 'r') as f:
                commands_data = json.load(f)
            
            commands = [cmd.get("command", "") for cmd in commands_data 
                       if cmd.get("command")]
            
            if len(commands) < 10:
                return {"status": "warning", "message": f"Insufficient data ({len(commands)} commands), need at least 10"}
            
            return await self.train_model(commands)
            
        except Exception as e:
            logger.error(f"Error during retraining: {e}")
            return {"status": "error", "message": str(e)}

    def get_model_stats(self) -> Dict[str, Any]:
        """Get current model statistics"""
        stats = {
            "model_loaded": self.model is not None,
            "scaler_loaded": self.scaler is not None,
            "vectorizer_loaded": self.vectorizer is not None,
            "model_path": self.model_path,
            "status": "ready" if self.model else "not_trained"
        }
        
        stats.update(self.model_stats)
        return stats

    def validate_command(self, command: str) -> Dict[str, Any]:
        """Validate and analyze a command"""
        features = self.extract_features(command)
        anomaly_score = self.predict_anomaly(features)
        threat_level = self.get_threat_level(anomaly_score)
        
        return {
            "command": command,
            "features": features,
            "anomaly_score": anomaly_score,
            "threat_level": threat_level,
            "risk_factors": features["detected_patterns"],
            "analysis_timestamp": datetime.now().isoformat()
        }

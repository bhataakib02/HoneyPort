#!/usr/bin/env python3
"""
Automatic Model Retraining for AIML Honeypot
Runs in background to keep ML model updated with new attack patterns
"""

import os
import sys
import asyncio
import logging
import time
import signal
from datetime import datetime, timedelta
from typing import Dict, Any

# Add paths for imports
sys.path.append('/app')
sys.path.append('/app/backend')

from backend.ai import AIManager
from backend.train_model import load_training_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/retrainer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ModelRetrainer:
    """Automatic model retraining service"""
    
    def __init__(self, interval_hours: int = 1):
        self.interval_hours = interval_hours
        self.interval_seconds = interval_hours * 3600
        self.ai_manager = AIManager()
        self.running = True
        self.last_training = None
        self.training_count = 0
        
        # Signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"Model retrainer initialized with {interval_hours}h interval")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down retrainer...")
        self.running = False

    async def needs_retraining(self) -> bool:
        """Check if model needs retraining based on new data"""
        commands_file = "/app/data/commands.json"
        
        if not os.path.exists(commands_file):
            logger.debug("No command data file found")
            return False
            
        try:
            # Check if file has been modified recently
            stat = os.stat(commands_file)
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            if self.last_training and modified_time <= self.last_training:
                logger.debug("No new command data since last training")
                return False
            
            # Check if we have enough new data
            import json
            with open(commands_file, 'r') as f:
                commands = json.load(f)
            
            # If last training was recent and we don't have many new commands, skip
            if self.last_training:
                recent_commands = [
                    cmd for cmd in commands
                    if datetime.fromisoformat(cmd.get('timestamp', '')) > self.last_training
                ]
                if len(recent_commands) < 10:
                    logger.debug(f"Only {len(recent_commands)} new commands, skipping retrain")
                    return False
            
            # Need retraining if we have enough commands
            minimal_commands = 50  # Minimum commands for meaningful training
            if len(commands) >= minimal_commands:
                logger.info(f"Retraining triggered: {len(commands)} commands available")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking retraining need: {e}")
            return False

    async def retrain_model(self) -> Dict[str, Any]:
        """Perform model retraining"""
        logger.info("Starting automatic model retraining...")
        
        try:
            # Load training data
            training_data = load_training_data()
            
            if not training_data:
                logger.warning("No training data available")
                return {"status": "error", "message": "No training data"}
            
            # Perform training
            result = await self.ai_manager.train_model(training_data)
            
            if result["status"] == "success":
                self.training_count += 1
                self.last_training = datetime.now()
                
                logger.info("✅ Model retraining completed successfully")
                logger.info(f"Training #{self.training_count}: {result['training_samples']} samples, "
                           f"{result['features']} features")
                
                # Save training log
                await self._log_training_success(result)
                
            else:
                logger.error(f"❌ Model training failed: {result}")
                
            return result
            
        except Exception as e:
            logger.error(f"Error during retraining: {e}")
            return {"status": "error", "message": str(e)}

    async def _log_training_success(self, result: Dict[str, Any]):
        """Log successful training session"""
        training_info = {
            "timestamp": datetime.now().isoformat(),
            "training_count": self.training_count,
            "samples": result.get("training_samples", 0),
            "features": result.get("features", 0),
            "contamination": result.get("contamination", 0),
            "status": "success"
        }
        
        # Append to training log
        log_file = "/app/logs/training_history.json"
        try:
            import json
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            history.append(training_info)
            
            # Keep only last 100 training sessions
            if len(history) > 100:
                history = history[-100:]
            
            with open(log_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to log training success: {e}")

    async def run(self):
        """Main retraining loop"""
        logger.info("🚀 Starting AIML Honeypot Model Retrainer")
        logger.info(f"⏱️ Retraining interval: {self.interval_hours} hours")
        
        # Check initial training need
        if await self.needs_retraining():
            logger.info("Initial training triggered (cold start)")
            await self.retrain_model()
        
        # Main loop
        while self.running:
            try:
                logger.info(f"Sleeping for {self.interval_hours} hours...")
                
                # Sleep in smaller chunks to allow graceful shutdown
                sleep_chunks = self.interval_seconds // 300  # 5-minute chunks
                for _ in range(sleep_chunks):
                    if not self.running:
                        break
                    await asyncio.sleep(300)
                
                if not self.running:
                    break
                
                # Check if retraining is needed
                if await self.needs_retraining():
                    logger.info("Periodic retraining triggered")
                    await self.retrain_model()
                else:
                    logger.debug("Skipping periodic retraining (no new data)")
                
            except Exception as e:
                logger.error(f"Error in retraining loop: {e}")
                # Continue despite errors
                await asyncio.sleep(60)  # Wait 1 minute before continuing
        
        logger.info("Model retrainer shutdown complete")

    async def get_status(self) -> Dict[str, Any]:
        """Get retrainer status"""
        return {
            "running": self.running,
            "interval_hours": self.interval_hours,
            "last_training": self.last_training.isoformat() if self.last_training else None,
            "training_count": self.training_count,
            "next_check": (self.last_training + timedelta(hours=self.interval_hours)).isoformat() 
                         if self.last_training else None
        }

async def main():
    """Main function"""
    # Get interval from environment or use default
    interval_hours = int(os.getenv("RETRAIN_INTERVAL", "1"))
    
    retrainer = ModelRetrainer(interval_hours)
    
    try:
        await retrainer.run()
    except KeyboardInterrupt:
        logger.info("Retrainer interrupted by user")
    except Exception as e:
        logger.error(f"Retrainer failed: {e}")
        sys.exit(1)
    
    logger.info("Retrainer shutdown completed")
    return 0

if __name__ == "__main__":
    # Ensure necessary directories exist
    os.makedirs("/app/logs", exist_ok=True)
    os.makedirs("/app/models", exist_ok=True)
    
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Fatal error in retrainer: {e}")
        sys.exit(1)

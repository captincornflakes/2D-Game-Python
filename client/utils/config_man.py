import os
import json

def load_config(config_path):
    """Load the client configuration from config.json."""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        # Default configuration
        return {
            "default_server": "localhost",
            "default_port": 85,
            "player_name": "Player"
        }

def save_config(config_path, config):
    """Save the client configuration to config.json."""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
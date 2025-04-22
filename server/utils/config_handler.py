import os
import json

# Hardcoded path to config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    """Load the server configuration from a JSON file."""
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            print(f"Config loaded successfully")  # Debug statement
            return config
    except FileNotFoundError:
        print(f"Config file not found at {CONFIG_PATH}. Using default values.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from config file: {e}")
        return {}
    except Exception as e:
        print(f"Failed to load config: {e}")
        return {}
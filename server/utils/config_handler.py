import os
import json

def load_config(config_path):
    """Load the server configuration from a JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            print(f"Config loaded successfully")  # Debug statement
            return config
    except FileNotFoundError:
        print(f"Config file not found at {config_path}. Using default values.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from config file: {e}")
        return {}
    except Exception as e:
        print(f"Failed to load config: {e}")
        return {}
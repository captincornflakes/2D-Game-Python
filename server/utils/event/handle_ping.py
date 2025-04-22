import json
from utils.config_handler import load_config  # Import the config handler

# Path to the server configuration file
CONFIG_PATH = "../config.json"

def handle_ping(client_socket):
    """Respond to a ping message."""
    # Load the configuration to get the MOTD
    config = load_config(CONFIG_PATH)
    motd = config.get("world", {}).get("motd", "Welcome to the server!")  # Default MOTD if not found

    # Create the response
    response = {"action": "pong", "motd": motd}
    client_socket.sendall(json.dumps(response).encode('utf-8'))
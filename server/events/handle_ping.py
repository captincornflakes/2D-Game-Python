import json
from utils.config_handler import load_config


def handle_ping(client_socket):
    """Respond to a ping message."""
    # Load the configuration to get the MOTD
    config = load_config()
    motd = config.get("world", {}).get("motd", "Welcome to the server!")  # Default MOTD if not found

    # Create the response
    response = {"action": "pong", "motd": motd}
    client_socket.sendall(json.dumps(response).encode('utf-8'))
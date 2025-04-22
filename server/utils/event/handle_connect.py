import json
import os
from utils.config_handler import load_config  # Import the config handler
from utils.player_auth import PlayerAuth  # Import PlayerAuth for API validation

def handle_connect(addr, message, clients):
    """Handle a connection request from a UDP client."""
    print(f"Handling connection from {addr}: {message}")

    # Extract client information from the message
    username = message.get("username")

    if not username:
        print(f"Invalid connection request from {addr}: Missing 'username'")
        return

    # Load the server configuration to determine the world folder
    config = load_config()  # No need to pass a path
    world_folder = os.path.join(os.path.dirname(__file__), "..", "..", config.get("world", {}).get("world_file", "world_data"))
    player_file_path = os.path.join(world_folder, "player.json")

    # Ensure the directory for player.json exists
    os.makedirs(os.path.dirname(player_file_path), exist_ok=True)

    # Initialize PlayerAuth to use the check_player_api method
    player_auth = PlayerAuth(world_folder)

    # Validate the player and retrieve the UUID from the API
    client_uuid = player_auth.check_player_api(username)
    if not client_uuid:
        print(f"Failed to validate player {username} via API. Connection denied.")
        return

    # Load existing player data from player.json
    if os.path.exists(player_file_path):
        with open(player_file_path, "r") as file:
            player_data = json.load(file)
    else:
        player_data = {}

    # Check if the player already exists in the file
    if client_uuid in player_data:
        print(f"Player {username} with UUID {client_uuid} found in player.json")
        player_info = player_data[client_uuid]
        player_info["online"] = True  # Mark the player as online
        player_info["udp_addr"] = addr  # Log the UDP connection address
    else:
        print(f"Player {username} with UUID {client_uuid} not found. Adding to player.json")
        # Add new player data
        player_info = {
            "uuid": client_uuid,
            "username": username,
            "inventory": [],
            "stats": {
                "health": 100,
                "stamina": 100,
                "hunger": 100
            },
            "online": True,
            "udp_addr": addr  # Log the UDP connection address
        }
        player_data[client_uuid] = player_info

    # Save the updated player data back to player.json
    with open(player_file_path, "w") as file:
        json.dump(player_data, file, indent=4)

    # Register the client in the clients dictionary
    clients[addr] = {
        "uuid": client_uuid,
        "username": username,
        "udp_addr": addr
    }

    print(f"Registered client {username} with UUID {client_uuid} at {addr}")

    # Send a response to the client with their player data
    response = {
        "action": "connected",
        "message": f"Welcome, {username}!",
        "player_data": player_info
    }
    response_data = json.dumps(response).encode('utf-8')

    # Send the response back to the client
    udp_socket = clients.get("udp_socket")  # Ensure the UDP socket is available
    if udp_socket:
        udp_socket.sendto(response_data, addr)
    else:
        print("UDP socket not available to send response.")
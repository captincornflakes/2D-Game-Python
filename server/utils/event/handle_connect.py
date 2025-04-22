import json
import os
from utils.config_handler import load_config  # Import the config handler

def handle_connect(addr, message, clients):
    """Handle a connection request from a UDP client."""
    print(f"Handling connection from {addr}: {message}")

    # Extract client information from the message
    client_uuid = message.get("uuid")
    username = message.get("username")

    if not client_uuid or not username:
        print(f"Invalid connection request from {addr}: Missing 'uuid' or 'username'")
        return

    # Load the server configuration to determine the world folder
    config = load_config()  # No need to pass a path
    world_folder = config.get("world", {}).get("world_file", "world_data")
    player_file_path = os.path.join("server", world_folder, "player.json")

    # Ensure the directory for player.json exists
    os.makedirs(os.path.dirname(player_file_path), exist_ok=True)

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
            "online": True
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
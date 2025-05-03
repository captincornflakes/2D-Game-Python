import json
from utils.config_handler import load_config
from player.player_auth import PlayerAuth  # Updated import path

def handle_connect(addr, message, clients, udp_socket):
    """Handle a connection request from a UDP client."""
    from world.world_handler import load_players_file, save_players_file, update_player_location  # Lazy import

    print(f"Handling connection from {addr}: {message}")

    username = message.get("username")
    if not username:
        print(f"Invalid connection request from {addr}: Missing 'username'")
        return

    config = load_config()
    world_folder = config["world"]["world_file"]
    player_auth = PlayerAuth(world_folder)

    client_uuid = player_auth.check_player_api(username)
    if not client_uuid:
        print(f"Failed to validate player {username} via API. Connection denied.")
        return

    player_data = load_players_file()
    if client_uuid in player_data:
        print(f"Player {username} with UUID {client_uuid} found in players.json")
        player_info = player_data[client_uuid]
        player_info["online"] = True
        player_info["udp_addr"] = addr
    else:
        print(f"Player {username} with UUID {client_uuid} not found. Adding to players.json")
        player_info = {
            "uuid": client_uuid,
            "username": username,
            "inventory": [],
            "stats": {"health": 100, "stamina": 100, "hunger": 100},
            "location": {"x": 1.5, "y": 1.5},
            "online": True,
            "udp_addr": addr
        }
        player_data[client_uuid] = player_info

    save_players_file(player_data)
    update_player_location(client_uuid, player_info["location"])

    clients[addr] = {"uuid": client_uuid, "username": username, "udp_addr": addr}

    response = {
        "action": "connected",
        "uuid": client_uuid,
        "message": f"Welcome, {username}!",
        "player_data": player_info,
        "coordinates": player_info["location"]
    }
    udp_socket.sendto(json.dumps(response).encode('utf-8'), addr)
    print(f"Sent response to {addr}: {response}")
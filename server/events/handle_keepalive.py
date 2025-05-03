import json
import time
import os
from utils.config_handler import load_config  # Import configuration loader

KEEPALIVE_TIMEOUT = 5  # Timeout in seconds to consider a player offline

def get_paths_from_config():
    """Load the player file path and world folder from the configuration."""
    config = load_config()
    player_file_path = os.path.join(config["world"]["world_file"], "players.json")
    world_folder = config["world"]["world_file"]
    return player_file_path, world_folder

def update_player_connection_status(world_folder, uuid, udp_addr, connected):
    """
    Update the player's online status, UDP address, and connection status in the players.json file.
    """
    players_file = os.path.join(world_folder, "players.json")
    if not os.path.exists(players_file):
        print(f"Players file not found at {players_file}. Creating a new one.")
        player_data = {}
    else:
        try:
            with open(players_file, "r") as file:
                player_data = json.load(file)
        except Exception as e:
            print(f"Error loading players.json: {e}")
            return

    if uuid in player_data:
        print(f"Updating connection status for player with UUID {uuid}.")
        player_data[uuid]["online"] = connected
        player_data[uuid]["udp_addr"] = udp_addr
        player_data[uuid]["connected"] = connected
    else:
        print(f"Adding new player with UUID {uuid}.")
        player_data[uuid] = {
            "online": connected,
            "udp_addr": udp_addr,
            "connected": connected
        }

    try:
        with open(players_file, "w") as file:
            json.dump(player_data, file, indent=4)
        print(f"Player connection status updated for UUID {uuid}.")
    except Exception as e:
        print(f"Error saving players.json: {e}")

def handle_keepalive(addr, message, clients):
    """Handle a keepalive message from a UDP client."""
    print(f"Received keepalive from {addr}: {message}")

    # Load paths dynamically from the configuration
    player_file_path, world_folder = get_paths_from_config()

    # Load existing player data from players.json
    if os.path.exists(player_file_path):
        with open(player_file_path, "r") as file:
            player_data = json.load(file)
    else:
        print("Player file not found. Cannot process keepalive.")
        return

    # Check if the client is registered
    if addr not in clients:
        print(f"Unregistered client {addr} sent keepalive. Ignoring.")
        return

    client_uuid = clients[addr]["uuid"]
    player_name = player_data.get(client_uuid, {}).get("username", "Unknown")

    # Update the player's online status and last keepalive time
    if client_uuid in player_data:
        player_data[client_uuid]["last_keepalive"] = time.time()

        # Update the player's connection status
        update_player_connection_status(
            world_folder=world_folder,
            uuid=client_uuid,
            udp_addr=addr,
            connected=True
        )

        print(f"Updated keepalive for player {player_name} (UUID: {client_uuid})")
    else:
        print(f"Player with UUID {client_uuid} not found in players.json.")

def monitor_keepalive(clients):
    """Monitor keepalive messages and mark players offline if timeout occurs."""
    # Load paths dynamically from the configuration
    player_file_path, world_folder = get_paths_from_config()

    while True:
        time.sleep(1)  # Check every second

        # Load existing player data from players.json
        if os.path.exists(player_file_path):
            with open(player_file_path, "r") as file:
                player_data = json.load(file)
        else:
            continue

        # Check for players who have timed out
        current_time = time.time()
        for client_uuid, player_info in player_data.items():
            last_keepalive = player_info.get("last_keepalive", 0)
            if player_info.get("online", False) and current_time - last_keepalive > KEEPALIVE_TIMEOUT:
                print(f"Player {player_info.get('username', 'Unknown')} (UUID: {client_uuid}) timed out. Marking as offline.")

                # Update the player's connection status to offline
                update_player_connection_status(
                    world_folder=world_folder,
                    uuid=client_uuid,
                    udp_addr=None,  # No UDP address when offline
                    connected=False
                )

                # Remove the client from the clients dictionary
                addr_to_remove = None
                for addr, client in clients.items():
                    if client["uuid"] == client_uuid:
                        addr_to_remove = addr
                        break
                if addr_to_remove:
                    del clients[addr_to_remove]
                    print(f"Closed UDP connection for {addr_to_remove}")
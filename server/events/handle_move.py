import json
from utils.config_handler import load_config
from utils.udp_handler import UDPHandler
from world.world_handler import load_players_file, save_players_file  # Import functions to handle player data

# Load configuration
config = load_config()
world_folder = config["world"]["world_file"]  # Get the world folder from the config
udp_host = config["server"]["host"]
udp_port = config["server"]["port"]

# Initialize the UDP connection
udp_handler = UDPHandler(udp_host, udp_port, None)  # No callback needed for this context

def handle_player_move(addr, message, clients):
    """Handle a player movement update and update the player's location in the world file."""
    try:
        if message["action"] != "player_move":
            print(f"Unknown message type received from {addr}: {message}")
            return

        uuid = message.get("uuid")
        new_x = message.get("x")
        new_y = message.get("y")

        if uuid is None or new_x is None or new_y is None:
            print(f"Invalid player_move message from {addr}: {message}")
            return

        print(f"Player {uuid} moved to ({new_x}, {new_y}) from {addr}")

        # Load player data from the players.json file
        player_data = load_players_file()

        if uuid in player_data:
            # Update the player's location in the file
            player_data[uuid]["location"] = {"x": new_x, "y": new_y}
            save_players_file(player_data)  # Save the updated data back to the file
            print(f"Updated player {uuid}'s location in players.json to ({new_x}, {new_y})")
        else:
            print(f"Player {uuid} not found in players.json.")

        # Update the in-memory client data
        if addr in clients:
            clients[addr]["location"] = {"x": new_x, "y": new_y}
            print(f"Updated player {uuid}'s location in memory to ({new_x}, {new_y})")
        else:
            print(f"Player {uuid} not found in clients dictionary.")

        # Send acknowledgment to the client
        response = {
            "action": "player_move_ack",
            "message": f"Player {uuid} moved to ({new_x}, {new_y})."
        }
        udp_handler.server_socket.sendto(json.dumps(response).encode('utf-8'), addr)
        print(f"Sent player_move acknowledgment to {addr}")

    except Exception as e:
        print(f"Error handling player_move message from {addr}: {e}")
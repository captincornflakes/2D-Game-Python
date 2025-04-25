import json
from utils.world_handler import update_player_location  # Import the update_player_location function

def handle_player_move(addr, message, udp_socket, clients=None, world_folder="world"):
    """Handle a player movement update and update the player's location in the world file."""
    try:
        # Check the type of the incoming message
        if message["type"] != "player_move":
            print(f"Unknown message type received from {addr}: {message}")
            return

        # Extract player movement data
        uuid = message.get("uuid")
        new_x = message.get("x")
        new_y = message.get("y")

        if uuid is None or new_x is None or new_y is None:
            print(f"Invalid player_move message from {addr}: {message}")
            return

        print(f"Player {uuid} moved to ({new_x}, {new_y}) from {addr}")

        # Update the player's location in the clients dictionary
        if clients and addr in clients:
            clients[addr]["location"] = {"x": new_x, "y": new_y}
            print(f"Updated player {uuid}'s location in memory to ({new_x}, {new_y})")
        else:
            print(f"Player {uuid} not found in clients dictionary.")

        # Update the player's location in the players.json file
        new_location = {"x": new_x, "y": new_y}
        update_player_location(world_folder, uuid, new_location)

    except Exception as e:
        print(f"Error handling player_move message from {addr}: {e}")
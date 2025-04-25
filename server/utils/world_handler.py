import os
import json
from utils.ops_handler import save_ops_data
from utils.helpers import save_player_data
from utils.worldgen import generate_initial_world  # Import the function from worldgen.py
from utils.config_handler import load_config  # Import the config handler

def initialize_world_folder(world_folder, initial_chunks, world_generator, players, ops, config):
    """Initialize the world folder and generate initial world data if it doesn't exist."""
    if not os.path.exists(world_folder):
        print(f"Creating world folder at {world_folder}...")
        os.makedirs(world_folder)
    else:
        print(f"World folder already exists at {world_folder}.")

    # Generate initial chunks using the function from worldgen.py
    print("Generating initial chunks...")
    generate_initial_world(initial_chunks, world_folder, world_generator)

    # Save world data
    print("Saving world data...")
    save_world_data(world_folder, config)

    # Save player data
    print("Saving player data...")
    save_player_data(players)

    # Save operator data
    print("Saving operator data...")
    save_ops_data(ops, world_folder)

    print("World folder initialization complete.")

def save_world_data(world_folder, config):
    """Save world data to the world-data.json file."""
    world_data = {
        "time": 0,  # Initial world time
        "motd": config["world"]["motd"],
        "game_mode": config["world"]["game_mode"],
        "difficulty": config["world"]["difficulty"]
    }
    world_data_file = os.path.join(world_folder, "world-data.json")
    if not os.path.exists(world_data_file):
        print(f"Saving initial world data to {world_data_file}...")
        with open(world_data_file, 'w') as f:
            json.dump(world_data, f)

def load_world(world_folder, players):
    """Load the world data, count chunks, and reset player connections."""
    chunks_folder = os.path.join(world_folder, "chunks")
    if not os.path.exists(chunks_folder):
        print(f"No chunks folder found in {world_folder}. World might not be initialized.")
        return

    # Count the number of chunks
    chunk_files = [f for f in os.listdir(chunks_folder) if f.endswith(".json")]
    print(f"World loaded with {len(chunk_files)} chunks.")

    # Reset all players' connected status to false
    players_file = os.path.join(world_folder, "players.json")
    if os.path.exists(players_file):
        try:
            with open(players_file, 'r') as f:
                player_data = json.load(f)

            for player_uuid, player_info in player_data.items():
                player_info["connected"] = False

            with open(players_file, 'w') as f:
                json.dump(player_data, f, indent=4)

            print("All players' connected status set to false.")
        except Exception as e:
            print(f"Error resetting player connections: {e}")
    else:
        print(f"No players.json file found in {world_folder}.")

    # Final output message
    print("World file is loaded.")

def get_chunk(chunk_x, chunk_y):
    """Retrieve a specific chunk from the world folder."""
    # Load the world folder path from the config.json file
    config = load_config("config.json")
    world_folder = config["world"]["folder"]

    # Construct the chunk file path
    chunk_file = os.path.join(world_folder, "chunks", f"{chunk_x}x{chunk_y}.json")
    if os.path.exists(chunk_file):
        try:
            with open(chunk_file, 'r') as f:
                chunk_data = json.load(f)
            print(f"Chunk ({chunk_x}, {chunk_y}) loaded successfully.")
            return chunk_data
        except Exception as e:
            print(f"Error loading chunk ({chunk_x}, {chunk_y}): {e}")
            return None
    else:
        print(f"Chunk ({chunk_x}, {chunk_y}) does not exist.")
        return None

def update_player_location(world_folder, uuid, new_location):
    """Update the player's location in the players.json file."""
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
        print(f"Updating location for player with UUID {uuid}.")
        player_data[uuid]["location"] = new_location
    else:
        print(f"Adding new player with UUID {uuid}.")
        player_data[uuid] = {"location": new_location}

    try:
        with open(players_file, "w") as file:
            json.dump(player_data, file, indent=4)
        print(f"Player location for UUID {uuid} successfully updated.")
    except Exception as e:
        print(f"Error saving players.json: {e}")


def update_player_inventory(world_folder, uuid, new_inventory):
    """Update the player's inventory in the players.json file."""
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
        print(f"Updating inventory for player with UUID {uuid}.")
        player_data[uuid]["inventory"] = new_inventory
    else:
        print(f"Adding new player with UUID {uuid}.")
        player_data[uuid] = {"inventory": new_inventory}

    try:
        with open(players_file, "w") as file:
            json.dump(player_data, file, indent=4)
        print(f"Player inventory for UUID {uuid} successfully updated.")
    except Exception as e:
        print(f"Error saving players.json: {e}")


def update_player_stats(world_folder, uuid, new_stats):
    """Update the player's stats in the players.json file."""
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
        print(f"Updating stats for player with UUID {uuid}.")
        player_data[uuid]["stats"] = new_stats
    else:
        print(f"Adding new player with UUID {uuid}.")
        player_data[uuid] = {"stats": new_stats}

    try:
        with open(players_file, "w") as file:
            json.dump(player_data, file, indent=4)
        print(f"Player stats for UUID {uuid} successfully updated.")
    except Exception as e:
        print(f"Error saving players.json: {e}")
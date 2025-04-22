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
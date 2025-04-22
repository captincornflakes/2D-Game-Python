import socket
import os
from world.generator import WorldGenerator
from utils.connection_handler import ConnectionHandler
from utils.player_auth import PlayerAuth
from utils.commands import CommandHandler, handle_console_command
from utils.ops_handler import load_ops
from utils.world_handler import initialize_world_folder, load_world
from utils.config_handler import load_config  # Import the load_config function

# Load configuration using the config handler
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')
CONFIG = load_config(CONFIG_PATH)

# Constants
HOST = CONFIG["server"]["host"]
TCP_PORT = CONFIG["server"]["tcp_port"]
UDP_PORT = CONFIG["server"]["udp_port"]
WORLD_FOLDER = os.path.join(os.path.dirname(__file__), CONFIG["world"]["world_file"])  # Ensure world folder is in the same directory as server.py
OPS_FILE = os.path.join(os.path.dirname(__file__), "ops.json")  # Store ops.json in the same directory as server.py
PLAYERS_FILE = os.path.join(WORLD_FOLDER, "players.json")  # Store players.json in the world folder

# Load operator data
OPS = load_ops()

class GameServer:
    def __init__(self):
        self.chunk_size = 32  # Hardcoded chunk size
        self.initial_chunks = [  # Hardcoded initial chunks
            {"x": 0, "y": 0},
            {"x": 1, "y": 0},
            {"x": 0, "y": 1},
            {"x": 1, "y": 1}
        ]
        self.world_folder = WORLD_FOLDER
        self.players = PlayerAuth(self.world_folder)
        self.command_handler = CommandHandler(self.world_folder, self.players)
        self.connection_handler = ConnectionHandler(HOST, TCP_PORT, UDP_PORT)  # Pass only the required arguments

        # Initialize or load the world folder
        if os.path.exists(self.world_folder):
            print("World folder exists. Loading world...")
            load_world(self.world_folder, self.players)
        else:
            print("World folder does not exist. Initializing world...")
            initialize_world_folder(
                self.world_folder,
                self.initial_chunks,
                None,  # Removed world_generator
                self.players,
                OPS,
                CONFIG
            )

    def start(self):
        """Start the server and handle connections."""
        print(f"Server started on {HOST}:{TCP_PORT} (TCP) and {UDP_PORT} (UDP)")
        print(f"MOTD: {CONFIG['world']['motd']}")
        self.connection_handler.start()  # Start the connection handler

        while True:
            # Wait for console commands
            try:
                command_input = input("> ")
                handle_console_command(self.command_handler, command_input)  # Call the new function
            except KeyboardInterrupt:
                print("\nShutting down the server...")
                break

if __name__ == "__main__":
    server = GameServer()
    server.start()
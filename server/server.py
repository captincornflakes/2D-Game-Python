import socket
import os
from threading import Thread
from world.worldgen import WorldGenerator  # Updated import path
from player.player_auth import PlayerAuth  # Corrected import path
from utils.connection_handler import ConnectionHandler
from utils.commands import CommandHandler, handle_console_command
from utils.ops_handler import load_ops
from utils.config_handler import load_config
from world.world_handler import initialize_or_load_world  # Updated import path

# Load configuration using the config handler
CONFIG = load_config()

# Load operator data using the ops handler
OPS = load_ops()

# Define the world folder based on the configuration
WORLD_FOLDER = CONFIG["world"]["world_file"]

class GameServer:
    def __init__(self):
        # Server configuration
        self.host = CONFIG["server"]["host"]
        self.port = CONFIG["server"]["port"]

        self.world_folder = WORLD_FOLDER
        self.players = PlayerAuth(self.world_folder)
        self.command_handler = CommandHandler(self.world_folder, self.players)
        self.player_file_path = os.path.join(WORLD_FOLDER, "player.json")
        
        # Pass world_folder to the ConnectionHandler
        self.connection_handler = ConnectionHandler(
            self.host,
            self.port,
            self.player_file_path,
            self.world_folder
        )
        self.clients = {}

        # Create a WorldGenerator instance
        self.world_generator = WorldGenerator(self.world_folder, initial_chunks=CONFIG["world"].get("initial_chunks", 10))

        # Initialize or load the world using the world handler
        initialize_or_load_world(
            self.world_folder,
            self.world_generator,
            self.players,
            OPS,
            CONFIG
        )

    def start(self):
        """Start the server and handle connections."""
        print(f"Server started on {self.host}:{self.port} (TCP and UDP)")
        print(f"MOTD: {CONFIG['world']['motd']}")

        self.connection_handler.start()  # Start the connection handler

        while True:
            # Wait for console commands
            try:
                command_input = input("> ")
                handle_console_command(self.command_handler, command_input)
            except KeyboardInterrupt:
                print("\nShutting down the server...")
                break

if __name__ == "__main__":
    server = GameServer()
    server.start()
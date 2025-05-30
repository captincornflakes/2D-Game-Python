import pygame
import os
from pygame.locals import *
from utils.gui_main import main_menu_screen  # Import the main menu screen
from utils.config_man import load_config, save_config  # Import configuration functions
from utils.server_manager import ServerManager  # Import ServerManager
from utils.gui_game import draw_checkered_grid  # Import draw_checkered_grid
from utils.tcp_handler import TCPHandler  # Import TCPHandler
from utils.udp_handler import UDPHandler  # Import UDPHandler

# Constants
TILE_SIZE = 32


class ClientApp:
    def __init__(self):
        """Initialize the client application."""
        pygame.init()
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.config = load_config(self.config_path)  # Load configuration
        self.assets_folder = self.config.get("assets_folder", "assets")
        self.screen_width = self.config.get("screen_width", 1280)
        self.screen_height = self.config.get("screen_height", 720)
        self.splash_image_path = os.path.join(self.assets_folder, "splash_screen.png")

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), RESIZABLE)  # Allow resizing
        pygame.display.set_caption("2D Scroll Survivor - Client")
        self.running = True
        self.server_manager = ServerManager()  # ServerManager will handle server details
        self.connected = False

        # Placeholder variables
        self.port = None  # Placeholder for server port
        self.address = None  # Placeholder for server address
        self.location = {"x": 0, "y": 0}  # Placeholder for player location
        self.stats = {"health": 100, "stamina": 100}  # Placeholder for player stats
        self.inventory = []  # Placeholder for player inventory
        self.uuid = None  # Placeholder for player UUID
        self.player_name = self.config.get("player_name", "Player")  # Default username

        # Initialize TCP and UDP handlers
        self.tcp_handler = TCPHandler(self.address, self.port)  # Initialize TCP handler
        self.udp_handler = UDPHandler(self.address, self.port)  # Initialize UDP handler

    def save_config(self):
        """Save the client configuration."""
        save_config(self.config_path, self.config)

    def game_loop(self):
        """Main game loop."""
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.running = False
                        break
                    elif event.type == VIDEORESIZE:
                        # Handle screen resizing
                        self.screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
                self.screen.fill((0, 0, 0))
                draw_checkered_grid(self.screen, self.location, TILE_SIZE)  # Pass self.location and TILE_SIZE
                pygame.display.flip()
        except Exception as e:
            print(f"Error in game loop: {e}")
        finally:
            self.connected = False

    def run(self):
        """Run the client."""
        try:
            # Call the main menu screen
            main_menu_screen(self.screen, self)
        except pygame.error as e:
            print(f"Pygame error: {e}")
            if "video system not initialized" in str(e):
                pygame.init()
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), RESIZABLE)
                pygame.display.set_caption("2D Scroll Survivor - Client")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            print("Shutting down the client...")
            pygame.quit()


if __name__ == "__main__":
    client_app = ClientApp()
    client_app.run()
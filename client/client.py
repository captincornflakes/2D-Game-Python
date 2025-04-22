import pygame
import os
import socket
import threading
import time
from pygame.locals import *
from utils.gui_main import title_screen
from utils.config_man import load_config, save_config
from utils.player_auth import PlayerAuth
from utils.server_manager import ServerManager
from utils.gui_game import draw_checkered_grid
from utils.event.connect_to_server import connect_to_server
from utils.event.ping_server import ping_server
from utils.tcp_handler import TCPHandler
from utils.udp_handler import UDPHandler
from utils.event.keepalive import start_keepalive  # Import the keepalive function

# Constants
TILE_SIZE = 32

# Load configuration and assets folder
config = load_config("config.json")
assets_folder = config.get("assets_folder", "assets")
SCREEN_WIDTH = config.get("screen_width", 1280)
SCREEN_HEIGHT = config.get("screen_height", 720)
splash_image_path = os.path.join(assets_folder, "splash_screen.png")


class ClientApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Scroll Survivor - Client")
        self.running = True
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.config = load_config(self.config_path)
        self.username = self.config.get("player_name", "Player")  # 'username' is set here
        self.server_address = self.config.get("default_server", "localhost")
        self.port = self.config.get("default_port", 23546)
        self.client_uuid = self.config.get("server_uuids", {}).get(f"{self.server_address}:{self.port}")
        self.tcp_handler = TCPHandler(self.server_address, self.port)
        self.udp_handler = UDPHandler(self.server_address, self.port)
        self.server_manager = ServerManager()
        self.connected = False

    def save_config(self):
        save_config(self.config_path, self.config)

    def connect_to_server(self):
        """Connect to the server and start the keepalive mechanism."""
        if connect_to_server(self, self.client_uuid):
            print("Connected to the server. Starting keepalive...")
            start_keepalive(self)  # Start sending keepalive messages
            return True
        else:
            print("Failed to connect to the server.")
            return False

    def game_loop(self):
        try:
            while self.running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.running = False
                        break
                self.screen.fill((0, 0, 0))
                draw_checkered_grid(self.screen)
                pygame.display.flip()
        except socket.error as e:
            print(f"Socket error: {e}")
            print("Returning to title screen.")
        finally:
            self.udp_handler.close()
            self.tcp_handler.disconnect()
            print("Disconnected from the server.")

    def run(self):
        """Run the client."""
        while self.running:
            try:
                self.username = title_screen(self.screen, self.username, self)
                if self.connect_to_server():
                    self.game_loop()
                else:
                    print("Returning to title screen.")
            except pygame.error as e:
                print(f"Pygame error: {e}")
                if "video system not initialized" in str(e):
                    print("Reinitializing pygame...")
                    pygame.init()
                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    pygame.display.set_caption("2D Scroll Survivor - Client")
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.running = False

        print("Exiting the client application.")


if __name__ == "__main__":
    client_app = ClientApp()
    client_app.run()
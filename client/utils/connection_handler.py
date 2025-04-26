import socket
import pygame
import json
import zlib
import os
import threading
from utils.gui_game import draw_checkered_grid
from utils.config_man import load_config  # Import the config loader
from utils.event.connect_to_server import connect_to_server  # Import the connect event
from utils.event.keepalive import start_keepalive  # Import the keepalive event
from utils.event.ping_server import ping_server  # Ensure ping_server is imported
from utils.tcp_handler import TCPHandler
from utils.udp_handler import UDPHandler

class Client:
    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port
        self.tcp_handler = TCPHandler(server_address, self.port)
        self.udp_handler = UDPHandler(server_address, self.port)
        self.connected = False  # Track connection state


    def disconnect(self):
        """Disconnect from the server."""
        try:
            if self.connected:
                disconnect_message = {"action": "disconnect"}
                self.udp_handler.send_message(disconnect_message)
                self.connected = False
                print("Disconnected from server.")
        except Exception as e:
            print(f"Failed to disconnect: {e}")
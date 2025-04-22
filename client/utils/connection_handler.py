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
from utils.event.ping_server import ping_server  # Import the ping event
from utils.tcp_handler import TCPHandler
from utils.udp_handler import UDPHandler

class Client:
    def __init__(self, server_address, tcp_port, udp_port, player_name="Player"):
        self.server_address = server_address
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.player_name = player_name

        self.tcp_handler = TCPHandler(server_address, tcp_port)
        self.udp_handler = UDPHandler(server_address, udp_port)
        self.connected = False  # Track connection state

    def connect_to_server(self, uuid):
        """Connect to the server using the connect_to_server event."""
        try:
            success = connect_to_server(self.udp_handler, uuid, self.player_name)
            if success:
                print(f"Connected to server: {self.server_address}:{self.udp_port} (UDP)")
                self.connected = True  # Update connection state

                # Start the keepalive mechanism
                start_keepalive(self)
                return True
            else:
                print("Failed to connect to the server.")
                self.connected = False
                return False
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.connected = False
            return False

    def ping_server(self, timeout=2):
        """Ping the server using the ping_server event."""
        try:
            return ping_server(self.tcp_handler, timeout)
        except Exception as e:
            print(f"Failed to ping server: {e}")
            return None

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
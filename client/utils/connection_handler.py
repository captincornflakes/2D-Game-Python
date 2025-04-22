import socket
import pygame
import json
import zlib
import os
import threading
from utils.gui_game import draw_checkered_grid
from utils.config_man import load_config  # Import the config loader
from utils.event.connect_to_server import connect_to_server  # Import the function
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
        """Connect to the server using UDP and send a join request."""
        try:
            join_request = {
                "action": "connect",
                "uuid": uuid,
                "username": self.player_name
            }
            self.udp_handler.send_message(join_request)
            print(f"Sent join request to server: {self.server_address}:{self.udp_port} (UDP)")

            response = self.udp_handler.receive_message()
            if response and response.get("action") == "connected":
                print(f"Connected to server: {response}")
                self.connected = True  # Update connection state
                return True
            else:
                print(f"Failed to connect: {response.get('message', 'Unknown error')}")
                self.connected = False
                return False
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            self.connected = False
            return False

    def ping_server(self, timeout=2):
        """Ping the server to check if it is reachable and retrieve the MOTD."""
        try:
            self.tcp_handler.connect()
            ping_request = {"action": "ping"}
            self.tcp_handler.send_message(ping_request)

            response = self.tcp_handler.receive_message()
            if response and response.get("action") == "pong" and "motd" in response:
                return response["motd"]
            else:
                print(f"Unexpected response: {response}")
                return None
        except Exception as e:
            print(f"Failed to ping server: {e}")
            return None
        finally:
            self.tcp_handler.disconnect()

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
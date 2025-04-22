import json
from utils.tcp_handler import TCPHandler
from utils.udp_handler import UDPHandler
from utils.event.handle_ping import handle_ping
from utils.event.handle_connect import handle_connect
from utils.event.handle_move import handle_move  # Import the handle_move function
from utils.event.handle_tile_update import handle_tile_update  # Import the handle_tile_update function


class ConnectionHandler:
    def __init__(self, host, tcp_port, udp_port):
        self.host = host
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.clients = {}  # Store client info: {addr: {"uuid": ..., "tcp_socket": ..., "udp_addr": ...}}

        # Initialize TCP and UDP handlers
        self.tcp_handler = TCPHandler(host, tcp_port, self.handle_tcp_message)
        self.udp_handler = UDPHandler(host, udp_port, self.handle_udp_message)

    def start(self):
        """Start the TCP and UDP servers."""
        self.tcp_handler.start()
        self.udp_handler.start()

    def handle_tcp_message(self, client_socket, addr, message):
        """Handle a message from a TCP client."""
        action = message.get("action")
        if action == "ping":
            handle_ping(client_socket)
        else:
            print(f"Unhandled TCP action from {addr}: {action}")

    def handle_udp_message(self, addr, message):
        """Handle a message from a UDP client."""
        action = message.get("action")
        if action == "connect":
            self.clients["udp_socket"] = self.udp_handler.server_socket  # Store the UDP socket
            handle_connect(addr, message, self.clients)  # Pass the clients dictionary
        elif action == "move":
            handle_move(addr, message)
        elif action == "tile_update":
            handle_tile_update(addr, message)
        else:
            print(f"Unhandled UDP action from {addr}: {action}")
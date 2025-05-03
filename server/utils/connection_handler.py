import json
import threading
from utils.tcp_handler import TCPHandler
from utils.udp_handler import UDPHandler
from utils.config_handler import load_config
from events.handle_keepalive import handle_keepalive, monitor_keepalive  # Import keepalive handlers

class ConnectionHandler:
    def __init__(self, host, port, player_file_path, world_folder, chunk_size=32):
        self.host = host
        self.port = port  # Single port for both TCP and UDP
        self.clients = {}  # Store client info: {addr: {"uuid": ..., "tcp_socket": ..., "udp_addr": ...}}
        self.player_file_path = player_file_path
        self.world_folder = world_folder
        self.chunk_size = chunk_size

        # Load the configuration to access the MOTD
        self.config = load_config()

        # Initialize TCP and UDP handlers
        self.tcp_handler = TCPHandler(host, port, self.handle_tcp_message)
        self.udp_handler = UDPHandler(host, port, self.handle_udp_message)

    def start(self):
        """Start the TCP and UDP servers and the keepalive monitor."""
        self.tcp_handler.start()
        self.udp_handler.start()

        # Start the keepalive monitor in a separate thread
        threading.Thread(target=monitor_keepalive, args=(self.clients,), daemon=True).start()

    def handle_tcp_message(self, client_socket, addr, message):
        """Handle a message from a TCP client."""
        action = message.get("action")
        if action == "ping":
            print(f"Ping received from {addr}")
            motd = self.config["world"]["motd"]  # Retrieve the MOTD from the config
            response = {"action": "pong", "message": motd}
            client_socket.send(json.dumps(response).encode('utf-8'))
            print(f"Sent MOTD to {addr}: {motd}")
        else:
            print(f"Unhandled TCP action from {addr}: {action}")

    def handle_udp_message(self, addr, message):
        """Handle a message from a UDP client."""
        from events.handle_connect import handle_connect  # Lazy import
        from events.handle_move import handle_player_move  # Lazy import

        action = message.get("action")
        if action == "connect":
            print(f"Connect request received from {addr}")
            handle_connect(addr, message, self.clients, self.udp_handler.server_socket)
        elif action == "player_move":
            print(f"Player move request received from {addr}")
            handle_player_move(addr, message, self.clients)
        elif action == "keepalive":
            print(f"Keepalive message received from {addr}")
            handle_keepalive(addr, message, self.clients)
        else:
            print(f"Unhandled UDP action from {addr}: {action}")
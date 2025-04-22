import socket
import json

class TCPHandler:
    def __init__(self, server_address, tcp_port):
        self.server_address = server_address
        self.tcp_port = tcp_port
        self.tcp_socket = None

    def connect(self):
        """Establish a TCP connection to the server."""
        try:
            self.tcp_socket = socket.create_connection((self.server_address, self.tcp_port))
            print(f"Connected to server at {self.server_address}:{self.tcp_port} (TCP)")
        except Exception as e:
            print(f"Failed to connect to server via TCP: {e}")
            self.tcp_socket = None

    def send_message(self, message):
        """Send a JSON-encoded message to the server over TCP."""
        try:
            if self.tcp_socket:
                self.tcp_socket.sendall(json.dumps(message).encode('utf-8'))
        except Exception as e:
            print(f"Failed to send TCP message: {e}")

    def receive_message(self):
        """Receive a JSON-encoded message from the server over TCP."""
        try:
            if self.tcp_socket:
                data = self.tcp_socket.recv(1024)
                return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Failed to receive TCP message: {e}")
        return None

    def disconnect(self):
        """Close the TCP connection."""
        if self.tcp_socket:
            self.tcp_socket.close()
            self.tcp_socket = None
            print("Disconnected from server (TCP).")
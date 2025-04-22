import socket
import json
import threading


class UDPHandler:
    def __init__(self, host, port, message_callback):
        self.host = host
        self.port = port
        self.message_callback = message_callback  # Callback to handle incoming messages
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        self.running = False

    def start(self):
        """Start the UDP server."""
        self.running = True
        print(f"UDP Server started on {self.host}:{self.port}")
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def listen_for_messages(self):
        """Listen for incoming UDP messages."""
        while self.running:
            try:
                data, addr = self.server_socket.recvfrom(1024)
                print(f"Received UDP message from {addr}: {data.decode('utf-8')}")  # Log the connection
                threading.Thread(target=self.handle_message, args=(data, addr), daemon=True).start()
            except Exception as e:
                print(f"Error receiving UDP message: {e}")

    def handle_message(self, data, addr):
        """Handle a message from a UDP client."""
        try:
            message = json.loads(data.decode('utf-8'))
            self.message_callback(addr, message)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON from {addr}: {e}")

    def stop(self):
        """Stop the UDP server."""
        self.running = False
        self.server_socket.close()
        print("UDP Server stopped.")
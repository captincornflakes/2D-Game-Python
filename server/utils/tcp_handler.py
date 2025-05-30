import socket
import json
import threading


class TCPHandler:
    def __init__(self, host, port, message_callback):
        """Initialize the TCP handler with the host, port, and message callback."""
        self.host = host  # Server host
        self.port = port  # Server port
        self.message_callback = message_callback  # Callback to handle incoming messages
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))  # Bind the socket to the host and port
        self.server_socket.listen(5)  # Listen for incoming connections
        self.running = False

    def start(self):
        """Start the TCP server."""
        self.running = True
        print(f"TCP Server started on {self.host}:{self.port}")
        threading.Thread(target=self.listen_for_clients, daemon=True).start()

    def listen_for_clients(self):
        """Listen for incoming TCP client connections."""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"New TCP connection from {addr}")
                threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
            except Exception as e:
                print(f"Error accepting TCP connection: {e}")

    def handle_client(self, client_socket, addr):
        """Handle communication with a TCP client."""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print(f"TCP client {addr} disconnected.")
                    break

                try:
                    message = json.loads(data.decode('utf-8'))
                    self.message_callback(client_socket, addr, message)
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON from {addr}: {e}")
        except Exception as e:
            print(f"Error handling TCP client {addr}: {e}")
        finally:
            client_socket.close()

    def stop(self):
        """Stop the TCP server."""
        self.running = False
        self.server_socket.close()
        print("TCP Server stopped.")
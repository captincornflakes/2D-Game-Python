import socket
import json

class TCPHandler:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.tcp_socket = None

    def connect(self):
        """Establish a TCP connection to the server."""
        try:
            self.tcp_socket = socket.create_connection((self.address, self.port))
            self.tcp_socket.settimeout(5)  # Set a default timeout for the socket
            print(f"Connected to server at {self.address}:{self.port} (TCP)")
        except Exception as e:
            print(f"Failed to connect to server via TCP: {e}")
            self.tcp_socket = None

    def is_connected(self):
        """Check if the TCP socket is connected."""
        return self.tcp_socket is not None

    def send_message(self, message):
        """Send a JSON-encoded message to the server over TCP."""
        try:
            if self.tcp_socket:
                self.tcp_socket.sendall(json.dumps(message).encode('utf-8'))
                print(f"Sent message: {message}")
            else:
                print("TCP socket is not connected. Cannot send message.")
        except Exception as e:
            print(f"Failed to send TCP message: {e}")

    def receive_message(self, timeout=None):
        """Receive a JSON-encoded message from the server over TCP."""
        try:
            if self.tcp_socket:
                if timeout:
                    self.tcp_socket.settimeout(timeout)  # Set a temporary timeout
                data = self.tcp_socket.recv(1024)
                self.tcp_socket.settimeout(5)  # Reset to default timeout
                return json.loads(data.decode('utf-8'))
            else:
                print("TCP socket is not connected. Cannot receive message.")
                return None
        except socket.timeout:
            print("TCP receive operation timed out.")
            return None
        except Exception as e:
            print(f"Failed to receive TCP message: {e}")
            return None

    def disconnect(self):
        """Close the TCP connection."""
        if self.tcp_socket:
            try:
                self.tcp_socket.close()
                print("Disconnected from server (TCP).")
            except Exception as e:
                print(f"Failed to close TCP socket: {e}")
            finally:
                self.tcp_socket = None
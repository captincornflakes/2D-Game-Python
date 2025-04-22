import socket
import json

class UDPHandler:
    def __init__(self, server_address, udp_port):
        self.server_address = server_address
        self.udp_port = udp_port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(5)

    def send_message(self, message):
        """Send a JSON-encoded message to the server over UDP."""
        try:
            self.udp_socket.sendto(json.dumps(message).encode('utf-8'), (self.server_address, self.udp_port))
        except Exception as e:
            print(f"Failed to send UDP message: {e}")

    def receive_message(self):
        """Receive a JSON-encoded message from the server over UDP."""
        try:
            data, _ = self.udp_socket.recvfrom(65535)  # Increase buffer size to 65535 bytes
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Failed to receive UDP message: {e}")
        return None

    def close(self):
        """Close the UDP socket."""
        self.udp_socket.close()
        print("Closed UDP socket.")
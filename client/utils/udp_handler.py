import socket
import json

class UDPHandler:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(5)

    def send_message(self, message, address=None, port=None):
        """Send a JSON-encoded message to the specified address and port over UDP."""
        target_address = address if address else self.address
        target_port = port if port else self.port

        try:
            self.udp_socket.sendto(json.dumps(message).encode('utf-8'), (target_address, target_port))
            print(f"Sent message to {target_address}:{target_port}: {message}")
        except Exception as e:
            print(f"Failed to send UDP message: {e}")

    def receive_message(self):
        """Receive a JSON-encoded message from the server over UDP."""
        try:
            data, addr = self.udp_socket.recvfrom(65535)  # Increase buffer size to 65535 bytes
            print(f"Received message from {addr}: {data.decode('utf-8')}")
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Failed to receive UDP message: {e}")
        return None

    def close(self):
        """Close the UDP socket."""
        self.udp_socket.close()
        print("Closed UDP socket.")
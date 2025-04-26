import socket
import json

def ping_server(address, port, timeout=2):
    """Ping the server to check if it is reachable and retrieve the MOTD."""
    try:
        # Establish a temporary TCP connection to the server
        with socket.create_connection((address, port), timeout=timeout) as tcp_socket:
            tcp_socket.settimeout(timeout)

            # Send a ping request
            ping_request = {"action": "ping"}
            tcp_socket.sendall(json.dumps(ping_request).encode('utf-8'))

            # Wait for a response
            data = tcp_socket.recv(1024)
            response = json.loads(data.decode('utf-8'))

            # Check if the response contains the expected "pong" action and MOTD
            if response.get("action") == "pong" and "motd" in response:
                return response["motd"]
            else:
                print(f"Unexpected response: {response}")
                return None
    except socket.timeout:
        print(f"Ping to {address}:{port} timed out.")
        return None
    except Exception as e:
        print(f"Failed to ping server at {address}:{port}: {e}")
        return None
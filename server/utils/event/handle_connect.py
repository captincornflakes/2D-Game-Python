import json

def handle_connect(addr, message, clients):
    """Handle a connection request from a UDP client."""
    print(f"Handling connection from {addr}: {message}")

    # Extract client information from the message
    client_uuid = message.get("uuid")
    username = message.get("username")

    if not client_uuid or not username:
        print(f"Invalid connection request from {addr}: Missing 'uuid' or 'username'")
        return

    # Register the client in the clients dictionary
    clients[addr] = {
        "uuid": client_uuid,
        "username": username,
        "udp_addr": addr
    }

    print(f"Registered client {username} with UUID {client_uuid} at {addr}")

    # Send a response to the client
    response = {
        "action": "connected",
        "message": f"Welcome, {username}!"
    }
    response_data = json.dumps(response).encode('utf-8')

    # Send the response back to the client
    udp_socket = clients.get("udp_socket")  # Ensure the UDP socket is available
    if udp_socket:
        udp_socket.sendto(response_data, addr)
    else:
        print("UDP socket not available to send response.")
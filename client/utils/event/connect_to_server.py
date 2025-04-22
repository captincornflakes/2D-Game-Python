def connect_to_server(client, uuid):
    """Connect to the server using UDP and send a join request."""
    try:
        join_request = {
            "action": "connect",
            "uuid": uuid,
            "username": client.username  # Use 'username' instead of 'player_name'
        }
        client.udp_handler.send_message(join_request)
        print(f"Sent join request to server: {client.server_address}:{client.udp_handler.udp_port} (UDP)")

        response = client.udp_handler.receive_message()
        if response and response.get("action") == "connected":
            print(f"Connected to server: {response}")
            client.connected = True  # Update connection state
            return True
        else:
            print(f"Failed to connect: {response.get('message', 'Unknown error')}")
            client.connected = False
            return False
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        client.connected = False
        return False
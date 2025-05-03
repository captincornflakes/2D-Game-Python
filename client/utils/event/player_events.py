def request_players(client, callback=None):
    """Request player data from the server."""
    try:
        # Send a request for players to the server
        player_request = {"type": "request_players"}
        client.udp_handler.send_message(player_request)
        print("Player request sent to the server.")

        # Wait for the server's response
        response = client.udp_handler.receive_message()
        if response and response.get("type") == "player_data":
            print(f"Player data received: {response}")
            if callback:
                callback(response)  # Pass the response to the callback function
        else:
            print("Invalid or no response received for player request.")
    except Exception as e:
        print(f"Error requesting players: {e}")


def send_player_move(client, x, y):
    """Send a player_move event to the server with the player's x and y coordinates."""
    try:
        # Create the player_move message
        player_move_message = {
            "action": "player_move",
            "uuid": client.player_data.get("uuid"),  # Use the player's UUID
            "x": x,
            "y": y
        }
        # Send the message to the server
        client.udp_handler.send_message(player_move_message)
        print(f"Player move sent to the server: {player_move_message}")
    except Exception as e:
        print(f"Error sending player move: {e}")
def request_tiles(udp_handler, player_grid_coords, callback):
    """Request tile data from the server and pass the response to the callback."""
    try:
        # Send a request for tiles to the server with the player's grid coordinates
        message = {
            "type": "request_tiles",
            "player_coords": {
                "x": player_grid_coords[0],
                "y": player_grid_coords[1]
            }
        }
        udp_handler.send_message(message)  # Use the UDPHandler to send the message
        print(f"Tile request sent to the server with player coordinates: {player_grid_coords}")

        # Wait for the server's response
        response_data = udp_handler.receive_message()
        if response_data:
            response, addr = response_data
            if response and response.get("type") == "tile_data":
                print(f"Tile data received from server: {response}")
                callback(response)  # Pass the tile data to the callback function
            else:
                print("Invalid tile data received from the server.")
        else:
            print("No response received from the server.")
    except Exception as e:
        print(f"Error requesting tiles: {e}")
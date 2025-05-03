import json
from world.world_handler import get_chunk  # Updated import path

def handle_request_tiles(addr, message, udp_socket, chunk_size=32):
    """Handle a tile request from the client."""
    try:
        # Extract player coordinates from the message
        player_coords = message.get("player_coords", {})
        x = player_coords.get("x", 0)
        y = player_coords.get("y", 0)
        print(f"Tile request received from {addr} for coordinates: ({x}, {y})")

        # Calculate the chunk coordinates based on the player's position and chunk size
        chunk_x = x // chunk_size
        chunk_y = y // chunk_size

        # Retrieve the chunk data using the get_chunk function
        chunk_data = get_chunk(chunk_x, chunk_y)

        if chunk_data:
            # Send the tile data back to the client
            tile_data = {
                "type": "tile_data",
                "chunk_coords": {"x": chunk_x, "y": chunk_y},
                "tiles": chunk_data["tiles"],
            }
            udp_socket.sendto(json.dumps(tile_data).encode(), addr)
            print(f"Tile data sent to {addr}: {tile_data}")
        else:
            print(f"Failed to retrieve chunk ({chunk_x}, {chunk_y}) for {addr}.")
    except Exception as e:
        print(f"Error handling tile request from {addr}: {e}")
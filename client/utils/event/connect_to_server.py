import pygame

def connect_to_server(client, screen, address, port):
    """Connect to the server using UDP and send a join request, with a loading screen."""
    try:
        # Update the client's address and port
        client.address = address
        client.port = port
        client.udp_handler.address = address
        client.udp_handler.port = port

        # Display the loading screen
        screen.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 50)  # Font for the loading text
        loading_text = font.render("Loading...", True, (255, 255, 255))  # White text
        text_rect = loading_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(loading_text, text_rect)
        pygame.display.flip()  # Update the display

        # Send the join request to the server
        join_request = {
            "action": "connect",
            "username": client.player_name  # Use the player's username
        }
        client.udp_handler.send_message(join_request)
        print(f"Sent join request to server: {address}:{port} (UDP)")

        # Wait for the server's response
        response = client.udp_handler.receive_message()
        if response and response.get("action") == "connected":
            print(f"Connected to server: {response}")
            
            # Store the received player data, coordinates, and UUID in the client object
            client.player_data = response.get("player_data", {})
            client.coordinates = response.get("coordinates", {"x": 0, "y": 0})
            client.client_uuid = response.get("uuid")  # Store the UUID provided by the server
            
            print(f"Player data stored: {client.player_data}")
            print(f"Player coordinates stored: {client.coordinates}")
            print(f"Client UUID stored: {client.client_uuid}")
            
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
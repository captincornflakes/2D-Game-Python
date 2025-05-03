import pygame

def connect_to_server(client, screen, address, port):
    """Connect to the server using UDP and send a join request, with a loading screen."""
    try:
        client.address = address
        client.port = port
        client.udp_handler.address = address
        client.udp_handler.port = port

        # Display the loading screen
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        loading_text = font.render("Loading...", True, (255, 255, 255))
        text_rect = loading_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(loading_text, text_rect)
        pygame.display.flip()

        # Send the join request
        join_request = {
            "action": "connect",
            "username": client.player_name
        }
        client.udp_handler.send_message(join_request, address=address, port=port)
        print(f"Sent join request to server at {address}:{port}: {join_request}")

        # Wait for the server's response
        response = client.udp_handler.receive_message()
        if response is None:
            print("No response received from the server.")
            client.connected = False
            return False

        if response.get("action") == "connected":
            print(f"Connected to server: {response}")
            client.player_data = response.get("player_data", {})
            client.coordinates = response.get("coordinates", {"x": 0, "y": 0})
            client.uuid = response.get("uuid")
            client.connected = True


            return True
        else:
            print(f"Failed to connect: {response.get('message', 'Unknown error')}")
            client.connected = False
            return False
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        client.connected = False
        return False
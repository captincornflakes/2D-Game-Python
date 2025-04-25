import pygame
from utils.event.player_events import send_player_move  # Import the send_player_move function

def handle_keybinds(event, grid_offset, client, keybinds):
    """Handle keybind interactions, update the grid offset, and send player movement to the server."""
    if event.type == pygame.KEYDOWN:
        try:
            # Check if the pressed key matches any keybind
            for action, key in keybinds.keybinds.items():
                if event.key == pygame.key.key_code(key):
                    print(f"Action triggered: {action}")  # Placeholder for action handling
                    # Update the grid offset to simulate movement
                    if action == "up":
                        grid_offset[1] -= 1  # Move the grid down (player moves up)
                        client.coordinates["y"] -= 1  # Update player's y-coordinate
                        send_player_move(client, client.coordinates["x"], client.coordinates["y"])
                        print("Move up")
                    elif action == "down":
                        grid_offset[1] += 1  # Move the grid up (player moves down)
                        client.coordinates["y"] += 1  # Update player's y-coordinate
                        send_player_move(client, client.coordinates["x"], client.coordinates["y"])
                        print("Move down")
                    elif action == "left":
                        grid_offset[0] -= 1  # Move the grid right (player moves left)
                        client.coordinates["x"] -= 1  # Update player's x-coordinate
                        send_player_move(client, client.coordinates["x"], client.coordinates["y"])
                        print("Move left")
                    elif action == "right":
                        grid_offset[0] += 1  # Move the grid left (player moves right)
                        client.coordinates["x"] += 1  # Update player's x-coordinate
                        send_player_move(client, client.coordinates["x"], client.coordinates["y"])
                        print("Move right")
        except ValueError:
            # Ignore unknown keys that are not in the keybindings
            print(f"Unknown key pressed: {event.key}")
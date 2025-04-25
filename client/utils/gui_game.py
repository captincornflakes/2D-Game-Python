import pygame
from utils.config_man import load_config  # Import the configuration loader
from utils.gui_utils import unload_previous_guis  # Import unload_previous_guis
from utils.event.keepalive import start_keepalive  # Import the keepalive function
from utils.keybindings import Keybinds  # Import the Keybinds handler
from utils.event.tile_events import request_tiles  # Import the request_tiles event
from utils.event.player_events import request_players  # Import the request_players event
from utils.event.entity_events import request_entities  # Import the request_entities event
from utils.event.player_events import send_player_move  # Import the send_player_move function

# Load configuration to get the scaling factor and refresh rate limit
config = load_config("config.json")
gui_scale = config.get("gui_scale", 1.0)  # Default to 1.0 if not specified
refresh_rate_limit = config.get("refresh_rate_limit", 60)  # Default to 60 FPS if not specified

# Initialize the Keybinds handler
keybinds = Keybinds()

def draw_checkered_grid(screen, grid_offset, base_grid_size=32, light_gray=(200, 200, 200), dark_gray=(150, 150, 150)):
    """Draw a checkered grid on the screen and assign coordinates to each square."""
    # Adjust grid size based on the scaling factor
    scaled_grid_size = int(base_grid_size * gui_scale)

    screen_width, screen_height = screen.get_size()

    # Calculate the center of the screen in terms of grid coordinates
    center_x = screen_width // 2
    center_y = screen_height // 2

    for y in range(0, screen_height, scaled_grid_size):
        for x in range(0, screen_width, scaled_grid_size):
            # Calculate grid coordinates relative to the grid offset
            grid_x = (x - center_x) // scaled_grid_size + grid_offset[0]
            grid_y = (center_y - y) // scaled_grid_size + grid_offset[1]  # Invert y-axis for top-down coordinates

            # Alternate between light gray and dark gray
            if (x // scaled_grid_size + y // scaled_grid_size) % 2 == 0:
                color = light_gray
            else:
                color = dark_gray

            # Draw the grid square
            pygame.draw.rect(screen, color, pygame.Rect(x, y, scaled_grid_size, scaled_grid_size))

            # Render the grid coordinates
            font = pygame.font.Font(None, 20)  # Small font for coordinates
            coord_text = font.render(f"{grid_x},{grid_y}", True, (0, 0, 0))  # Black text
            text_rect = coord_text.get_rect(center=(x + scaled_grid_size // 2, y + scaled_grid_size // 2))
            screen.blit(coord_text, text_rect)

def handle_keybinds(event, grid_offset, client):
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

def game_gui_loop(screen, client, main_menu_screen):
    """Main GUI loop for the game."""
    udp_handler = client.udp_handler  # Get the UDP handler from the client

    clock = pygame.time.Clock()
    grid_offset = [0, 0]  # Initialize grid offset (x, y)
    base_grid_size = 32  # Base grid size
    paused = False  # Initialize the paused state
    tile_data = {}  # Store the received tile data

    def handle_tile_data(data):
        """Callback to handle received tile data."""
        nonlocal tile_data
        tile_data = data  # Update the tile data
        print(f"Tile data updated: {tile_data}")

    # Request initial data
    request_tiles(udp_handler, grid_offset, handle_tile_data)  # Pass the callback function

    # Set the grid offset based on the player's coordinates
    grid_offset[0] = int(client.coordinates.get("x", 0))
    grid_offset[1] = int(client.coordinates.get("y", 0))

    while client.connected:  # Keep running the game loop while the client is connected
        # Clear the screen
        screen.fill((0, 0, 0))  # Black background

        if not paused:
            # Draw the grid
            draw_checkered_grid(screen, grid_offset, base_grid_size)

            # Draw the player (centered on the screen)
            draw_player(screen, base_grid_size)

            # Use the received tile data (if available)
            if tile_data:
                for tile in tile_data.get("tiles", []):
                    print(f"Rendering tile at {tile['location']} with type {tile['type']}")

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.connected = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggle pause state
            elif not paused:
                handle_keybinds(event, grid_offset, client)

        if paused:
            action = draw_pause_menu(screen, client, main_menu_screen)
            if action == "resume":
                paused = False
            elif action == "quit":
                return

        # Update the display
        pygame.display.flip()
        clock.tick(refresh_rate_limit)

    print("Client disconnected. Returning to the main menu.")
    main_menu_screen(screen, client.username, client)

def draw_player(screen, base_grid_size=32):
    """Draw the player sprite fixed at the center of the screen."""
    # Adjust player size based on the grid size and scaling factor
    scaled_grid_size = int(base_grid_size * gui_scale)
    player_size = scaled_grid_size  # Player size matches the size of one tile
    player_color = (255, 0, 0)  # Red color for the player sprite

    # Calculate the center of the screen
    screen_width, screen_height = screen.get_size()
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Draw the player as a rectangle fixed at the center of the screen
    player_x = center_x - (player_size // 2)
    player_y = center_y - (player_size // 2)
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

def draw_pause_menu(screen, client, main_menu_screen):
    """Draw a transparent overlay with two buttons for the pause menu."""
    screen_width, screen_height = screen.get_size()

    # Draw a semi-transparent overlay
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
    screen.blit(overlay, (0, 0))

    # Button properties
    button_width, button_height = 200, 50
    font = pygame.font.Font(None, 36)

    # Quit button
    quit_button_rect = pygame.Rect(
        screen_width // 2 - button_width // 2,
        screen_height // 2 - button_height - 10,
        button_width,
        button_height,
    )
    pygame.draw.rect(screen, (200, 0, 0), quit_button_rect)  # Red button
    quit_text = font.render("Quit", True, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    screen.blit(quit_text, quit_text_rect)

    # Resume button
    resume_button_rect = pygame.Rect(
        screen_width // 2 - button_width // 2,
        screen_height // 2 + 10,
        button_width,
        button_height,
    )
    pygame.draw.rect(screen, (0, 200, 0), resume_button_rect)  # Green button
    resume_text = font.render("Resume", True, (255, 255, 255))
    resume_text_rect = resume_text.get_rect(center=resume_button_rect.center)
    screen.blit(resume_text, resume_text_rect)

    # Handle button clicks
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button_rect.collidepoint(event.pos):
                print("Quit button clicked")
                client.connected = False  # Exit the game loop
                main_menu_screen(screen, client.username, client)  # Load the server selector
                return "quit"  # Indicate that the game should quit
            elif resume_button_rect.collidepoint(event.pos):
                print("Resume button clicked")
                return "resume"  # Indicate that the game should resume
    return None  # No action taken
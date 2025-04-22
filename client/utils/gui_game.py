import pygame
from utils.gui_utils import draw_checkered_grid, unload_previous_guis  # Import unload_previous_guis
from utils.event.keepalive import start_keepalive  # Import the keepalive function

def game_gui_loop(screen, client):
    """Main GUI loop for the game."""
    # Ensure pygame is initialized
    if not pygame.get_init():
        print("Pygame not initialized. Initializing now...")
        pygame.init()

    unload_previous_guis()  # Unload other GUIs before starting the game loop

    # Start the keepalive mechanism
    if client.connected:
        start_keepalive(client)
    else:
        print("Client is not connected. Keepalive will not start.")

    clock = pygame.time.Clock()

    while True:
        # Clear the screen
        screen.fill((0, 0, 0))  # Black background

        # Draw the grid
        draw_checkered_grid(screen)  # Call the imported function

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS
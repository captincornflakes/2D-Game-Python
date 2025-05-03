import pygame
import os
from utils.config_man import load_config  # Ensure configuration loader is imported

# Load configuration to get the scaling factor
config = load_config("config.json")
gui_scale = config.get("gui_scale", 1.0)  # Default to 1.0 if not specified

def draw_button(screen, rect, text, font, background_color=(200, 200, 200), border_color=(255, 255, 255), text_color=(0, 0, 0)):
    pygame.draw.rect(screen, background_color, rect)  # Draw the button background
    pygame.draw.rect(screen, border_color, rect, 2)  # Draw the border
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

def unload_previous_guis():
    pygame.event.clear()  # Clear the event queue

def draw_splash_screen(screen, client):
    """Draw the splash screen as the background."""
    if hasattr(client, "splash_image") and client.splash_image:
        # Use the preloaded splash image from the client
        splash_image = pygame.transform.scale(client.splash_image, (screen.get_width(), screen.get_height()))
    else:
        # Load the splash image from the file system if not already loaded
        splash_image_path = client.splash_image_path
        if not os.path.exists(splash_image_path):
            raise FileNotFoundError(f"Splash screen image not found at {splash_image_path}")
        splash_image = pygame.image.load(splash_image_path)
        splash_image = pygame.transform.scale(splash_image, (screen.get_width(), screen.get_height()))
        # Cache the loaded splash image in the client object
        client.splash_image = splash_image

    # Draw the splash image on the screen
    screen.blit(splash_image, (0, 0))

def draw_checkered_grid(screen, grid_offset, base_grid_size=32):
    """Draw a checkered grid on the screen."""
    light_gray = (200, 200, 200)
    dark_gray = (150, 150, 150)

    scaled_grid_size = int(base_grid_size * gui_scale)
    screen_width, screen_height = screen.get_size()

    for y in range(0, screen_height, scaled_grid_size):
        for x in range(0, screen_width, scaled_grid_size):
            # Alternate between light gray and dark gray
            color = light_gray if (x // scaled_grid_size + y // scaled_grid_size) % 2 == 0 else dark_gray
            pygame.draw.rect(screen, color, pygame.Rect(x, y, scaled_grid_size, scaled_grid_size))

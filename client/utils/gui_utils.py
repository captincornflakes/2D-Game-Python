import pygame
from utils.config_man import load_config  # Import the configuration loader

# Load configuration to get the scaling factor
config = load_config("config.json")
gui_scale = config.get("gui_scale", 1.0)  # Default to 1.0 if not specified

def draw_button(screen, rect, text, font, background_color=(200, 200, 200), border_color=(255, 255, 255), text_color=(0, 0, 0)):
    """Draw a button with a gray background, border, and black text."""
    pygame.draw.rect(screen, background_color, rect)  # Draw the button background
    pygame.draw.rect(screen, border_color, rect, 2)  # Draw the border
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

def unload_previous_guis():
    """Unload resources or states from previous GUIs."""
    pygame.event.clear()  # Clear the event queue
    print("Previous GUIs unloaded.")  # Debug message

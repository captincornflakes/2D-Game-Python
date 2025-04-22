import pygame
import os
from utils.gui_utils import draw_button  # Import draw_button from gui_utils
from utils.gui_settings import display_settings_screen  # Import from gui_settings
from utils.gui_server import display_join_server_screen  # Import the server GUI function

def display_loading_screen(screen, splash_image_path):
    """Display the loading screen with title, buttons, and a splash screen background."""
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)

    # Load the splash screen image
    splash_image = pygame.image.load(splash_image_path)
    splash_image = pygame.transform.scale(splash_image, (screen.get_width(), screen.get_height()))

    while True:
        # Draw the splash screen as the background
        screen.blit(splash_image, (0, 0))

        # Title
        title = title_font.render("2D Scroll Survivor", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

        # Buttons
        join_rect = pygame.Rect(screen.get_width() // 2 - 100, 250, 200, 50)
        settings_rect = pygame.Rect(screen.get_width() // 2 - 100, 350, 200, 50)

        draw_button(screen, join_rect, "Join a Server", font)
        draw_button(screen, settings_rect, "Settings", font)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if join_rect.collidepoint(event.pos):
                    return "join_server"  # Navigate to the "Join a Server" screen
                if settings_rect.collidepoint(event.pos):
                    return "settings"  # Navigate to the "Settings" screen

        pygame.display.flip()

def title_screen(screen, username, client_app):
    """Display the title screen with navigation to other screens."""
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)

    assets_folder = client_app.config.get("assets_folder", "assets")
    splash_image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), assets_folder, "splash_screen.png")

    # Load the splash screen image
    splash_image = pygame.image.load(splash_image_path)
    splash_image = pygame.transform.scale(splash_image, (screen.get_width(), screen.get_height()))

    while True:
        # Draw the splash screen as the background
        screen.blit(splash_image, (0, 0))

        # Title
        title = title_font.render("2D Scroll Survivor", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

        # Buttons
        join_rect = pygame.Rect(screen.get_width() // 2 - 100, 250, 200, 50)
        settings_rect = pygame.Rect(screen.get_width() // 2 - 100, 350, 200, 50)

        draw_button(screen, join_rect, "Join a Server", font)
        draw_button(screen, settings_rect, "Settings", font)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if join_rect.collidepoint(event.pos):
                    # Navigate to the server selector screen
                    connected = display_join_server_screen(screen, splash_image_path, client_app)
                    if connected:
                        return username  # Return to the main game loop
                if settings_rect.collidepoint(event.pos):
                    # Navigate to the settings screen
                    username = display_settings_screen(screen, username, splash_image_path)

        pygame.display.flip()
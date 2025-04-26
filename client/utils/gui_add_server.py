import pygame
from pygame.locals import *
from utils.gui_utils import draw_button, draw_splash_screen  # Import draw_splash_screen
from utils.server_manager import ServerManager  # Import the ServerManager class

def display_add_server_screen(screen, client):
    """Display the 'Add Server' screen."""
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 28)

    # Initialize the ServerManager
    server_manager = ServerManager()

    # Input fields for adding a new server
    input_active = {"name": False, "address": False, "port": False}
    input_text = {"name": "", "address": "", "port": ""}
    input_boxes = {
        "name": pygame.Rect(300, 200, 200, 40),
        "address": pygame.Rect(300, 250, 200, 40),
        "port": pygame.Rect(300, 300, 200, 40),
    }

    while True:
        # Draw the splash screen as the background
        draw_splash_screen(screen, client)

        # Title
        title = font.render("Add Server", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        # Input fields for adding a new server
        for key, rect in input_boxes.items():
            pygame.draw.rect(screen, (200, 200, 200), rect)  # Gray background
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # White border
            label_rect = pygame.Rect(rect.x - 120, rect.y, 100, rect.height)
            pygame.draw.rect(screen, (255, 255, 255), label_rect)  # White background
            pygame.draw.rect(screen, (0, 0, 0), label_rect, 2)  # Black border
            label = input_font.render(f"{key.capitalize()}:", True, (0, 0, 0))  # Black text
            screen.blit(label, (label_rect.x + 5, label_rect.y + 5))
            text_surface = input_font.render(input_text[key], True, (0, 0, 0))  # Black text
            screen.blit(text_surface, (rect.x + 5, rect.y + 5))

        # Save Button
        save_button_rect = pygame.Rect(300, 350, 150, 50)
        draw_button(screen, save_button_rect, "Save", font)

        # Back Button
        back_button_rect = pygame.Rect(500, 350, 150, 50)
        draw_button(screen, back_button_rect, "Back", font)

        # Event handling
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                for key, rect in input_boxes.items():
                    if rect.collidepoint(event.pos):
                        input_active = {k: False for k in input_active}  # Deactivate all
                        input_active[key] = True
                    else:
                        input_active[key] = False

                if save_button_rect.collidepoint(event.pos):
                    if input_text["name"] and input_text["address"] and input_text["port"].isdigit():
                        server_manager.add_server(input_text["name"], input_text["address"], int(input_text["port"]))
                        return  # Return to the previous screen

                if back_button_rect.collidepoint(event.pos):
                    return  # Return to the previous screen

            if event.type == KEYDOWN:
                for key, active in input_active.items():
                    if active:
                        if event.key == K_BACKSPACE:
                            input_text[key] = input_text[key][:-1]
                        else:
                            input_text[key] += event.unicode

        pygame.display.flip()
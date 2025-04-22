import pygame
import os
from utils.gui_utils import draw_button  # Import draw_button from gui_utils

def display_settings_screen(screen, username, splash_image_path):
    """Display the 'Settings' screen."""
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 28)
    input_box = pygame.Rect(300, 250, 200, 40)
    input_active = False
    input_text = username

    # Load the splash screen image
    splash_image = pygame.image.load(splash_image_path)
    splash_image = pygame.transform.scale(splash_image, (screen.get_width(), screen.get_height()))

    while True:
        # Draw the splash screen as the background
        screen.blit(splash_image, (0, 0))

        # Title
        title = font.render("Settings", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))

        # Label for username input
        username_label = input_font.render("Username:", True, (255, 255, 255))
        screen.blit(username_label, (input_box.x + input_box.width // 2 - username_label.get_width() // 2, input_box.y - 30))

        # Input box for username
        pygame.draw.rect(screen, (200, 200, 200), input_box)  # Gray background
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)  # White border
        username_render = input_font.render(input_text, True, (0, 0, 0))  # Black text
        screen.blit(username_render, (input_box.x + 5, input_box.y + 5))

        # Back Button
        back_rect = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)
        pygame.draw.rect(screen, (200, 200, 200), back_rect)  # Draw button background
        pygame.draw.rect(screen, (255, 255, 255), back_rect, 2)  # Draw button border
        back_text = font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # Save Button
        save_rect = pygame.Rect(screen.get_width() // 2 - 100, 320, 200, 50)
        pygame.draw.rect(screen, (200, 200, 200), save_rect)  # Draw button background
        pygame.draw.rect(screen, (255, 255, 255), save_rect, 2)  # Draw button border
        save_text = font.render("Save", True, (0, 0, 0))
        save_text_rect = save_text.get_rect(center=save_rect.center)
        screen.blit(save_text, save_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return input_text  # Return the updated username
                if save_rect.collidepoint(event.pos):
                    print(f"Username '{input_text}' saved!")  # Simulate saving the username
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.display.flip()

import pygame
from utils.gui_utils import draw_button, draw_splash_screen  # Add draw_splash_screen
from utils.gui_keybindings import display_keybindings_screen  # Ensure keybindings GUI is imported

def display_settings_screen(screen, client):
    username = client.player_name  # Get the username from the client app
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 28)
    input_box = pygame.Rect(300, 250, 200, 40)
    input_active = False
    input_text = username

    while True:
        screen.fill((0, 0, 0))
        draw_splash_screen(screen, client)

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

        # Save Button
        save_rect = pygame.Rect(screen.get_width() // 2 - 100, 320, 200, 50)
        draw_button(screen, save_rect, "Save", font)

        # Keybinds Button
        keybinds_rect = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)
        draw_button(screen, keybinds_rect, "Keybinds", font)

        # Back Button
        back_rect = pygame.Rect(screen.get_width() // 2 - 100, 480, 200, 50)
        draw_button(screen, back_rect, "Back", font)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return input_text  # Return the updated username
                if save_rect.collidepoint(event.pos):
                    print(f"Username '{input_text}' saved!")  # Simulate saving the username
                if keybinds_rect.collidepoint(event.pos):
                    display_keybindings_screen(screen, client)
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

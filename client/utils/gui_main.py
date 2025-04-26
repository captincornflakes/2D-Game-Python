import pygame
from utils.gui_utils import draw_button, draw_splash_screen  # Ensure draw_splash_screen is imported
from utils.gui_settings import display_settings_screen  # Ensure settings GUI is imported
from utils.gui_server import display_join_server_screen  # Ensure server GUI is imported

def main_menu_screen(screen, client):
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)

    while True:
        screen.fill((0, 0, 0))
        draw_splash_screen(screen, client)

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
                    display_join_server_screen(screen, client)
                if settings_rect.collidepoint(event.pos):
                    # Navigate to the settings screen
                    client.username = display_settings_screen(screen, client)

        pygame.display.flip()
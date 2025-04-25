import pygame
from pygame.locals import *
from utils.keybindings import Keybinds
from utils.gui_utils import draw_button

def display_keybindings_screen(screen, splash_image_path):
    """Display the 'Keybindings' screen in a grid layout with two columns."""
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 28)

    # Initialize the Keybinds handler
    keybinds = Keybinds()

    # Input fields for each keybind
    input_active = {action: False for action in keybinds.keybinds}
    input_text = keybinds.keybinds.copy()
    input_boxes = {}

    # Grid layout configuration
    column_width = screen.get_width() // 2 - 100
    row_height = 60
    x_positions = [200, column_width + 200]  # Two columns
    y_start = 150
    y_offset = y_start

    # Create input boxes for each keybind
    for i, action in enumerate(keybinds.keybinds):
        column = i % 2  # Alternate between two columns
        row = i // 2
        x = x_positions[column]
        y = y_start + row * row_height
        input_boxes[action] = pygame.Rect(x + 200, y, 200, 40)

    # Load the splash screen image
    splash_image = pygame.image.load(splash_image_path)
    splash_image = pygame.transform.scale(splash_image, (screen.get_width(), screen.get_height()))

    while True:
        # Draw the splash screen as the background
        screen.blit(splash_image, (0, 0))

        # Title
        title = font.render("Keybindings", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        # Draw input fields for each keybind
        for i, (action, rect) in enumerate(input_boxes.items()):
            # Label
            label = input_font.render(f"{action.replace('_', ' ').capitalize()}:", True, (255, 255, 255))
            screen.blit(label, (rect.x - 200, rect.y + 5))

            # Input box
            pygame.draw.rect(screen, (200, 200, 200), rect)  # Gray background
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # White border
            text_surface = input_font.render(input_text[action], True, (0, 0, 0))  # Black text
            screen.blit(text_surface, (rect.x + 5, rect.y + 5))

        # Save Button
        save_button_rect = pygame.Rect(50, screen.get_height() - 150, 100, 50)
        draw_button(screen, save_button_rect, "Save", font)

        # Back Button
        back_button_rect = pygame.Rect(50, screen.get_height() - 80, 100, 50)
        draw_button(screen, back_button_rect, "Back", font)

        # Event handling
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                for action, rect in input_boxes.items():
                    if rect.collidepoint(event.pos):
                        input_active = {a: False for a in input_active}  # Deactivate all
                        input_active[action] = True
                    else:
                        input_active[action] = False

                if save_button_rect.collidepoint(event.pos):
                    # Save updated keybindings using the Keybinds handler
                    for action in input_text:
                        keybinds.update_keybind(action, input_text[action])
                    print("Keybindings saved!")
                    return  # Return to the previous screen

                if back_button_rect.collidepoint(event.pos):
                    return  # Return to the previous screen

            if event.type == KEYDOWN:
                for action, active in input_active.items():
                    if active:
                        if event.key == K_BACKSPACE:
                            input_text[action] = input_text[action][:-1]
                        else:
                            input_text[action] = pygame.key.name(event.key).upper()

        pygame.display.flip()
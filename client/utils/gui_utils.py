import pygame

def draw_button(screen, rect, text, font, background_color=(200, 200, 200), border_color=(255, 255, 255), text_color=(0, 0, 0)):
    """Draw a button with a gray background, border, and black text."""
    pygame.draw.rect(screen, background_color, rect)  # Draw the button background
    pygame.draw.rect(screen, border_color, rect, 2)  # Draw the border
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)
    
    
def draw_checkered_grid(screen, grid_size=32, light_gray=(200, 200, 200), dark_gray=(150, 150, 150)):
    """Draw a checkered grid on the screen."""
    screen_width, screen_height = screen.get_size()

    for y in range(0, screen_height, grid_size):
        for x in range(0, screen_width, grid_size):
            # Alternate between light gray and dark gray
            if (x // grid_size + y // grid_size) % 2 == 0:
                color = light_gray
            else:
                color = dark_gray
            pygame.draw.rect(screen, color, pygame.Rect(x, y, grid_size, grid_size))

def unload_previous_guis():
    """Unload resources or states from previous GUIs."""
    pygame.event.clear()  # Clear the event queue
    print("Previous GUIs unloaded.")  # Debug message

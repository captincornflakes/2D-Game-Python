import os
import threading
import time
import pygame
from pygame.locals import *
from utils.server_manager import ServerManager
from utils.gui_utils import draw_button, draw_splash_screen
from utils.gui_game import game_gui_loop
from utils.gui_edit_server import display_edit_server_screen
from utils.gui_add_server import display_add_server_screen
from utils.event.ping_server import ping_server

def display_join_server_screen(screen, client_app):
    """Display the join server screen."""
    from utils.gui_main import main_menu_screen  # Lazy import
    from utils.event.connect_to_server import connect_to_server  # Lazy import

    font = pygame.font.Font(None, 36)
    server_manager = ServerManager()
    servers = server_manager.get_all_servers()

    # Load icons for edit, delete, and connect
    assets_folder = client_app.config.get("assets_folder", "assets")
    edit_icon = pygame.image.load(os.path.join(assets_folder, "notepad_icon.png"))
    edit_icon = pygame.transform.scale(edit_icon, (30, 30))
    delete_icon = pygame.image.load(os.path.join(assets_folder, "trash_can_icon.png"))
    delete_icon = pygame.transform.scale(delete_icon, (30, 30))
    connect_icon = pygame.image.load(os.path.join(assets_folder, "connect_icon.png"))
    connect_icon = pygame.transform.scale(connect_icon, (30, 30))

    ping_results = {server["name"]: "..." for server in servers}

    def update_ping():
        """Update the ping for all servers every 60 seconds."""
        while True:
            for server in servers:
                motd = ping_server(server["address"], server["port"])
                ping_results[server["name"]] = motd if motd else "Offline"
            time.sleep(60)

    threading.Thread(target=update_ping, daemon=True).start()

    last_button_press_time = 0

    while True:
        # Draw the splash screen
        draw_splash_screen(screen, client_app)

        # Title
        title = font.render("Join a Server", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        # Back Button
        back_button_rect = pygame.Rect(50, 100, 150, 50)
        draw_button(screen, back_button_rect, "Back", font)

        # Add Server Button
        add_server_button_rect = pygame.Rect(screen.get_width() - 200, 100, 150, 50)
        draw_button(screen, add_server_button_rect, "Add Server", font)

        # Draw the transparent background for the server list
        server_list_background = pygame.Surface((screen.get_width() - 100, screen.get_height() - 400), pygame.SRCALPHA)
        server_list_background.fill((50, 50, 50, 150))
        screen.blit(server_list_background, (50, 350))

        # List saved servers
        y_offset = 360
        for server in servers:
            edit_button_rect = pygame.Rect(60, y_offset, 30, 30)
            screen.blit(edit_icon, edit_button_rect)

            delete_button_rect = pygame.Rect(95, y_offset, 30, 30)
            screen.blit(delete_icon, delete_button_rect)

            connect_button_rect = pygame.Rect(130, y_offset, 30, 30)
            screen.blit(connect_icon, connect_button_rect)

            server_label = font.render(server["name"], True, (255, 255, 255))
            screen.blit(server_label, (200, y_offset))

            ping_label = font.render(ping_results.get(server["name"], "..."), True, (255, 255, 255))
            screen.blit(ping_label, (500, y_offset))

            if pygame.mouse.get_pressed()[0]:
                current_time = time.time()
                if current_time - last_button_press_time >= 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if edit_button_rect.collidepoint(mouse_pos):
                        # Open the edit server screen
                        display_edit_server_screen(screen, client_app, server["name"], server)
                        servers = server_manager.get_all_servers()  # Reload the server list after editing
                        last_button_press_time = current_time
                        break
                    if delete_button_rect.collidepoint(mouse_pos):
                        # Delete the server
                        server_manager.delete_server(server["name"])
                        servers = server_manager.get_all_servers()  # Reload the server list
                        ping_results.pop(server["name"], None)  # Remove the ping result
                        last_button_press_time = current_time
                        break
                    if connect_button_rect.collidepoint(mouse_pos):
                        print(f"Connecting to {server['name']} at {server['address']}:{server['port']}")
                        if connect_to_server(client_app, screen, server["address"], server["port"]):
                            game_gui_loop(screen, client_app)
                            last_button_press_time = current_time
                            return

            y_offset += 35

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_time = time.time()
                if current_time - last_button_press_time >= 1:
                    if back_button_rect.collidepoint(event.pos):
                        main_menu_screen(screen, client_app)
                        last_button_press_time = current_time
                        return
                    if add_server_button_rect.collidepoint(event.pos):
                        display_add_server_screen(screen, client_app)
                        servers = server_manager.get_all_servers()
                        last_button_press_time = current_time
                        break

        pygame.display.flip()


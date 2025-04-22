import os
import threading
import time
import pygame
from pygame.locals import *
from utils.server_manager import ServerManager
from utils.config_man import load_config  # Import the configuration loader
from utils.gui_utils import draw_button  # Import the shared function
from utils.gui_game import game_gui_loop  # Import the game GUI loop
from utils.event.connect_to_server import connect_to_server
from utils.event.ping_server import ping_server
from utils.gui_edit_server import display_edit_server_screen  # Import the edit server screen
from utils.gui_add_server import display_add_server_screen  # Import the add server screen

# Load configuration
config = load_config(os.path.join(os.path.dirname(__file__), "../config.json"))
assets_folder = config.get("assets_folder", "assets")  # Dynamically load assets folder from config

def display_join_server_screen(screen, splash_image_path, client_app, main_menu_screen):
    """Display the join server screen."""
    font = pygame.font.Font(None, 36)
    server_manager = ServerManager()  # Create an instance of ServerManager
    servers = server_manager.get_all_servers()  # Retrieve the list of servers

    # Load the splash screen image
    splash_image = pygame.image.load(splash_image_path)
    splash_image = pygame.transform.scale(splash_image, (screen.get_width(), screen.get_height()))

    # Load icons for edit, delete, and connect
    edit_icon = pygame.image.load(os.path.join(assets_folder, "notepad_icon.png"))
    edit_icon = pygame.transform.scale(edit_icon, (30, 30))  # Resize the icon
    delete_icon = pygame.image.load(os.path.join(assets_folder, "trash_can_icon.png"))
    delete_icon = pygame.transform.scale(delete_icon, (30, 30))  # Resize the icon
    connect_icon = pygame.image.load(os.path.join(assets_folder, "connect_icon.png"))
    connect_icon = pygame.transform.scale(connect_icon, (30, 30))  # Resize the icon

    # Initialize ping results
    ping_results = {server["name"]: "..." for server in servers}

    def update_ping():
        """Update the ping for all servers every 60 seconds."""
        while True:
            for server in servers:
                motd = ping_server(client_app)
                if motd:
                    ping_results[server["name"]] = motd
                else:
                    ping_results[server["name"]] = "Offline"
            time.sleep(60)

    # Start the ping update thread
    threading.Thread(target=update_ping, daemon=True).start()

    while True:
        # Draw the splash screen as the background
        screen.blit(splash_image, (0, 0))

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

        # List saved servers with edit, delete, connect, name, and ping
        y_offset = 360
        for server in servers:
            # Edit button (icon)
            edit_button_rect = pygame.Rect(60, y_offset, 30, 30)
            screen.blit(edit_icon, edit_button_rect)

            # Delete button (icon)
            delete_button_rect = pygame.Rect(95, y_offset, 30, 30)  # 5px padding
            screen.blit(delete_icon, delete_button_rect)

            # Connect button (icon)
            connect_button_rect = pygame.Rect(130, y_offset, 30, 30)  # 5px padding
            screen.blit(connect_icon, connect_button_rect)

            # Server name
            server_label = font.render(server["name"], True, (255, 255, 255))
            screen.blit(server_label, (200, y_offset))

            # Ping result
            ping_label = font.render(ping_results.get(server["name"], "..."), True, (255, 255, 255))
            screen.blit(ping_label, (500, y_offset))

            # Check for button clicks
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if edit_button_rect.collidepoint(mouse_pos):
                    # Open the edit server screen
                    display_edit_server_screen(screen, splash_image_path, server_manager, server["name"], server)
                    servers = server_manager.get_all_servers()  # Reload the server list after editing
                    break
                if delete_button_rect.collidepoint(mouse_pos):
                    print(f"Deleting server: {server['name']}")
                    server_manager.delete_server(server["name"])
                    servers = server_manager.get_all_servers()  # Reload the server list
                    ping_results.pop(server["name"], None)  # Remove the ping result
                    break
                if connect_button_rect.collidepoint(mouse_pos):
                    print(f"Connecting to {server['name']} at {server['address']}:{server['port']}")
                    client_app.server_address = server["address"]
                    client_app.udp_handler.udp_port = server["port"]
                    if connect_to_server(client_app, client_app.client_uuid):
                        print("Connection successful. Loading game GUI...")
                        game_gui_loop(screen, client_app, main_menu_screen)  # Pass main_menu_screen
                        return  # Exit the join server screen

            y_offset += 35  # Adjust spacing between rows

        # Event handling
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                # Check if Back button is clicked
                if back_button_rect.collidepoint(event.pos):
                    return  # Return to the loading screen

                # Check if Add Server button is clicked
                if add_server_button_rect.collidepoint(event.pos):
                    # Open the Add Server screen
                    display_add_server_screen(screen, splash_image_path, server_manager)
                    servers = server_manager.get_all_servers()  # Reload the server list after adding
                    break

        pygame.display.flip()


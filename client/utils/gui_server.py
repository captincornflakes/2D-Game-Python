import os
import threading
import time
import pygame
from pygame.locals import *
from utils.server_manager import ServerManager
from utils.connection_handler import Client
from utils.config_man import load_config  # Import the configuration loader
from utils.gui_utils import draw_button  # Import the shared function
from utils.gui_game import game_gui_loop  # Import the game GUI loop
from utils.event.connect_to_server import connect_to_server
from utils.event.ping_server import ping_server
from utils.tcp_handler import TCPHandler
from utils.udp_handler import UDPHandler

# Load configuration
config = load_config(os.path.join(os.path.dirname(__file__), "../config.json"))
assets_folder = config.get("assets_folder", "assets")  # Dynamically load assets folder from config

def display_join_server_screen(screen, splash_image_path, client_app):
    """Display the join server screen."""
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 28)
    server_manager = ServerManager()  # Create an instance of ServerManager
    servers = server_manager.get_all_servers()  # Call the method on the instance
    server_manager.print_all_servers()

    # Load configuration dynamically
    config_path = os.path.join(os.path.dirname(__file__), "../config.json")
    config = load_config(config_path)

    # Initialize ping results
    ping_results = {server["name"]: "..." for server in servers}

    # Allow the window to be resizable
    pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)

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

    # Track button states
    button_disabled = {"delete": False, "connect": False}

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
        # Handle resizing
        screen_width, screen_height = screen.get_size()
        splash_image = pygame.transform.scale(splash_image, (screen_width, screen_height))

        # Draw the splash screen as the background
        screen.blit(splash_image, (0, 0))

        # Title
        title = font.render("Join a Server", True, (255, 255, 255))
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

        # Back Button
        back_button_rect = pygame.Rect(50, 100, 150, 50)
        draw_button(screen, back_button_rect, "Back", font)

        # Add Server Button
        add_server_button_rect = pygame.Rect(screen_width - 200, 100, 150, 50)
        draw_button(screen, add_server_button_rect, "Add Server", font)

        # Draw the transparent background for the server list
        server_list_background = pygame.Surface((screen_width - 100, screen_height - 400), pygame.SRCALPHA)
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
                if delete_button_rect.collidepoint(mouse_pos) and not button_disabled["delete"]:
                    # Disable the delete button
                    button_disabled["delete"] = True
                    print(f"Deleting server: {server['name']}")
                    server_manager.delete_server(server["name"])
                    servers = server_manager.get_all_servers()  # Reload the server list
                    ping_results.pop(server["name"], None)  # Remove the ping result
                    button_disabled["delete"] = False  # Re-enable the delete button
                    break
                if connect_button_rect.collidepoint(mouse_pos) and not button_disabled["connect"]:
                    # Disable the connect button
                    button_disabled["connect"] = True
                    print(f"Connecting to {server['name']} at {server['address']}:{server['port']}")

                    # Set the server address and port in the connection handler
                    client_app.server_address = server["address"]
                    client_app.udp_handler.udp_port = server["port"]

                    # Call connect_to_server from connection_handler
                    if connect_to_server(client_app, client_app.client_uuid):
                        print("Connection successful. Loading game GUI...")
                        game_gui_loop(screen, client_app)  # Pass client_app as the client argument
                        return  # Exit the join server screen

                    # Re-enable the connect button if connection fails
                    button_disabled["connect"] = False

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
                    display_edit_server_screen(screen, splash_image_path, server_manager, "", {"address": "", "port": 85})
                    servers = server_manager.get_all_servers()  # Reload the server list after adding
                    break

        pygame.display.flip()


def display_edit_server_screen(screen, splash_image_path, server_manager, server_name, server_info):
    """Display the 'Edit Server' screen."""
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 28)

    # Input fields for editing the server
    input_active = {"name": False, "address": False, "port": False}
    input_text = {
        "name": server_name,
        "address": server_info["address"],
        "port": str(server_info["port"]),
    }
    input_boxes = {
        "name": pygame.Rect(300, 200, 200, 40),
        "address": pygame.Rect(300, 250, 200, 40),
        "port": pygame.Rect(300, 300, 200, 40),
    }

    while True:
        # Draw the splash screen as the background
        splash_image = pygame.image.load(splash_image_path)
        splash_image = pygame.transform.scale(splash_image, (screen.get_width(), screen.get_height()))
        screen.blit(splash_image, (0, 0))

        # Title
        title = font.render("Edit Server", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        # Input fields for editing the server
        for key, rect in input_boxes.items():
            # Draw input box background
            pygame.draw.rect(screen, (200, 200, 200), rect)  # Gray background
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # White border
            # Draw label with white background and black text
            label_rect = pygame.Rect(rect.x - 120, rect.y, 100, rect.height)
            pygame.draw.rect(screen, (255, 255, 255), label_rect)  # White background
            pygame.draw.rect(screen, (0, 0, 0), label_rect, 2)  # Black border
            label = input_font.render(f"{key.capitalize()}:", True, (0, 0, 0))  # Black text
            screen.blit(label, (label_rect.x + 5, label_rect.y + 5))
            # Draw input text
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
                # Check if input boxes are clicked
                for key, rect in input_boxes.items():
                    if rect.collidepoint(event.pos):
                        input_active = {k: False for k in input_active}  # Deactivate all
                        input_active[key] = True
                    else:
                        input_active[key] = False

                # Check if Save button is clicked
                if save_button_rect.collidepoint(event.pos):
                    if input_text["name"] and input_text["address"] and input_text["port"].isdigit():
                        server_manager.update_server(server_name, input_text["name"], input_text["address"], int(input_text["port"]))
                        return  # Return to the previous screen

                # Check if Back button is clicked
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


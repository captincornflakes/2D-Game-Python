import json
import os
import time
from threading import Thread

KEEPALIVE_TIMEOUT = 5  # Timeout in seconds to consider a player offline

def handle_keepalive(addr, message, clients, player_file_path):
    """Handle a keepalive message from a UDP client."""
    print(f"Received keepalive from {addr}: {message}")

    # Load existing player data from player.json
    if os.path.exists(player_file_path):
        with open(player_file_path, "r") as file:
            player_data = json.load(file)
    else:
        print("Player file not found. Cannot process keepalive.")
        return

    # Check if the client is registered
    if addr not in clients:
        print(f"Unregistered client {addr} sent keepalive. Ignoring.")
        return

    client_uuid = clients[addr]["uuid"]

    # Update the player's online status and last keepalive time
    if client_uuid in player_data:
        player_data[client_uuid]["online"] = True
        player_data[client_uuid]["last_keepalive"] = time.time()

        # Save the updated player data back to player.json
        with open(player_file_path, "w") as file:
            json.dump(player_data, file, indent=4)

        print(f"Updated keepalive for player {player_data[client_uuid]['username']} (UUID: {client_uuid})")

        # Send a response back to the client confirming the keepalive
        keepalive_response = {
            "action": "keepalive_ack",
            "message": "Keepalive received. Server is running."
        }
        udp_socket = clients.get("udp_socket")
        if udp_socket:
            udp_socket.sendto(json.dumps(keepalive_response).encode('utf-8'), addr)
            print(f"Sent keepalive acknowledgment to {addr}")
    else:
        print(f"Player with UUID {client_uuid} not found in player.json.")

def monitor_keepalive(clients, player_file_path):
    """Monitor keepalive messages and mark players offline if timeout occurs."""
    while True:
        time.sleep(1)  # Check every second

        # Load existing player data from player.json
        if os.path.exists(player_file_path):
            with open(player_file_path, "r") as file:
                player_data = json.load(file)
        else:
            continue

        # Check for players who have timed out
        current_time = time.time()
        for client_uuid, player_info in player_data.items():
            last_keepalive = player_info.get("last_keepalive", 0)
            if player_info.get("online", False) and current_time - last_keepalive > KEEPALIVE_TIMEOUT:
                print(f"Player {player_info['username']} (UUID: {client_uuid}) timed out. Marking as offline.")
                player_info["online"] = False

                # Remove the client from the clients dictionary
                addr_to_remove = None
                for addr, client in clients.items():
                    if client["uuid"] == client_uuid:
                        addr_to_remove = addr
                        break
                if addr_to_remove:
                    # Send a disconnect message to the client
                    disconnect_message = {
                        "action": "disconnect",
                        "reason": "Keepalive timeout. You have been disconnected from the server."
                    }
                    udp_socket = clients.get("udp_socket")
                    if udp_socket:
                        udp_socket.sendto(json.dumps(disconnect_message).encode('utf-8'), addr_to_remove)
                        print(f"Sent disconnect message to {addr_to_remove}")

                    del clients[addr_to_remove]
                    print(f"Closed UDP connection for {addr_to_remove}")

        # Save the updated player data back to player.json
        with open(player_file_path, "w") as file:
            json.dump(player_data, file, indent=4)
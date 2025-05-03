import time
import threading

def start_keepalive(client):
    def keepalive_loop():
        while client.connected:
            try:
                # Send a keepalive message to the server with the client's UUID
                keepalive_message = {
                    "action": "keepalive",
                    "uuid": client.uuid  # Include the client's UUID
                }
                client.udp_handler.send_message(keepalive_message)
                print(f"Keepalive message sent to the server with UUID: {client.uuid}")

                # Wait for the server's response
                response = client.udp_handler.receive_message()
                if response and response.get("action") == "keepalive_ack":
                    print(f"Server response: {response.get('message', 'No message received')}")
                    print(f"Server acknowledged UUID: {response.get('uuid')}, Player Name: {response.get('player_name')}")
                else:
                    print("Unexpected or no response from server for keepalive.")
            except Exception as e:
                print(f"Failed to send or receive keepalive message: {e}")
                client.connected = False
                break
            time.sleep(2)  # Wait for 2 seconds before sending the next keepalive

    # Start the keepalive loop in a separate thread
    threading.Thread(target=keepalive_loop, daemon=True).start()
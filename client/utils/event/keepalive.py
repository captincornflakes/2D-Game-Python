import time
import threading

def start_keepalive(client):
    def keepalive_loop():
        while client.connected:
            try:
                # Send a keepalive message to the server
                keepalive_message = {"action": "keepalive"}
                client.udp_handler.send_message(keepalive_message)
                print("Keepalive message sent to the server.")

                # Wait for the server's response
                response = client.udp_handler.receive_message()
                if response and response.get("action") == "keepalive_ack":
                    print(f"Server response: {response.get('message', 'No message received')}")
                else:
                    print("Unexpected or no response from server for keepalive.")
            except Exception as e:
                print(f"Failed to send or receive keepalive message: {e}")
                client.connected = False
                break
            time.sleep(2)  # Wait for 2 seconds before sending the next keepalive

    # Start the keepalive loop in a separate thread
    threading.Thread(target=keepalive_loop, daemon=True).start()
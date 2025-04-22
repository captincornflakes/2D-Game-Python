import time
import threading

def start_keepalive(client):
    """
    Start sending keepalive messages to the server every 3 seconds.
    If the client is disconnected, stop sending keepalive messages.
    """
    def keepalive_loop():
        while client.connected:
            try:
                # Send a keepalive message to the server
                keepalive_message = {"action": "keepalive"}
                client.udp_handler.send_message(keepalive_message)
                print("Keepalive message sent to the server.")
            except Exception as e:
                print(f"Failed to send keepalive message: {e}")
                client.connected = False
                break
            time.sleep(2)  # Wait for 3 seconds before sending the next keepalive

    # Start the keepalive loop in a separate thread
    threading.Thread(target=keepalive_loop, daemon=True).start()
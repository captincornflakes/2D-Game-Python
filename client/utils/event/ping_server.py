def ping_server(client, timeout=2):
    """Ping the server to check if it is reachable and retrieve the MOTD."""
    try:
        client.tcp_handler.connect()
        ping_request = {"action": "ping"}
        client.tcp_handler.send_message(ping_request)

        response = client.tcp_handler.receive_message()
        if response and response.get("action") == "pong" and "motd" in response:
            return response["motd"]
        else:
            print(f"Unexpected response: {response}")
            return None
    except Exception as e:
        print(f"Failed to ping server: {e}")
        return None
    finally:
        client.tcp_handler.disconnect()
def request_entities(client, callback=None):
    """Request entity data from the server."""
    try:
        # Send a request for entities to the server
        entity_request = {"type": "request_entities"}
        client.udp_handler.send_message(entity_request)
        print("Entity request sent to the server.")

        # Wait for the server's response
        response = client.udp_handler.receive_message()
        if response and response.get("type") == "entity_data":
            print(f"Entity data received: {response}")
            if callback:
                callback(response)  # Pass the response to the callback function
        else:
            print("Invalid or no response received for entity request.")
    except Exception as e:
        print(f"Error requesting entities: {e}")
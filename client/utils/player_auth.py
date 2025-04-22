class PlayerAuth:
    def __init__(self, connection_handler):
        self.connection_handler = connection_handler

    def authenticate_player(self, username):
        auth_message = {
            "action": "authenticate",
            "username": username
        }

        # Send the authentication message to the server
        self.connection_handler.send_message(auth_message)

        # Wait for the server's response
        response = self.connection_handler.receive_message()

        if response and response.get("action") == "authenticated":
            print(f"Player authenticated: {response}")
            return response
        else:
            print("Failed to authenticate player.")
            return None
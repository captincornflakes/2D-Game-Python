import uuid
import os
import json
import requests  # Import requests for API calls

class PlayerAuth:
    def __init__(self, world_folder):
        self.players_file = os.path.join(world_folder, "players.json")
        self.players = self.load_players()

    def load_players(self):
        """Load players from the players.json file."""
        if os.path.exists(self.players_file):
            with open(self.players_file, 'r') as f:
                return json.load(f)
        return {}

    def save_players(self):
        """Save players to the players.json file."""
        with open(self.players_file, 'w') as f:
            json.dump(self.players, f, indent=4)

    def player_exists(self, uuid):
        """Check if a player exists by their UUID."""
        return uuid in self.players

    def get_player(self, uuid):
        """Get player data by UUID."""
        return self.players.get(uuid)

    def add_player(self, uuid, player_data):
        """Add a new player."""
        self.players[uuid] = player_data
        self.save_players()

    def check_player_api(self, player_name):
        """Check the external API for the player's UUID."""
        try:
            response = requests.get(f"https://echodebates.com/auth/api.php", params={"player": player_name})
            if response.status_code == 200:
                data = response.json()
                if "uuid" in data:
                    return data["uuid"]
                else:
                    print(f"API response does not contain a UUID: {data}")
            else:
                print(f"Failed to fetch data from API. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error connecting to the API: {e}")
        return None
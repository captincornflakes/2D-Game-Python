import json
import os

class CommandHandler:
    def __init__(self, world_folder, player_auth):
        self.world_folder = world_folder
        self.player_auth = player_auth
        self.ops_file = os.path.join(world_folder, "ops.json")
        self.load_operators()

    def load_operators(self):
        """Load operators from the ops.json file."""
        if os.path.exists(self.ops_file):
            try:
                with open(self.ops_file, 'r') as f:
                    self.operators = json.load(f).get("operators", [])
            except json.JSONDecodeError:
                print(f"Error: {self.ops_file} contains invalid JSON. Starting with an empty operator list.")
                self.operators = []
        else:
            self.operators = []

    def is_operator(self, player_name):
        """Check if a player is an operator."""
        for operator in self.operators:
            if operator["name"] == player_name:
                return True
        return False

    def op_player(self, player_name):
        """Grant operator permissions to a player."""
        if not self.is_operator(player_name):
            self.operators.append({"name": player_name, "permissions": ["all"]})
            self.save_operators()
            print(f"Player {player_name} is now an operator.")
        else:
            print(f"Player {player_name} is already an operator.")

    def kick_player(self, player_name):
        """Kick a player from the server."""
        player_id = self.get_player_id_by_name(player_name)
        if player_id:
            self.player_auth.remove_player(player_id)
            print(f"Player {player_name} has been kicked from the server.")
        else:
            print(f"Player {player_name} not found.")

    def change_player_name(self, old_name, new_name):
        """Change a player's name."""
        player_id = self.get_player_id_by_name(old_name)
        if player_id:
            self.player_auth.players[player_id]["name"] = new_name
            self.player_auth.save_players()
            print(f"Player name changed from {old_name} to {new_name}.")
        else:
            print(f"Player {old_name} not found.")

    def get_player_id_by_name(self, player_name):
        """Retrieve a player's UUID by their name."""
        for player_id, player_data in self.player_auth.players.items():
            if player_data.get("name") == player_name:
                return player_id
        return None

    def save_operators(self):
        """Save the operators to the ops.json file."""
        with open(self.ops_file, 'w') as f:
            json.dump({"operators": self.operators}, f, indent=4)

    def handle_command(self, command, args):
        """Handle a console command."""
        if command == "/op" and len(args) == 1:
            self.op_player(args[0])
        elif command == "/kick" and len(args) == 1:
            self.kick_player(args[0])
        elif command == "/name" and len(args) == 2:
            self.change_player_name(args[0], args[1])
        elif command in ["/tpa", "/tph"]:
            print(f"Command {command} is not yet implemented.")
        else:
            print(f"Unknown command: {command}")

def handle_console_command(command_handler, command_input):
    """Handle console commands."""
    parts = command_input.strip().split()
    if not parts:
        print("No command entered.")
        return

    command = parts[0]
    args = parts[1:]
    command_handler.handle_command(command, args)
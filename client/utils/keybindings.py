import json
import os

class Keybinds:
    def __init__(self):
        # Define the default path to the keybindings.json file
        self.filepath = os.path.join(os.path.dirname(__file__), "../keybindings.json")
        self.keybinds = self._load_keybinds()

    def _load_keybinds(self):
        """Load keybindings from the JSON file."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Keybindings file not found: {self.filepath}")
        with open(self.filepath, "r") as file:
            return json.load(file)

    def get_keybind(self, action):
        """Get the keybind for a specific action."""
        return self.keybinds.get(action, None)

    def update_keybind(self, action, new_key):
        """Update the keybind for a specific action."""
        if action not in self.keybinds:
            raise KeyError(f"Action '{action}' does not exist in keybindings.")
        self.keybinds[action] = new_key
        self._save_keybinds()

    def _save_keybinds(self):
        """Save the updated keybindings back to the JSON file."""
        with open(self.filepath, "w") as file:
            json.dump(self.keybinds, file, indent=4)

# Example usage
if __name__ == "__main__":
    keybinds = Keybinds()

    # Get a keybind
    print("Key for moving up:", keybinds.get_keybind("up"))

    # Update a keybind
    keybinds.update_keybind("up", "ArrowUp")
    print("Updated key for moving up:", keybinds.get_keybind("up"))

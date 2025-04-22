import os
import json

class ServerManager:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "..\\servers.json")  # Path to servers.json
        print(f"Loading servers from: {self.file_path}")  # Debug: Print the file path
        self.servers = {}  # Dictionary to store server information
        self.load_servers()  # Load servers from the file during initialization

    def load_servers(self):
        """Load server information from the servers.json file."""
        if os.path.exists(self.file_path):
            print(f"Found servers.json at: {self.file_path}")  # Debug: File found
            try:
                with open(self.file_path, 'r') as f:
                    self.servers = json.load(f)  # Load servers into the dictionary
                    print(f"Loaded servers: {self.servers}")  # Debug: Print loaded servers
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")  # Debug: JSON error
                self.servers = {}
        else:
            print(f"servers.json not found at: {self.file_path}")  # Debug: File not found
            self.servers = {}  # Initialize with an empty dictionary if the file doesn't exist

    def save_servers(self):
        """Save server information to the servers.json file."""
        with open(self.file_path, 'w') as f:
            json.dump(self.servers, f, indent=4)

    def get_all_servers(self):
        """Return a list of all servers."""
        return [{"name": name, "address": info["address"], "port": info["port"]} for name, info in self.servers.items()]

    def get_server(self, name):
        """Return a specific server by name."""
        if name in self.servers:
            return self.servers[name]
        raise ValueError(f"Server with name '{name}' not found.")

    def add_server(self, name, address, port):
        """Add a new server to the list."""
        self.servers[name] = {
            "address": address,
            "port": port
        }
        self.save_servers()

    def delete_server(self, name):
        """Delete a server from the list."""
        if name in self.servers:
            del self.servers[name]
            self.save_servers()
            print(f"Server '{name}' deleted successfully.")
        else:
            print(f"Server '{name}' not found.")

    def update_server(self, old_name, new_name, address, port):
        """Update an existing server's information."""
        if old_name in self.servers:
            # Remove the old server entry if the name is being changed
            if old_name != new_name:
                del self.servers[old_name]

            # Add or update the server with the new information
            self.servers[new_name] = {
                "address": address,
                "port": port
            }
            self.save_servers()
            print(f"Server '{old_name}' updated successfully to '{new_name}'.")
        else:
            print(f"Server '{old_name}' not found.")

    def select_server(self):
        """Allow the user to select or add a server."""
        print("Available Servers:")
        for i, (name, info) in enumerate(self.servers.items(), start=1):
            print(f"{i}. {name} - {info['address']}:{info['port']}")

        choice = input("Select a server by number or type 'add' to add a new server: ")
        if choice.lower() == "add":
            name = input("Enter server name: ")
            address = input("Enter server address: ")
            port = int(input("Enter server port: "))
            self.add_server(name, address, port)
            print("Server added!")
        else:
            try:
                index = int(choice) - 1
                selected_server = list(self.servers.items())[index]
                name, info = selected_server
                print(f"Selected Server: {name} - {info['address']}:{info['port']}")
                return info["address"], info["port"]
            except (ValueError, IndexError):
                print("Invalid selection.")
                return None, None

    def print_all_servers(self):
        """Print all servers to the console."""
        servers = self.get_all_servers()
        if servers:
            print("Available Servers:")
            for server in servers:
                print(f"Name: {server['name']}, Address: {server['address']}, Port: {server['port']}")
        else:
            print("No servers available.")
            
            
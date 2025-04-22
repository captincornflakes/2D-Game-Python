# 2D Multiplayer Game Server

## Overview
This project is a 2D multiplayer game server designed for an open-world shared survival game. It supports client connections over TCP and UDP, managing various aspects of the game, including player data, world state, and server-client communication.

## Features
- **Player Management**: Tracks player inventory, health, stamina, and hunger.
- **World Generation**: Dynamically generates a grid-based world with chunks, starting with an initial layout of 4 connected chunks.
- **Game Loop**: Manages the game state and updates based on player actions and game time.
- **Networking**: Supports both TCP and UDP for client-server communication.
- **Command System**: Includes server-side commands for managing players and the game world.
- **Configuration**: Fully customizable server settings via `config.json`.

## Project Structure
```
2D-Game-Python
├── server
│   ├── __init__.py
│   ├── server.py
│   ├── world
│   │   ├── __init__.py
│   │   ├── chunk.py
│   │   ├── generator.py
│   │   └── tiles.json
│   ├── player
│   │   ├── __init__.py
│   │   ├── inventory.py
│   │   └── stats.py
│   └── utils
│       ├── __init__.py
│       ├── helpers.py
│       ├── worldgen.py
│       ├── connection_handler.py
│       ├── event
│       │   ├── handle_connect.py
│       │   ├── handle_move.py
│       │   ├── handle_ping.py
│       │   └── handle_tile_update.py
│       └── ...
├── client
│   ├── client.py
│   ├── utils
│   │   ├── gui_main.py
│   │   ├── gui_game.py
│   │   ├── gui_server.py
│   │   ├── gui_settings.py
│   │   └── ...
│   ├── assets
│   │   ├── default
│   │   │   └── tiles.json
│   │   └── remake
│   │       └── tiles.json
│   └── config.json
├── requirements.txt
├── config.json
├── LICENSE
└── README.md
```

## Setup Instructions

### Server Setup
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-repo/2D-Game-Python.git
   ```
2. Navigate to the `server` directory:
   ```bash
   cd 2D-Game-Python/server
   ```
3. Install the required dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
4. Configure the server settings in `config.json` as needed.
5. Run the server:
   ```bash
   python server.py
   ```

### Client Setup
1. Navigate to the `client` directory:
   ```bash
   cd 2D-Game-Python/client
   ```
2. Install the required dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
3. Configure the client settings in `config.json` as needed.
4. Run the client:
   ```bash
   python client.py
   ```

## Usage
- **Server**: The server listens for client connections on the configured TCP and UDP ports (default: `23546`).
- **Client**: Players can connect to the server, interact with the world, manage their inventory, and track their stats.
- **Commands**: Use server-side commands (e.g., `/op`, `/kick`) to manage players and the game world.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the GNU General Public License v3. See the [LICENSE](LICENSE) file for details.

## Future Enhancements
- Add more tile types and world features.
- Implement advanced player interactions (e.g., trading, combat).
- Improve the GUI for both client and server management.
- Add support for persistent world saving and loading.

## Contact
For questions or support, please open an issue on the GitHub repository.
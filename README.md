# 2D Multiplayer Game Server

## Overview
This project is a 2D multiplayer game server designed for an open-world shared survival game. It supports client connections over UDP and manages various aspects of the game, including player data and world state.

## Features
- **Player Management**: Tracks player inventory, health, stamina, and hunger.
- **World Generation**: Creates a grid-based world with chunks, starting with an initial layout of 4 connected chunks.
- **Game Loop**: Manages the game state and updates based on player actions and game time.
- **UDP Connection**: Operates on localhost port 85 for client-server communication.

## Project Structure
```
2d-multiplayer-game-server
├── server
│   ├── __init__.py
│   ├── server.py
│   ├── world
│   │   ├── __init__.py
│   │   ├── chunk.py
│   │   └── generator.py
│   ├── player
│   │   ├── __init__.py
│   │   ├── inventory.py
│   │   └── stats.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── tests
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_world.py
│   └── test_player.py
├── requirements.txt
├── config.json
└── README.md
```

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies listed in `requirements.txt`.
4. Configure the server settings in `config.json` as needed.
5. Run the server using `python server/server.py`.

## Usage
- Connect clients to the server using UDP on localhost port 85.
- Players can interact with the world, manage their inventory, and track their stats.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
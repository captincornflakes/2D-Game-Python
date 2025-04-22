import os
import json

class TileHandler:
    def __init__(self, tile_data_file=None):
        # Dynamically determine the path to tiles.json
        if tile_data_file is None:
            tile_data_file = os.path.join(os.path.dirname(__file__), 'tiles.json')
        self.tiles = {}
        self.load_tiles(tile_data_file)

    def load_tiles(self, tile_data_file):
        if not os.path.exists(tile_data_file):
            raise FileNotFoundError(f"Error: {tile_data_file} not found. Ensure the file exists.")
        try:
            with open(tile_data_file, 'r') as f:
                self.tiles = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Error: {tile_data_file} contains invalid JSON.")

    def get_tile(self, tile_id):
        return self.tiles.get(tile_id, None)


class WorldGenerator:
    def __init__(self, chunk_size=32, tile_handler=None):
        self.chunk_size = chunk_size
        self.world = {}
        self.tile_handler = tile_handler or TileHandler()

    def generate_initial_world(self, initial_chunks):
        # Generate a grid of chunks centered around (0, 0)
        half_chunks = initial_chunks // 2
        for x in range(-half_chunks, half_chunks):
            for y in range(-half_chunks, half_chunks):
                self.world[(x, y)] = self.create_chunk(x, y)
        return self.world

    def create_chunk(self, x, y):
            print(f"Creating chunk at ({x}, {y})")  # Debugging output
            # Generate chunk data
            chunk_data = {
                "tiles": [
                    {"location": {"x": i, "y": j}, "type": "grass"}
                    for i in range(self.chunk_size)
                    for j in range(self.chunk_size)
                ]
            }
            return chunk_data

    def save_world(self, file_path):
        # Convert tuple keys to strings
        serializable_world = {f"{key[0]},{key[1]}": value for key, value in self.world.items()}
        with open(file_path, 'w') as f:
            json.dump(serializable_world, f)

    def load_world(self, file_path):
        with open(file_path, 'r') as f:
            serializable_world = json.load(f)
        # Convert string keys back to tuples
        self.world = {tuple(map(int, key.split(','))): value for key, value in serializable_world.items()}
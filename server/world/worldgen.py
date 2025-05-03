import os
import json

class WorldGenerator:
    def __init__(self, world_folder, initial_chunks=10):
        """
        Initialize the WorldGenerator with the world folder and number of initial chunks.
        """
        self.world_folder = world_folder  # Use the provided world folder
        self.initial_chunks = initial_chunks  # Default to 10 chunks if not specified

    def generate_chunk(self, chunk_x, chunk_y):
        """
        Generate a single chunk and save it to the chunks folder inside the world folder.
        """
        chunks_folder = os.path.join(self.world_folder, "chunks")
        if not os.path.exists(chunks_folder):
            print(f"Chunks folder not found at {chunks_folder}. Creating it...")
            os.makedirs(chunks_folder)

        # Generate the chunk data
        chunk_data = {
            "chunk_x": chunk_x,
            "chunk_y": chunk_y,
            "tiles": [[0 for _ in range(16)] for _ in range(16)]  # Example: 16x16 grid of tiles
        }
        chunk_file = os.path.join(chunks_folder, f"{chunk_x}x{chunk_y}.json")
        with open(chunk_file, 'w') as f:
            json.dump(chunk_data, f)
        print(f"Generated chunk ({chunk_x}, {chunk_y}) at {chunk_file}.")

    def generate_initial_chunks(self):
        """
        Generate the initial chunks and save them to the chunks folder inside the world folder.
        """
        chunks_folder = os.path.join(self.world_folder, "chunks")
        if not os.path.exists(chunks_folder):
            print(f"Creating chunks folder at {chunks_folder}...")
            os.makedirs(chunks_folder)

        # Generate the specified number of initial chunks
        for x in range(self.initial_chunks):
            for y in range(self.initial_chunks):
                self.generate_chunk(x, y)

        print(f"Initial world generation complete with {self.initial_chunks}x{self.initial_chunks} chunks.")

    def generate_initial_world(self):
        """
        Generate the initial world by calling the generate_initial_chunks function.
        """
        print("Generating initial world...")
        self.generate_initial_chunks()
import os
import json

def generate_chunk(x, y, world_folder, world_generator):
    """Generate a single chunk and save it to the world folder."""
    chunks_folder = os.path.join(world_folder, "chunks")
    if not os.path.exists(chunks_folder):
        os.makedirs(chunks_folder)

    print(f"Generating chunk ({x}, {y})")  # Debugging output
    chunk_data = world_generator.create_chunk(x, y)
    chunk_file = os.path.join(chunks_folder, f"{x}x{y}.json")
    with open(chunk_file, 'w') as f:
        json.dump(chunk_data, f)
    print(f"Chunk ({x}, {y}) saved to {chunk_file}")

def generate_initial_world(initial_chunks, world_folder, world_generator):
    """Generate the initial chunks for the world."""
    for chunk in initial_chunks:
        x, y = chunk["x"], chunk["y"]
        generate_chunk(x, y, world_folder, world_generator)  # Call the generate_chunk function
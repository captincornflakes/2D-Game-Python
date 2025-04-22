import os
import json

def generate_initial_world(initial_chunks, world_folder, world_generator):
    chunks_folder = os.path.join(world_folder, "chunks")
    if not os.path.exists(chunks_folder):
        os.makedirs(chunks_folder)

    for chunk in initial_chunks:
        x, y = chunk["x"], chunk["y"]
        print(f"Generating chunk ({x}, {y})")  # Debugging output
        chunk_data = world_generator.create_chunk(x, y)
        chunk_file = os.path.join(chunks_folder, f"{x}x{y}.json")
        with open(chunk_file, 'w') as f:
            json.dump(chunk_data, f)
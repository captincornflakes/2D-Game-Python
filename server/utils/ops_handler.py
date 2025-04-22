import os
import json

OPS_FILE = os.path.join(os.path.dirname(__file__), "..", "ops.json")  # Path to ops.json

def load_ops():
    """Load operator data from the ops.json file."""
    if os.path.exists(OPS_FILE):
        with open(OPS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {"operators": []}  # Default empty operators list

def save_ops(ops_data):
    """Save operator data to the ops.json file."""
    with open(OPS_FILE, 'w') as f:
        json.dump({"operators": ops_data["operators"]}, f, indent=4)

def save_ops_data(ops, world_folder):
    """Save operator data to the ops.json file."""
    ops_file = os.path.join(world_folder, "ops.json")
    print(f"Saving operator data to {ops_file}...")
    with open(ops_file, 'w') as f:
        json.dump(ops, f, indent=4)
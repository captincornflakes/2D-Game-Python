import os
import json

# Define the path to ops.json in the main server folder
OPS_FILE = os.path.join(os.path.dirname(__file__), "..", "ops.json")

def load_ops():
    """Load operator data from the ops.json file."""
    if os.path.exists(OPS_FILE):
        try:
            with open(OPS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding ops.json: {e}")
            return {"operators": []}
    else:
        print(f"ops.json not found. Creating a new one.")
        return {"operators": []}  # Default empty operators list

def save_ops(ops_data):
    """Save operator data to the ops.json file."""
    try:
        with open(OPS_FILE, 'w') as f:
            json.dump({"operators": ops_data["operators"]}, f, indent=4)
        print(f"Operator data successfully saved to {OPS_FILE}.")
    except Exception as e:
        print(f"Error saving operator data: {e}")
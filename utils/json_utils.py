# Import standard libraries
import json
import os

# Define the relative path to the directory containing all JSON data files
DATA_DIR = "./data"


# Function to load a JSON file from the data directory
def load_json(filename):
    # Construct the full path to the file
    path = os.path.join(DATA_DIR, filename)
    try:
        # Open and read the JSON file
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {path}")

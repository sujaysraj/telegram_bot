# utils/data.py

import json
import os

def load_data(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f)

    with open(file, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Fix broken/empty JSON file
            print(f"[WARNING] {file} was empty or invalid. Reinitializing.")
            json.dump({}, open(file, 'w'))
            return {}


def save_data(file, data):
    """
    Save data to a JSON file with pretty formatting.
    """
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)


import os
import json


def save_json(json_str, folder_path: str, filename: str):
    # Make sure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    python_data = json.loads(json_str)

    with open(filename, "w") as f:
        json.dump(python_data, f, indent=2)

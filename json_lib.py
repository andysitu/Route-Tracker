import os
import json


def save_json(json_str, folder_path: str, filename: str):
    # Make sure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    filepath = os.path.join(folder_path, filename)

    python_data = json.loads(json_str)

    with open(filepath, "w") as file:
        json.dump(python_data, file, indent=2)

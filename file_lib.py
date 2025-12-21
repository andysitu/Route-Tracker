import os
import json


def save_json(to_save_json, folder_path: str, filename: str):
    # Make sure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    filepath = os.path.join(folder_path, filename)

    if type(to_save_json) is str:
        to_save_json = json.loads(to_save_json)

    with open(filepath, "w") as file:
        json.dump(to_save_json, file, indent=2)

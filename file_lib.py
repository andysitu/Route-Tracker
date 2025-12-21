import os
import json
import route


def save_filename_to_data_list(filepath):
    data_list_folder_path = route.get_data_folder_path(None, False)

    list_filepath = os.path.join(data_list_folder_path, "data_list.txt")

    with open(list_filepath, "a") as file:
        file.write(filepath + "\n")


def save_json(to_save_json, folder_path: str, filename: str):
    # Make sure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    filepath = os.path.join(folder_path, filename)

    if type(to_save_json) is str:
        to_save_json = json.loads(to_save_json)

    with open(filepath, "w") as file:
        json.dump(to_save_json, file, indent=2)

    save_filename_to_data_list(filepath)

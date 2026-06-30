import json


def read_json(file_path):
    """
    Read JSON file and return data
    """
    with open(file_path, "r") as file:
        return json.load(file)
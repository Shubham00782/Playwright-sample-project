import json
import os


def read_json(file_path):
    """
    Read a JSON file by its absolute (or relative) path and return parsed data.
    """
    with open(file_path, "r") as file:
        return json.load(file)


def get_testdata_path(filename: str) -> str:
    """
    Resolve the absolute path to a file inside the project-root testdata/ folder.

    Uses this utility file's own location to anchor the project root, so the
    result is correct regardless of which test file calls it.

    Example:
        path = get_testdata_path("booking_payload.json")
        # → <project_root>/testdata/booking_payload.json
    """
    # utils/ is one level below the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, "testdata", filename)


def read_testdata_json(filename: str):
    """
    Load a JSON file from the project-root testdata/ folder in one call.

    Example:
        payload = read_testdata_json("booking_payload.json")
    """
    return read_json(get_testdata_path(filename))
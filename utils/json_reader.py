import json
from pathlib import Path


class JSONReader:
    def __init__(self, json_file_name):
        project_root = Path(__file__).resolve().parent.parent
        self.file_path = project_root / "test_data" / json_file_name

    def load_test_data(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)
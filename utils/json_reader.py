import json


class JSONReader:
    def __init__(self, json_file):
        self.json_file = json_file

    def load_test_data(self):
        with open(self.json_file, "r", encoding="utf-8") as file:
            return json.load(file)
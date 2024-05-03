import os
import json


class SaveManager:
    def __init__(self):
        self.data = {}

    def save_game(self):
        self.save_data(self.data)

    def reset_night(self):
        self.data["night"] = 1
        self.save_data(self.data)

    def reset_save(self):
        self.data = {"night": 1, "stars": 0}

    @staticmethod
    def save_data(data: dict) -> None:
        with open(f"data/saves/save.json", 'w') as f:
            f.write(json.dumps(data))

    def load_data(self) -> bool | dict:
        path = f"data/saves/save.json"
        if not os.path.isfile(path):
            return False
        with open(path, 'r') as f:
            self.data = json.loads(f.read())
            return self.data

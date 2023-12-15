import os
import json


class SaveManager:
    def __init__(self):
        self.data = {}

    def save_game(self) -> bool:
        self.save_data(self.data)
        return True

    def reset_save(self):
        self.save_data({"night": 1})

    @staticmethod
    def save_data(data: dict) -> None:
        with open(f"data/saves/save.json", 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def load_data() -> bool | dict:
        path = f"data/saves/save.json"
        if not os.path.isfile(path):
            return False
        with open(path, 'r') as f:
            return json.loads(f.read())
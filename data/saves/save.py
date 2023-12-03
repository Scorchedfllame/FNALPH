import os
import json


class SaveManager:
    def __init__(self):
        self._saves = [file for file in os.listdir('data/saves') if file.endswith('.json')]
        self._current_save = 0

    def save_game(self, data: dict) -> bool:
        if self._current_save != 0:
            self.save_data(data, self._current_save)
            return True
        return False

    @staticmethod
    def save_data(data: dict, save: int) -> None:
        with open(f"data/saves/save/{save}.json", 'w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def load_data(save: int) -> bool | dict:
        path = f"data/saves/save/{save}.json"
        if not os.path.isfile(path):
            return False
        with open(path, 'r') as f:
            return json.loads(f.read())

    def get_current_save(self) -> bool | int:
        if self._current_save == 0:
            return False
        return self._current_save

import json
from .game import Game
from .buttons import Button


class Jumpscare:
    def __init__(self, image_path: str, kill: bool, length: float, effect: None):
        self.image_path = image_path
        self.kill = kill
        self.length = length
        self.effect = effect

    @classmethod
    def load_data(cls, path: str) -> None:
        with open(path, 'r') as f:
            jumpscares = json.loads(f.read())
            for jumpscare in jumpscares:
                cls.__init__(jumpscare[0], jumpscare[1], jumpscare[2])

    def activate(self):
        pass


class Animatronic:
    def __init__(self, name: str, difficulty: int, jumpscare: Jumpscare = None):
        self.name = name
        self.difficulty = difficulty
        self.description, self.image_path = self.load_data()
        self.jumpscare = jumpscare

    def load_data(self) -> tuple[str, str]:
        with open('AppData/GameData/animatronics.json', 'r') as f:
            animatronic = json.loads(f.read())[self.name]
            return animatronic['description'], animatronic['image_path']

    def start_jumpscare(self):
        if self.jumpscare is not None:
            self.jumpscare.activate()
        else:
            print("BOO!")


class ThePuppet(Animatronic):
    def __init__(self, game: Game, difficulty: int):
        super().__init__("The Puppet", difficulty)
        self.game = game
        self.camera = game.systems['Cams System'].camera_list[5]
        self.camera.add_button()
        self.max_music_time = 1000
        self._music_box_time = self.max_music_time

    def tick(self) -> None:
        if self.game.utils['GMB'].active:
            self.add_time(self.game.utils["GMB"].puppet_amount)
        self.subtract_time(self.difficulty)

    def subtract_time(self, amount: int) -> None:
        self._music_box_time = max(self._music_box_time - amount, 0)

    def add_time(self, amount: int) -> None:
        self._music_box_time = min(amount + self.max_music_time, self.max_music_time)

    def update(self) -> None:
        if self._music_box_time <= 0:
            self.start_jumpscare()
            self.game.kill()


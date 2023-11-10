import json
from .game import Game
from .buttons import Button
import pygame


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
        self.kill_event = pygame.event.Event(pygame.USEREVENT + 2)
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
        self.CHARGE_AMOUNT = 20
        self.MAX_MUSIC_TIME = 100
        self.MUSIC_DECREASE_AMOUNT = 10
        self._charging = False
        self._music_box_time = 0
        self._game = game
        self._camera = game.systems['Cams System'].camera_list[5]
        self._timer = pygame.USEREVENT + 1
        self._camera.add_button()

    def start(self):
        pygame.time.set_timer(self._timer, (25 - self.difficulty) * 500)
        self._music_box_time = self.MAX_MUSIC_TIME

    def tick(self, event: pygame.event.Event) -> None:
        if event.type == self._timer:
            if self._game.utils['GMB'].active:
                self.add_time(self._game.utils["GMB"].puppet_amount)
            elif self._charging:
                self.add_time(self.CHARGE_AMOUNT)
            else:
                self.subtract_time(10)

    def stop_charge(self):
        self._charging = False

    def start_charge(self):
        self._charging = True

    def subtract_time(self, amount: int) -> None:
        self._music_box_time = max(self._music_box_time - amount, 0)

    def add_time(self, amount: int) -> None:
        self._music_box_time = min(amount + self.MAX_MUSIC_TIME, self.MAX_MUSIC_TIME)


class Bonnie(Animatronic):
    def __init__(self, game: Game, difficulty: int):
        super().__init__('Bonnie', difficulty)
        self._game = game
        self._location = 0

    def draw(self):
        camera_location = self.get_cam_from_location()
        camera = self.game.systems["Cams System"].camera_list[self._location]

    def get_cam_from_location()

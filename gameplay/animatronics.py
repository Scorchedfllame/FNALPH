import json
from .game import Game
from AppData.GameData.constants import *
import pygame
import random


class Jumpscare:
    def __init__(self, image_path: str, kill: bool, length: float, effect=None):
        self.image_path = image_path
        self.kill = kill
        self.length = length
        self.effect = effect

    @classmethod
    def load_data(cls, path: str) -> None:
        list_jumpscares = []
        with open(path, 'r') as f:
            jumpscares = json.loads(f.read())
            for jumpscare in jumpscares:
                list_jumpscares.append(cls(jumpscare[0], jumpscare[1], jumpscare[2]))
            return

    def activate(self):
        pass


class MenuLabel:
    """
    The thing being affected when using custom night functionality.
    """
    def __init__(self, name: str, difficulty: int, description: str, image_path: str, can_edit: bool = True):
        self.name = name
        self._difficulty = difficulty
        self.description = description
        self.image_path = image_path
        self.can_edit = can_edit


class Animatronic:
    """
    General class for all animatronics.
    Creating from this will make an empty animatronic with no functionality.
    """
    def __init__(self, name: str, difficulty: int, jumpscare: Jumpscare = None):
        self.name = name
        self._difficulty = difficulty
        self._aggression = self._difficulty
        description, image_path = self.load_data(('description', 'image_path'))
        self.menu_label = MenuLabel(self.name, self._difficulty, description, image_path)
        self.jumpscare = jumpscare

    def load_data(self, info: tuple) -> tuple:
        with open('AppData/GameData/animatronics.json', 'r') as f:
            animatronic = json.loads(f.read())[self.name]
            return tuple([animatronic[i] for i in info])

    def start_jumpscare(self) -> None:
        if self.jumpscare is not None:
            self.jumpscare.activate()
        else:
            print("BOO!")

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def tick(self, event: pygame.event.Event) -> None:
        pass

    def draw(self, screen) -> None:
        pass

    def kill(self):
        pygame.event.post(KILL)
        if self.jumpscare is not None:
            self.jumpscare.activate()

    def update_aggression(self, delta: int) -> None:
        self._aggression = max(min(self._aggression + delta, 20), 0)

    def reset_aggression(self) -> None:
        self._aggression = self._difficulty


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
        self._camera.add_button()

    def start(self) -> None:
        pygame.time.set_timer(PUPPET_TIMER, (20 - self._aggression) * 500)
        self._music_box_time = self.MAX_MUSIC_TIME

    def stop(self) -> None:
        pygame.time.set_timer(PUPPET_TIMER, 0)

    def tick(self, event: pygame.event.Event) -> None:
        if event.type == PUPPET_TIMER:
            if self._game.utils['GMB'].active:
                self.add_time(self._game.utils["GMB"].puppet_amount)
            elif self._charging:
                self.add_time(self.CHARGE_AMOUNT)
            else:
                self.subtract_time(10)
        if self._music_box_time <= 0:
            pygame.time.delay(random.randint(1000, 3000))
            self.kill()

    def stop_charge(self):
        self._charging = False

    def start_charge(self):
        self._charging = True

    def subtract_time(self, amount: int) -> None:
        self._music_box_time = max(self._music_box_time - amount, 0)

    def add_time(self, amount: int) -> None:
        self._music_box_time = min(amount + self.MAX_MUSIC_TIME, self.MAX_MUSIC_TIME)


class Bonnie(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """
    def __init__(self, game: Game, difficulty: int):
        super().__init__('Bonnie', difficulty)
        self.OFFICE_LOCATION = 5
        self._office = game.office
        self._cameras = game.systems["Cams System"].camera_list
        self._location = -1
        self._kill_locked = False
        self._camera_key, self._movement_key = self.load_data(('cameras', 'movements'))
        self.movement_timer = 5100

    def start(self) -> None:
        pygame.time.set_timer(BONNIE_TIMER, self.movement_timer)
        self._location = 0

    def stop(self) -> None:
        pygame.time.set_timer(BONNIE_TIMER, 0)
        self._location = -1

    def tick(self, event: pygame.event.Event) -> None:
        if event.type == BONNIE_TIMER:
            if self._kill_locked:
                self.kill()
            # Movement Opportunities
            rng = random.randint(1, 20)
            if self._location == self.OFFICE_LOCATION and rng < self._aggression:
                # Get whether door is closed
                if self._office.door_left:
                    self.blocked()
                else:
                    self._office.lock()
                    self._kill_locked = True
                    pygame.time.set_timer(BONNIE_TIMER, random.randint(15000, 25000))
            elif rng <= self._aggression:
                self.move()
        if event.type == CAMERA_FLIPPED_DOWN and self._kill_locked:
            self.kill()

    def blocked(self):
        self._kill_locked = False
        self._location = random.randint(0, 1)

    def move(self) -> None:
        movements = self._movement_key
        moves = movements[str(self._location)]
        self._location = moves[random.randint(0, len(moves)-1)]

    def draw(self, screen) -> None:
        if self._location == self.OFFICE_LOCATION:
            if self._office.active:
                screen.blit(self._get_image())
        else:
            camera_location = self._get_cam_index_from_location()
            camera = self._cameras[camera_location]
            if camera.active:
                screen.blit(self._get_image())

    # Some sort of dictionary with all the images and stages that bonnie possesses
    def _get_image(self) -> any:
        return pygame.image.load('resources/sprites/animatronics/bonnie/bonnie' + str(self._location)).convert_alpha()

    def _get_cam_index_from_location(self) -> int:
        cameras = self._camera_key
        camera = cameras[str(self._location)]
        return camera

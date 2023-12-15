import json
from data.game.constants import *
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
        description = self.load_data()['menu_label']['description']
        image_path = self.load_data()['menu_label']['image_path']
        self.menu_label = MenuLabel(self.name, self._difficulty, description, image_path)
        self.jumpscare = jumpscare

    def load_data(self) -> dict:
        with open('data/game/animatronics.json', 'r') as f:
            animatronic = json.loads(f.read())[self.name]
            return animatronic

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
    def __init__(self, game: any, difficulty: int):
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


class Chica(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any, difficulty: int):
        super().__init__('Chica', difficulty)
        self._office = game.office
        self.door = game.office.doors[1]
        self._game = game
        self._cameras = game.systems["Cameras"].camera_list
        self._location = 0
        self._kill_locked = False
        self._camera_key = self.load_data()['cameras']
        self._movement_key = self.load_data()['movements']
        self.FILE_LOCATION = 'resources/sprites/animatronics/baddie/chirca_'
        self.open_light = pygame.image.load(self.FILE_LOCATION+'open_light.png').convert()
        self.open_light = pygame.transform.scale_by(self.open_light, pygame.display.get_surface().get_height()/
                                                    self.open_light.get_height())
        self.closed_light = pygame.image.load(self.FILE_LOCATION + 'closed_light.png').convert()
        self.closed_light = pygame.transform.scale_by(self.closed_light, pygame.display.get_surface().get_height() /
                                                      self.closed_light.get_height())
        self.TIMER = CHICA_TIMER
        self.movement_timer = 4900
        self.OFFICE_LOCATION = len(self._movement_key)

    def start(self) -> None:
        pygame.time.set_timer(self.TIMER, self.movement_timer)
        self.update_images()

    def stop(self) -> None:
        pygame.time.set_timer(self.TIMER, 0)
        self._location = -1

    def tick(self, event: pygame.event.Event) -> None:
        if event.type == self.TIMER:
            if self._kill_locked:
                self.kill()
            # Movement Opportunities
            rng = random.randint(1, 20)
            if self._location == self.OFFICE_LOCATION:
                if rng < self._aggression:
                    # Get whether door is closed
                    if self.door.door_status == 'closed':
                        self.blocked()
                    else:
                        self.door.lock()
                        self._kill_locked = True
                        pygame.time.set_timer(BONNIE_TIMER, random.randint(15000, 25000))
            elif rng <= self._aggression:
                movements = self._movement_key
                moves = movements[self._location]
                self.move(moves[random.randint(0, len(moves) - 1)])
        if event.type == CAMERA_FLIPPED_DOWN and self._kill_locked:
            self.kill()

    def blocked(self):
        self._kill_locked = False
        self.move(random.randint(0, 1))

    def move(self, position: int) -> None:
        self._update_camera()
        self.camera.reset_background()
        self._location = position
        self._game.update_animatronics()

    def update_images(self) -> None:
        if self._location != self.OFFICE_LOCATION:
            self._update_camera()
            self.camera.background.blit(self._get_image(), (0, 0))
        else:
            self.door.curr_images['open_light'] = self.open_light
            self.door.curr_images['closed_light'] = self.closed_light

    # Some sort of dictionary with all the images and stages that bonnie possesses
    def _get_image(self) -> any:
        image = pygame.image.load(
            self.FILE_LOCATION + str(self._location) + '.png').convert_alpha()
        return pygame.transform.scale_by(image, pygame.display.get_surface().get_height() / image.get_height())

    def _update_camera(self):
        if self._location != self.OFFICE_LOCATION:
            cameras = self._camera_key
            camera = cameras[self._location]
            self.camera = self._cameras[camera]
        else:
            self.door.reset()


class Bonnie(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any, difficulty: int):
        super().__init__('Bonnie', difficulty)
        self._office = game.office
        self.door = game.office.doors[0]
        self._game = game
        self._cameras = game.systems["Cameras"].camera_list
        self._location = 0
        self._kill_locked = False
        self._camera_key = self.load_data()['cameras']
        self._movement_key = self.load_data()['movements']
        self.FILE_LOCATION = 'resources/sprites/animatronics/bonnie/bonbie_'
        self.open_light = pygame.image.load(self.FILE_LOCATION+'open_light.png').convert()
        self.open_light = pygame.transform.scale_by(self.open_light, pygame.display.get_surface().get_height()/
                                                    self.open_light.get_height())
        self.closed_light = pygame.image.load(self.FILE_LOCATION + 'closed_light.png').convert()
        self.closed_light = pygame.transform.scale_by(self.closed_light, pygame.display.get_surface().get_height() /
                                                      self.closed_light.get_height())
        self.TIMER = BONNIE_TIMER
        self.movement_timer = 5100
        self.OFFICE_LOCATION = len(self._movement_key)

    def start(self) -> None:
        pygame.time.set_timer(self.TIMER, self.movement_timer)
        self.update_images()

    def stop(self) -> None:
        pygame.time.set_timer(self.TIMER, 0)
        self._location = -1

    def tick(self, event: pygame.event.Event) -> None:
        if event.type == self.TIMER:
            if self._kill_locked:
                self.kill()
            # Movement Opportunities
            rng = random.randint(1, 20)
            if self._location == self.OFFICE_LOCATION:
                if rng < self._aggression:
                    # Get whether door is closed
                    if self.door.door_status == 'closed':
                        self.blocked()
                    else:
                        self.door.lock()
                        self._kill_locked = True
                        pygame.time.set_timer(BONNIE_TIMER, random.randint(15000, 25000))
            elif rng <= self._aggression:
                movements = self._movement_key
                moves = movements[self._location]
                self.move(moves[random.randint(0, len(moves) - 1)])
        if event.type == CAMERA_FLIPPED_DOWN and self._kill_locked:
            self.kill()

    def blocked(self):
        self._kill_locked = False
        self.move(random.randint(0, 1))

    def move(self, position: int) -> None:
        self._update_camera()
        self.camera.reset_background()
        self._location = position
        self._game.update_animatronics()

    def update_images(self) -> None:
        if self._location != self.OFFICE_LOCATION:
            self._update_camera()
            self.camera.background.blit(self._get_image(), (0, 0))
        else:
            self.door.curr_images['open_light'] = self.open_light
            self.door.curr_images['closed_light'] = self.closed_light

    # Some sort of dictionary with all the images and stages that bonnie possesses
    def _get_image(self) -> any:
        image = pygame.image.load(
            self.FILE_LOCATION + str(self._location) + '.png').convert_alpha()
        return pygame.transform.scale_by(image, pygame.display.get_surface().get_height() / image.get_height())

    def _update_camera(self):
        if self._location != self.OFFICE_LOCATION:
            cameras = self._camera_key
            camera = cameras[self._location]
            self.camera = self._cameras[camera]
        else:
            self.door.reset()


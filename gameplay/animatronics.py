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
        self.move_sounds = [pygame.mixer.Sound('resources/sounds/footsteps_' + str(i) + '.mp3') for i in range(1, 5)]
        self.video = None

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
        kill = pygame.event.Event(KILL, {"video": self.video})
        pygame.event.post(kill)
        if self.jumpscare is not None:
            self.jumpscare.activate()

    def update_aggression(self, delta: int) -> None:
        self._aggression = max(min(self._aggression + delta, 20), 0)

    def reset_aggression(self) -> None:
        self._aggression = self._difficulty


class Chica(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any, difficulty: int):
        super().__init__('Chica', difficulty)
        self._office = game.office
        self.door = game.office.doors[0]
        self._game = game
        self._cameras = game.systems["Cameras"].camera_list
        self._location = 0
        self._kill_locked = False
        self._camera_key = self.load_data()['cameras']
        self._movement_key = self.load_data()['movements']
        self.FILE_LOCATION = 'resources/sprites/animatronics/chica/chica_'
        # self.video = pygame.image.load(self.FILE_LOCATION+'jumpscare.png').convert_alpha()

        self.open_light = pygame.image.load(self.FILE_LOCATION+'open_light.png').convert_alpha()
        self.open_light = pygame.transform.scale_by(self.open_light, pygame.display.get_surface().get_height()/
                                                    self.open_light.get_height())
        self.closed_light = pygame.image.load(self.FILE_LOCATION + 'closed_light.png').convert_alpha()
        self.closed_light = pygame.transform.scale_by(self.closed_light, pygame.display.get_surface().get_height() /
                                                      self.closed_light.get_height())
        self.TIMER = CHICA_TIMER
        self.movement_timer = 4900
        self.OFFICE_LOCATION = len(self._camera_key)

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
                if rng <= self._aggression:
                    # Get whether door is closed
                    if self.door.door_status == 'closed':
                        self.blocked()
                    else:
                        self.door.lock()
                        self._kill_locked = True
                        pygame.time.set_timer(self.TIMER, random.randint(15000, 25000))
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
        self.door.reset()
        self.camera.reset_background()
        self._location = position
        self._game.update_animatronics()
        self.move_sounds[random.randint(0, len(self.move_sounds)-1)].play()

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


class Bonnie(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any, difficulty: int):
        super().__init__('Bonnie', difficulty)
        self._office = game.office
        self.door = game.office.doors[1]
        self._game = game
        self._cameras = game.systems["Cameras"].camera_list
        self._location = 0
        self._kill_locked = False
        self._camera_key = self.load_data()['cameras']
        self._movement_key = self.load_data()['movements']
        self.FILE_LOCATION = 'resources/sprites/animatronics/bonnie/bonnie_'
        self.open_light = pygame.image.load(self.FILE_LOCATION+'open_light.png').convert_alpha()
        self.open_light = pygame.transform.scale_by(self.open_light, pygame.display.get_surface().get_height()/
                                                    self.open_light.get_height())
        self.closed_light = pygame.image.load(self.FILE_LOCATION + 'closed_light.png').convert_alpha()
        self.closed_light = pygame.transform.scale_by(self.closed_light, pygame.display.get_surface().get_height() /
                                                      self.closed_light.get_height())
        self.TIMER = BONNIE_TIMER
        self.movement_timer = 5100
        self.OFFICE_LOCATION = len(self._camera_key)

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
                if rng <= self._aggression:
                    # Get whether door is closed
                    if self.door.door_status == 'closed':
                        self.blocked()
                    else:
                        self.door.lock()
                        self._kill_locked = True
                        pygame.time.set_timer(self.TIMER, random.randint(15000, 25000))
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
        self.door.reset()
        self.camera.reset_background()
        self._location = position
        self._game.update_animatronics()
        self.move_sounds[random.randint(0, len(self.move_sounds)-1)].play()

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


class Lefty(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any, difficulty: int):
        super().__init__('Lefty', difficulty)
        self._office = game.office
        self.door = game.office.doors[0]
        self._game = game
        self._cameras = game.systems["Cameras"].camera_list
        self._location = 0
        self._kill_locked = False
        self._camera_key = self.load_data()['cameras']
        self._movement_key = self.load_data()['movements']
        self.FILE_LOCATION = 'resources/sprites/animatronics/lefty/lefty_'
        self.open_light = pygame.image.load(self.FILE_LOCATION+'open_light.png').convert_alpha()
        self.open_light = pygame.transform.scale_by(self.open_light, pygame.display.get_surface().get_height()/
                                                    self.open_light.get_height())
        self.closed_light = pygame.image.load(self.FILE_LOCATION + 'closed_light.png').convert_alpha()
        self.closed_light = pygame.transform.scale_by(self.closed_light, pygame.display.get_surface().get_height() /
                                                      self.closed_light.get_height())
        self.TIMER = LEFTY_TIMER
        self.movement_timer = 2500
        self.OFFICE_LOCATION = len(self._camera_key)

    def start(self) -> None:
        pygame.time.set_timer(self.TIMER, self.movement_timer)
        self.update_images()
        print(self._location)

    def stop(self) -> None:
        pygame.time.set_timer(self.TIMER, 0)
        self._location = -1

    def tick(self, event: pygame.event.Event) -> None:
        if event.type == self.TIMER and not self.camera.active:
            if self._kill_locked:
                self.kill()
            # Movement Opportunities
            rng = random.randint(1, 20)
            if self._location == self.OFFICE_LOCATION:
                if rng <= self._aggression:
                    # Get whether door is closed
                    if self.door.door_status == 'closed':
                        self.blocked()
                    else:
                        self.door.lock()
                        self._kill_locked = True
                        pygame.time.set_timer(self.TIMER, random.randint(15000, 25000))
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
        self.door.reset()
        self.camera.reset_background()
        self._location = position
        self._game.update_animatronics()
        self.move_sounds[random.randint(0, len(self.move_sounds) - 1)].play()

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


class Knight(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any, difficulty: int):
        super().__init__('Knight', difficulty)
        self._game = game
        self.door = self._game.office.doors[0]
        cameras = game.systems["Cameras"].camera_list
        self.camera = cameras[4]
        self._location = 0
        self.FILE_LOCATION = 'resources/sprites/animatronics/knight/knight_'
        self.TIMER = KNIGHT_TIMER
        self.aggression = 0
        self.movement_timer = 100
        self.OFFICE_LOCATION = 4
        self.MAX_AGGRESSION = 18000

    def start(self) -> None:
        pygame.time.set_timer(self.TIMER, self.movement_timer)
        self.update_images()

    def stop(self) -> None:
        pygame.time.set_timer(self.TIMER, 0)
        self._location = -1

    def tick(self, event: pygame.event.Event) -> None:
        if event.type == self.TIMER:
            if not self.camera.active:
                self.aggression += self._difficulty * 20
                # Movement Opportunities
                if self.aggression >= self.MAX_AGGRESSION:
                    if self._location == self.OFFICE_LOCATION:
                        if self.door.door_status == 'closed':
                            self.blocked()
                        else:
                            self.kill()
                    else:
                        self.move(self._location + 1)
                        self.aggression = 0
            else:
                self.aggression = random.randint(0, 3000)

    def blocked(self):
        self.aggression = 0
        self.move(0)

    def move(self, position: int) -> None:
        self._update_camera()
        self.camera.reset_background()
        self._location = position
        self._game.update_animatronics()

    def update_images(self) -> None:
        if self._location != self.OFFICE_LOCATION:
            self._update_camera()
            self.camera.background.blit(self._get_image(), (0, 0))

    # Some sort of dictionary with all the images and stages that bonnie possesses
    def _get_image(self) -> any:
        image = pygame.image.load(
            self.FILE_LOCATION + str(self._location) + '.png').convert_alpha()
        return pygame.transform.scale_by(image, pygame.display.get_surface().get_height() / image.get_height())

    def _update_camera(self):
        pass


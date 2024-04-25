import json
from data.game.constants import *
import pygame
import random
import os
from .animation import Animator


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
    def __init__(self, name: str, game, movement_timer_length: int, timer: int, door: int):
        self.name = name
        self._difficulty = 0
        self._aggression = self._difficulty
        description = self.load_data()['menu_label']['description']
        image_path = self.load_data()['menu_label']['image_path']
        self.menu_label = MenuLabel(self.name, self._difficulty, description, image_path)
        self.move_sounds = [pygame.mixer.Sound('resources/sounds/footsteps_' + str(i) + '.mp3') for i in range(1, 5)]
        for sound in self.move_sounds:
            sound.set_volume(.25)
        self.video = None
        self._office = game.office
        self.door = game.office.doors[door]
        self._game = game
        self._cameras = game.systems["Cameras"].camera_list
        self._location = 0
        self._kill_locked = False
        self._camera_key = self.load_data()['cameras']
        self._movement_key = self.load_data()['movements']
        self.FILE_LOCATION = f'resources/sprites/animatronics/{name}/'
        self.images = os.listdir(self.FILE_LOCATION)
        self.img_dict = {}
        for image in self.images:
            self.img_dict[image.removesuffix('.png')] = pygame.image.load(self.FILE_LOCATION + image).convert_alpha()
        self.TIMER = timer
        self.movement_timer = movement_timer_length
        self.OFFICE_LOCATION = len(self._camera_key)
        self.active = False
        self.camera = self._cameras[self._camera_key[0]]
        if 'jumpscare' in self.load_data().keys():
            jump_data = self.load_data()['jumpscare']
            self.jumpscare = Animator(pygame.image.load(self.FILE_LOCATION + "jumpscare.png").convert_alpha(),
                                      pygame.rect.Rect(0, 0, jump_data[0],
                                                       jump_data[1]),
                                      scale_to_fit=True,
                                      speed=jump_data[2]/100,
                                      type='jump')
        else:
            self.jumpscare = None

    def load_data(self) -> dict:
        with open('data/game/animatronics.json', 'r') as f:
            animatronic = json.loads(f.read())[self.name]
            return animatronic

    def kill(self):
        kill = pygame.event.Event(KILL, {"animation": self.jumpscare})
        pygame.event.post(kill)

    def set_difficulty(self, difficulty: int):
        self._difficulty = difficulty
        self._aggression = self._difficulty

    def update_aggression(self, delta: int) -> None:
        self._aggression = max(min(self._aggression + delta, 20), 0)

    def reset_aggression(self) -> None:
        self._aggression = self._difficulty

    def start(self) -> None:
        self.active = True
        pygame.time.set_timer(self.TIMER, self.movement_timer)
        self._location = 0
        self.reset_aggression()
        self.update_images()

    def stop(self) -> None:
        pygame.time.set_timer(self.TIMER, 0)
        self._location = -1
        self.active = False

    def tick(self, event: pygame.event.Event) -> None:
        if self.active:
            if event.type == self.TIMER:
                if self._kill_locked:
                    self.kill()
                # Movement Opportunities
                rng = random.randint(1, 20)
                if rng <= self._aggression:
                    self.successful_movement()
            if event.type == CAMERA_FLIPPED_DOWN and self._kill_locked:
                self.kill()

    def successful_movement(self):
        if self._location == self.OFFICE_LOCATION:
            # Get whether door is closed
            self.at_door()
        else:
            self.move(self.get_movement())

    def at_door(self):
        if self.door.door_status == 'closed':
            self.blocked()
        else:
            self.door.lock()
            self._kill_locked = True
            pygame.time.set_timer(self.TIMER, random.randint(15000, 25000))

    def get_movement(self):
        movements = self._movement_key
        moves = movements[self._location]
        return moves[random.randint(0, len(moves) - 1)]

    def blocked(self):
        self._kill_locked = False
        self.move(self.get_movement())

    def move(self, position: int) -> None:
        if self.camera.active:
            self.camera.small_glitch()
        self._update_camera()
        self.door.reset()
        self.camera.reset_background()
        self._location = position
        self._game.update_animatronics()
        self.move_sounds[random.randint(0, len(self.move_sounds)-1)].play()
        pygame.time.set_timer(self.TIMER, self.movement_timer)
        if self.camera.active:
            self.camera.small_glitch()
        self._update_camera()

    def update_images(self) -> None:
        if self.active:
            if self._location != self.OFFICE_LOCATION:
                self._update_camera()
                self.camera.background.blit(self._get_image(), (0, 0))
            else:
                self.door.curr_images['open_light'] = self.img_dict[self.name.lower() + '_' + 'open_light']
                self.door.curr_images['closed_light'] = self.img_dict[self.name.lower() + '_' + 'closed_light']

    # Some sort of dictionary with all the images and stages that bonnie possesses
    def _get_image(self) -> any:
        return self.img_dict[self.name.lower() + '_' + str(self._location)]

    def _update_camera(self):
        if self._location != self.OFFICE_LOCATION:
            cameras = self._camera_key
            camera = cameras[self._location]
            self.camera = self._cameras[camera]


class Chica(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any):
        super().__init__('Chica', game, 4980, CHICA_TIMER, 0)

    def move(self, position: int) -> None:
        lefty = self._game.animatronics[2]
        office = position == self.OFFICE_LOCATION and lefty._location == lefty.OFFICE_LOCATION
        shoulder = position == self.OFFICE_LOCATION - 1 and lefty._location == lefty.OFFICE_LOCATION - 1
        if not (office or shoulder):
            if self.camera.active:
                self.camera.small_glitch()
            self._update_camera()
            self.door.reset()
            self.camera.reset_background()
            self._location = position
            self._game.update_animatronics()
            self.move_sounds[random.randint(0, len(self.move_sounds)-1)].play()
            pygame.time.set_timer(self.TIMER, self.movement_timer)
            if self.camera.active:
                self.camera.small_glitch()
            self._update_camera()


class Bonnie(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any):
        super().__init__('Bonnie', game, 4970, BONNIE_TIMER, 1)


class Lefty(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any):
        super().__init__('Lefty', game, 3020, LEFTY_TIMER, 0)

    def tick(self, event: pygame.event.Event) -> None:
        if self.active:
            if self.camera.active:
                pygame.time.set_timer(self.TIMER, self.movement_timer)
            if event.type == self.TIMER:
                if self._kill_locked:
                    self.kill()
                # Movement Opportunities
                rng = random.randint(1, 20)
                if rng <= self._aggression:
                    self.successful_movement()
            if event.type == CAMERA_FLIPPED_DOWN and self._kill_locked:
                self.kill()

    def move(self, position: int) -> None:
        chica = self._game.animatronics[1]
        office = position == self.OFFICE_LOCATION and chica._location == chica.OFFICE_LOCATION
        shoulder = position == self.OFFICE_LOCATION - 1 and chica._location == chica.OFFICE_LOCATION - 1
        if not (office or shoulder):
            if self.camera.active:
                self.camera.small_glitch()
            self._update_camera()
            self.door.reset()
            self.camera.reset_background()
            self._location = position
            self._game.update_animatronics()
            self.move_sounds[random.randint(0, len(self.move_sounds) - 1)].play()
            pygame.time.set_timer(self.TIMER, self.movement_timer)
            if self.camera.active:
                self.camera.small_glitch()


class Knight(Animatronic):
    """
    Starts in the lunchroom, moves around the left side and attacks at the left door.
    """

    def __init__(self, game: any):
        super().__init__('Knight', game, 5010, KNIGHT_TIMER, 0)
        self.primed = False
        self.running = False
        self.locked = False
        self.attack_num = 0
        self.run_sound = pygame.mixer.Sound('resources/sounds/fnaf-running.mp3')
        self.OFFICE_LOCATION = 3

    def start(self):
        self.active = True
        self.primed = False
        self.running = False
        self.locked = False
        self.attack_num = 0
        pygame.time.set_timer(self.TIMER, self.movement_timer)
        self._location = 0
        self.reset_aggression()
        self.update_images()

    def run(self):
        self.primed = False
        self.running = True
        pygame.mixer.find_channel(True).play(self.run_sound)
        pygame.time.set_timer(self.TIMER, int(self.run_sound.get_length() * 1000))

    def get_to_door(self):
        if self.door.door_status == 'closed':
            self.blocked()
        else:
            self.kill()
            self.move(0)

    def blocked(self):
        self.running = False
        pygame.time.set_timer(self.TIMER, self.movement_timer)
        self.move(self.get_movement())
        self._game.power_manager.power_remaining -= (5 ** self.attack_num) * 1000
        self.attack_num += 1

    def tick(self, event: pygame.event.Event) -> None:
        if self.active:
            if self.camera.active:
                if self.primed:
                    self.run()
                elif not self.running:
                    self.locked = True
                    pygame.time.set_timer(self.TIMER, random.randint(830, 16670))
            if event.type == self.TIMER:
                if self.locked:
                    self.locked = False
                else:
                    pygame.time.set_timer(self.TIMER, self.movement_timer)
                    rng = random.randint(1, 20)
                    if self.primed:
                        self.run()
                    elif self.running:
                        self.get_to_door()
                    # Movement Opportunities
                    elif rng <= self._aggression and not self.locked:
                        self.successful_movement()

    def move(self, position: int) -> None:
        self.camera.reset_background()
        self._location = position
        self._game.update_animatronics()

    def successful_movement(self):
        self.move(self.get_movement())
        if self._location == self.OFFICE_LOCATION:
            pygame.time.set_timer(self.TIMER, 25000)
            self.primed = True

    def update_images(self) -> None:
        self.camera.background.blit(self._get_image(), (0, 0))


class Hitch(Animatronic):
    def __init__(self, game: any):
        super().__init__("Hitch", game, 5010, HITCH_TIMER, 0)
        self.images = None
        self.img_dict = None
        self.black = pygame.surface.Surface((1920*2, 1080))
        self.black.fill('black')

    def update_images(self) -> None:
        self.camera.background.blit(self.black, (0, 0))

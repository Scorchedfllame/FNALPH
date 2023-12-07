import pygame
from data.game.constants import *
from .buttons import ToggleButton
import json


class Office:
    def __init__(self):
        self.doors = Door.generate_doors()
        self.IMAGE_SCALE_SIZE = 2
        self.image = pygame.image.load('resources/backgrounds/offices/office.png').convert()
        self.image = pygame.transform.scale_by(self.image, self.IMAGE_SCALE_SIZE)
        self.surface = pygame.surface.Surface(self.image.get_size())
        self.rot_x = 0
        self.MAX_ROTATION = 90
        self.active = True
        self._locked = False

    def get_power_usage(self):
        power_usage = 0
        for i in self.doors:
            if i.door_status == 'closed':
                power_usage += 1
        return power_usage

    def tick(self, event: pygame.event.Event):
        if event.type == CAMERA_FLIPPED_UP:
            self.active = False
        if event.type == CAMERA_FLIPPED_DOWN:
            self.active = True
        if self.active:
            for door in self.doors:
                door.tick(event)

    def frame(self):
        if self.active:
            self.rot_x += self.get_rot_from_mouse(pygame.mouse.get_pos())
            self.rot_x = max(-self.MAX_ROTATION, self.rot_x)
            self.rot_x = min(self.MAX_ROTATION, self.rot_x)

    @staticmethod
    def get_rot_from_mouse(mouse_pos):
        mouse_x, _ = mouse_pos
        screen_x, _ = pygame.display.get_surface().get_size()
        normalized = (2 * mouse_x/screen_x - 1)
        if screen_x * 2/5 > mouse_x or mouse_x > screen_x * 3/5:
            return normalized * 10
        return 0

    def get_pos_from_rot(self):
        screen_x, _ = pygame.display.get_surface().get_size()
        image_x, _ = self.image.get_size()
        # normalization 0-1
        normalized = (self.rot_x + self.MAX_ROTATION)/(2*self.MAX_ROTATION)

        # turn into other stuff
        return normalized * (screen_x - image_x)

    def draw(self):
        if self.active:
            screen = pygame.display.get_surface()
            rect = self.surface.get_rect()
            self.surface.blit(self.image, (0, 0))
            screen.blit(self.surface, (self.get_pos_from_rot(), 0))
            for door in self.doors:
                door.draw(screen, pygame.Vector2(self.get_pos_from_rot(), 0))

    def lock(self):
        self._locked = True


class Door:
    def __init__(self, image_paths: dict[str], relative_pos: tuple[int, int] = (0, 0)):
        self._default_images = {key: pygame.image.load(value).convert() for key, value in image_paths.items()}
        self.curr_images = self._default_images.copy()
        self.light_status = 'dark'
        self.door_status = 'open'
        self.relative_pos = relative_pos
        self.current_surface = self.curr_images[self.get_status()]
        self.rect = self.current_surface.get_rect()
        self.rect.topleft = self.relative_pos
        # self.light_button = Button(self.curr_images['light_button_off'], (0, 0), self.light_on, self.light_off)
        self.door_button = ToggleButton(self.curr_images['door_button_off'],
                                        (self.rect.x, self.rect.y),
                                        self.close_door,
                                        self.open_door)

    @classmethod
    def generate_doors(cls) -> list:
        door_list = []
        with open('data/game/office.json', 'r') as f:
            dictionary = json.loads(f.read())
            for door in dictionary['doors']:
                door_list.append(Door(door['images'], tuple(door['pos'])))
        return door_list

    def tick(self, event: pygame.event.Event):
        self.door_button.tick(event)
        # self.light_button.tick(event)

    def draw(self, surface: pygame.Surface, vector: pygame.Vector2):
        self.rect.topleft = (0, 0)
        self.rect.move_ip(vector)
        self.door_button.resize(self.rect.topleft)
        self.door_button.draw(surface)
        # self.light_button.draw(surface)

    def light_on(self):
        self.light_status = 'light'

    def light_off(self):
        self.light_status = 'dark'

    def get_status(self):
        return f"{self.door_status}_{self.light_status}"

    def open_door(self):
        self.door_status = 'open'
        self.current_surface = self.curr_images[f"open_{self.light_status}"]

    def close_door(self):
        self.door_status = 'closed'
        self.current_surface = self.curr_images[f"closed_{self.light_status}"]


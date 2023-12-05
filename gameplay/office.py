import pygame
from data.game.constants import *
from .buttons import Button
import random


class Office:
    def __init__(self):
        self.door_left = False
        self.door_right = False
        self.vent_door = False
        self.light_left = False
        self.light_right = False
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
        for i in [self.door_left, self.door_right, self.light_left, self.light_right]:
            if i:
                power_usage += 1
        return power_usage

    def tick(self, event: pygame.event.Event):
        if event.type == CAMERA_FLIPPED_UP:
            self.active = False
        if event.type == CAMERA_FLIPPED_DOWN:
            self.active = True

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

    def lock(self):
        self._locked = True


class Door:
    def __init__(self, image_paths: dict[str]):
        self.images = {'open_dark': pygame.image.load(image_paths['open_dark']).convert(),
                       'open_light': pygame.image.load(image_paths['open_light']).convert(),
                       'closed_dark': pygame.image.load(image_paths['closed_dark']).convert(),
                       'closed_light': pygame.image.load(image_paths['closed_light']).convert(),
                       'button_on': pygame.image.load(image_paths['button_on']).convert(),
                       'button_off': pygame.image.load(image_paths['button_off']).convert()}
        self.light_button = LightButton(image_paths['light_on'], image_paths['light_off'])
        self.light_status = 'dark'
        self.door_status = 'open'
        self.current_surface = self.images[self.get_status()]
        self.rect = self.current_surface.get_rect()

    def update_light_status(self):
        if self.light_button.on:
            self.light_status = 'light'
        else:
            self.light_status = 'dark'

    def get_status(self):
        return f"{self.door_status}_{self.light_status}"

    def open_door(self):
        self.current_surface = self.images[f"open_{self.light_status}"]

    def close_door(self):
        self.current_surface = self.images[f"closed_{self.light_status}"]


class LightButton:
    def __init__(self, on_image_path: str, off_image_path: str):
        self.on_image = pygame.image.load(on_image_path).convert()
        self.off_image = pygame.image.load(off_image_path).convert()
        self.on = False


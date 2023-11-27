import pygame
from AppData.GameData.constants import *


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
        self.rot_x = 45
        self.MAX_ROTATION = 45
        self.active = True
        self._locked = False

    def tick(self, event: pygame.event.Event):
        if event.type == CAMERA_FLIPPED_UP:
            self.active = False
        if event.type == CAMERA_FLIPPED_DOWN:
            self.active = True

    def get_pos_from_rot(self):
        screen_x, _ = pygame.display.get_surface().get_size()
        image_x, _ = self.image.get_size()
        # normalization 0-1
        normalized = (self.rot_x + 45)/90

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

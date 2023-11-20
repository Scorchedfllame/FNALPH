import pygame
from AppData.GameData.constants import *


class Office:
    def __init__(self):
        self.door_left = False
        self.door_right = False
        self.vent_door = False
        self.light_left = False
        self.light_right = False
        self.active = True
        self._locked = False

    def tick(self, event: pygame.event.Event):
        if event.type == CAMERA_FLIPPED_UP:
            self.active = False
        if event.type == CAMERA_FLIPPED_DOWN:
            self.active = True

    def draw(self):
        if self.active:
            screen = pygame.display.get_surface()
            screen.blit(pygame.image.load('resources/backgrounds/offices/office.png').convert(), (0, 0))

    def lock(self):
        self._locked = True

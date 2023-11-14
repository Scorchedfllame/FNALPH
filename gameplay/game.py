from .office import Office
import pygame
from AppData.GameData.constants import *


class Game:
    def __init__(self):
        self.timer = 0
        self.utils = {}
        self.animatronics = []
        self.update_animatronics = []
        self.systems = {}
        self.office = Office()
        self._win = False
        self._killed = False
        self.power = 100
        self.power_remaining = 10000
        self.power_usage = 1
        self.POWER_DIFFICULTY = 7

    def start(self):
        pygame.time.set_timer(UPDATE_POWER, 1000)

    def update_power(self):
        self.power_remaining -= self.POWER_DIFFICULTY * (2 ** self.power_usage)
        self.power = round(self.power_remaining / 100)
        if self.power_remaining <= 0:
            pygame.event.post(BLACKOUT)

    def global_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            for animatronic in self.update_animatronics:
                animatronic.tick(event)
            if event.type == UPDATE_POWER:
                self.update_power()

    def kill(self):
        if not self._win:
            self._killed = True
            self.stop_timer()

    def stop_timer(self):
        pass



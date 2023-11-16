from gameplay.office import Office
from gameplay.systems import Cameras, Vents
from AppData.GameData.constants import *
from gameplay.buttons import *
import pygame
from AppData.GameData.constants import *


class Game:
    def __init__(self):
        self.timer = 0
        self.utils = {}
        self.animatronics = []
        self.update_animatronics = []
        self.systems = {"Cameras": Cameras()}
        self.buttons = []
        self.office = Office()
        self._win = False
        self._killed = False
        self.power = 100
        self.power_remaining = 10000
        self.power_usage = 1
        self.POWER_DIFFICULTY = 7
        self.events = self.init_events()
        self.init_buttons()

    @staticmethod
    def init_events() -> dict:
        camera_up_event = pygame.event.Event(CAMERA_FLIPPED_UP)
        camera_down_event = pygame.event.Event(CAMERA_FLIPPED_DOWN)
        return {"camera_up_event": camera_up_event, "camera_down_event": camera_down_event}

    def init_buttons(self):
        flick_button = pygame.image.load('resources/ui/flick.png').convert_alpha()
        camera_flick = Flick(flick_button,
                             (300, 400),
                             self.events['camera_up_event'],
                             self.events['camera_down_event'])
        self.buttons.append(camera_flick)

    def start(self):
        pygame.time.set_timer(UPDATE_POWER, 1000)

    def update_power(self):
        self.power_remaining -= self.POWER_DIFFICULTY * (2 ** self.power_usage)
        self.power = round(self.power_remaining / 100)
        if self.power_remaining <= 0:
            pygame.event.post(BLACKOUT)

    def tick(self, event: pygame.event.Event):
        if event.type == UPDATE_POWER:
            self.update_power()

    def global_tick(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
        for animatronic in self.update_animatronics:
            animatronic.tick(event)
        for system in self.systems.values():
            system.tick(event)
        for button in self.buttons:
            button.tick(event)
        self.office.tick(event)
        self.tick(event)

    def global_draw(self):
        self.office.draw()
        for system in self.systems.values():
            system.draw()
        for animatronic in self.animatronics:
            animatronic.draw()
        for button in self.buttons:
            button.draw()

    def kill(self):
        if not self._win:
            self._killed = True
            self.stop_timer()

    def stop_timer(self):
        pass



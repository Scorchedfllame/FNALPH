from .office import Office
from .systems import Cameras, Vents
from AppData.GameData.constants import *
from .buttons import *
import pygame


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
                             self.events['camera_down_events'])
        self.buttons.append(camera_flick)

    def start(self):
        pass

    def global_tick(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
        for animatronic in self.update_animatronics:
            animatronic.tick(event)
        for system in self.systems.values():
            system.tick(event)
        for button in self.buttons:
            button.tick()

    def global_draw(self):
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



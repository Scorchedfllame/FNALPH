from gameplay.office import Office
from gameplay.systems import Cameras, Vents
from AppData.GameData.constants import *
from gameplay.buttons import *
import pygame
from AppData.GameData.constants import *


class Game:
    def __init__(self):
        self.timer = 0
        self.power = 100
        self.power_remaining = 100000
        self.power_usage = 1
        self.utils = {}
        self.animatronics = []
        self.update_animatronics = []
        self.systems = {"Cameras": Cameras()}
        self.buttons = []
        self.POWER_DIFFICULTY = 7
        self.GLOBAL_FONT = pygame.font.SysFont('Arial', 30, True)
        self.office = Office()
        self.events = self.init_events()
        self.init_buttons()
        self._win = False
        self._killed = False

    @staticmethod
    def init_events() -> dict:
        camera_up_event = pygame.event.Event(CAMERA_FLIPPED_UP)
        camera_down_event = pygame.event.Event(CAMERA_FLIPPED_DOWN)
        return {"camera_up_event": camera_up_event, "camera_down_event": camera_down_event}

    def init_buttons(self):
        screen = pygame.display.get_surface()
        flick_button = pygame.image.load('resources/ui/flick.png').convert_alpha()
        flick_button = pygame.transform.scale(flick_button, (600, 100))
        camera_flick = Flick(flick_button,
                             (int(screen.get_size()[0]/4), (screen.get_size()[1]) - 100),
                             self.events['camera_up_event'],
                             self.events['camera_down_event'],
                             draw_type='center')
        self.buttons.append(camera_flick)

    def start(self):
        pygame.time.set_timer(UPDATE_POWER, 100)

    def update_power(self):
        self.power_usage = self.get_power_usage()
        self.power_remaining -= self.POWER_DIFFICULTY * (2 ** self.power_usage)
        self.power = round(self.power_remaining / 1000)
        if self.power_remaining <= 0:
            pygame.event.post(BLACKOUT)

    def get_power_usage(self) -> int:
        power_usage = 1
        power_usage += self.office.get_power_usage()
        for system in self.systems.values():
            if system.active:
                power_usage += 2
        print(power_usage)
        return power_usage

    def tick(self, event: pygame.event.Event):
        if event.type == UPDATE_POWER:
            self.update_power()

    def global_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
        self.office.frame()

    def global_draw(self):
        screen = pygame.display.get_surface()
        self.office.draw()
        for system in self.systems.values():
            system.draw()
        for animatronic in self.animatronics:
            animatronic.draw()
        for button in self.buttons:
            button.draw()
        self.draw_power(screen)

    def draw_power(self, screen):
        self.draw_power_percentage(screen)
        self.draw_power_percentage(screen)

    def draw_power_usage(self, surface):
        print(self.power_usage)
        for i in range(self.power_usage):
            pygame.draw.rect(surface, 'red', pygame.Rect(5*i + 5, surface.get_height() - 35, 15, 30))

    def draw_power_percentage(self, surface):
        text = self.GLOBAL_FONT.render(str(self.power), True, 'White')
        surface.blit(text, (0, 0))

    def kill(self):
        if not self._win:
            self._killed = True
            self.stop_timer()

    def stop_timer(self):
        pass



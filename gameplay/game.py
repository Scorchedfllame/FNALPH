from gameplay.office import Office
from gameplay.systems import Cameras
from gameplay.power import PowerManager
from gameplay.buttons import *
from data.game.constants import *


class Game:
    def __init__(self):
        self.timer = 0
        self.power_manager = PowerManager()
        self.utils = {}
        self.animatronics = []
        self.systems = {"Cameras": Cameras()}
        self.buttons = []
        self.GLOBAL_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 55)
        self.BIGGER_GLOBAL_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 65)
        self.office = Office()
        self.events = self.init_events()
        self.init_buttons()
        self.debugger = True
        self._win = False
        self._killed = False

    @staticmethod
    def init_events() -> dict:
        camera_up_event = pygame.event.Event(CAMERA_FLIPPED_UP)
        camera_down_event = pygame.event.Event(CAMERA_FLIPPED_DOWN)
        return {"camera_up_event": camera_up_event, "camera_down_event": camera_down_event}

    def init_buttons(self):
        screen = pygame.display.get_surface()
        flick_button = pygame.image.load('resources/ui/buttons/camera_flick.png').convert_alpha()
        camera_flick = Flick(flick_button,
                             (int(screen.get_width()/2), screen.get_height() - 25),
                             self.events['camera_up_event'],
                             self.events['camera_down_event'],
                             draw_type='midbottom',
                             scale=screen.get_width()/(screen.get_width()*1.2))
        self.buttons.append(camera_flick)

    def start(self):
        pygame.time.set_timer(UPDATE_POWER, 100)

    def get_power_usage(self) -> int:
        power_usage = 1
        power_usage += self.office.get_power_usage()
        for system in self.systems.values():
            if system.active:
                power_usage += 2
        return min(power_usage, 5)

    def tick(self, event: pygame.event.Event):
        if event.type == UPDATE_POWER:
            self.power_manager.update_power(self.get_power_usage())

    def resize(self):
        screen = pygame.display.get_surface()
        for i in self.buttons:
            i.resize((int(screen.get_width()/2), screen.get_height() - 25), screen.get_width()/(screen.get_width()*2))

    def global_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.WINDOWRESIZED:
                for system in self.systems.values():
                    system.resize()
                self.resize()
            for animatronic in self.animatronics:
                animatronic.tick(event)
            for system in self.systems.values():
                system.tick(event)
            for button in self.buttons:
                button.tick(event)
            self.office.tick(event)
            self.tick(event)
        self.office.frame()
        for system in self.systems.values():
            system.frame()

    def global_draw(self):
        screen = pygame.display.get_surface()
        self.office.draw()
        for system in self.systems.values():
            system.draw()
        for animatronic in self.animatronics:
            animatronic.draw()
        for button in self.buttons:
            button.draw(screen)
        self.power_manager.draw(screen)

    def kill(self):
        if not self._win:
            self._killed = True
            self.stop_timer()

    def stop_timer(self):
        pass

from .clock import Clock
from gameplay.office import Office
from gameplay.systems import Cameras
from gameplay.power import PowerManager
from gameplay.buttons import *
from gameplay import Bonnie, Chica, Lefty, Knight
from data.game.constants import *
import json
from data.saves.save import SaveManager
import random


class Game:
    def __init__(self, save_manager: SaveManager):
        self.save_manager = save_manager
        self.night = self.save_manager.load_data()['night']
        self.night_dict = self.get_night_dict()
        self.utils = {}
        self.systems = {"Cameras": Cameras()}
        self.buttons = []
        self.GLOBAL_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 55)
        self.BIGGER_GLOBAL_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 65)
        self.office = Office()
        self.animatronics = []
        self.night_data = self.night_dict[str(self.night)]
        animatronic_key = {"Bonnie": Bonnie, "Chica": Chica, "Lefty": Lefty, "Knight": Knight}
        for animatronic, data in self.night_data['animatronics'].items():
            self.animatronics.append(animatronic_key[animatronic](self, data['difficulty']))
        self.events = self.init_events()
        self.flick = self.init_flick()
        self.power_manager = PowerManager(self.night_data['power_time'])
        self.clock = Clock(self.night)
        self.status = 'playing'
        self.debugger = True
        self.active = True
        self._win = False
        self._killed = False
        self.end_function = 'next'
        self.jump_scare_sound = pygame.mixer.Sound('resources/sounds/jump_scare.mp3')
        self.jump_scare_sound.set_volume(0.3)
        self.victory_sound = pygame.mixer.Sound('resources/sounds/five-nights-at-freddys-6-am.mp3')
        self.kill_anim = None
        try:
            self.phone_call = pygame.mixer.Sound('resources/sounds/night_' + str(self.night) + '.mp3')
        except:
            self.phone_call = None

    def stop(self):
        pygame.time.set_timer(GAME_TIMER, 0)
        pygame.mixer.stop()
        for animatronic in self.animatronics:
            animatronic.stop()
        self.office.stop()
        self.save_manager.save_game()
        self.power_manager.stop()
        if self.night == 7:
            self.save_manager.data = {"night": 6}
        self.save_manager.save_game()
        for system in self.systems.values():
            system.stop()
        pygame.display.get_surface().fill('black')
        pygame.display.flip()

    def next_night(self):
        self.save_manager.save_game()

    @staticmethod
    def get_night_dict() -> dict:
        with open('data/game/nights.json', 'r') as f:
            return json.loads(f.read())

    @staticmethod
    def init_events() -> dict:
        camera_up_event = pygame.event.Event(CAMERA_FLIPPED_UP)
        camera_down_event = pygame.event.Event(CAMERA_FLIPPED_DOWN)
        return {"camera_up_event": camera_up_event, "camera_down_event": camera_down_event}

    def init_flick(self):
        screen = pygame.display.get_surface()
        flick_button = pygame.image.load('resources/ui/buttons/camera_flick.png').convert_alpha()
        camera_flick = Flick(flick_button,
                             (int(screen.get_width() * 2/5), screen.get_height() - 25),
                             self.events['camera_up_event'],
                             self.events['camera_down_event'],
                             draw_type='midbottom',
                             scale=screen.get_width()/(screen.get_width()*1.2))
        return camera_flick

    def start(self):
        self.power_manager.start()
        self.office.start()
        self.clock.start()
        for system in self.systems.values():
            system.start()
        for animatronic in self.animatronics:
            animatronic.start()
        if self.phone_call is not None:
            pygame.mixer.find_channel(True).play(self.phone_call)

    def get_power_usage(self) -> int:
        power_usage = 1
        power_usage += self.office.get_power_usage()
        for system in self.systems.values():
            if system.active:
                power_usage += 1
        return min(power_usage, 5)

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stop()
                self.active = False
                self.end_function = 'menu'
        if event.type == GAME_TIMER:
            self.victory_sound.fadeout(1000)
            self.active = False
            self.stop()
        if event.type == UPDATE_POWER:
            self.power_manager.update_power(self.get_power_usage())
        if event.type == KILL and self.status == 'playing':
            self.kill(event.animation)
        if event.type == WIN and self.status == 'playing':
            self.win()

    def resize(self):
        screen = pygame.display.get_surface()
        for i in self.buttons:
            i.resize((int(screen.get_width()/2), screen.get_height() - 25), screen.get_width()/(screen.get_width()*2))

    def blackout(self):
        pygame.mixer.stop()
        pygame.mixer.Sound('resources/sounds/power_off.mp3').play()
        self.office.image = pygame.image.load('resources/backgrounds/office_blackout.png').convert()
        self.office.image = pygame.transform.scale_by(self.office.image,
                                                      pygame.display.get_surface().get_height()/
                                                      self.office.image.get_size()[1])
        self.systems['Cameras'].activate_blackout()
        pygame.time.set_timer(pygame.event.Event(KILL, {'animation': self.animatronics[3].jumpscare}),
                              random.randint(5000, 40000))
        self.animatronics = []
        self.office.doors = []

    def kill(self, animation):
        self.kill_anim = animation
        self.kill_anim.play_forward()
        pygame.mixer.stop()
        self.stop()
        self.status = 'killed'
        self.end_function = 'menu'
        self.jump_scare_sound.play(maxtime=1000)
        pygame.time.set_timer(GAME_TIMER, 1000)

    def win(self):
        pygame.mixer.stop()
        self.save_manager.data = {"night": self.night + 1}
        self.stop()
        self.status = 'win'
        self.victory_sound.play(fade_ms=1000)
        pygame.time.set_timer(GAME_TIMER, int(self.victory_sound.get_length() * 1000) - 1000)

    def global_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                exit()
            if event.type == pygame.WINDOWRESIZED:
                for system in self.systems.values():
                    system.resize()
                self.power_manager.resize()
                self.resize()
            if event.type == BLACKOUT:
                self.blackout()
            if event.type == WIN:
                self.win()
            for animatronic in self.animatronics:
                animatronic.tick(event)
            for system in self.systems.values():
                system.tick(event)
            if not self.systems['Cameras'].blackout:
                self.flick.tick(event)
            self.office.tick(event)
            self.tick(event)
            self.clock.tick(event)
            if event.type == CLOCK:
                for animatronic in self.animatronics:
                    change_list = self.night_data['animatronics'][animatronic.name]['change']
                    for change in change_list:
                        if change[0] == self.clock.hour:
                            animatronic.update_aggression(change[1])
                            break
        self.office.frame()

    def global_draw(self):
        screen = pygame.display.get_surface()
        self.office.draw()
        for system in self.systems.values():
            system.draw()
        if not self.systems['Cameras'].blackout:
            self.flick.draw(screen)
        for button in self.buttons:
            button.draw(screen)
        self.power_manager.draw(screen)
        self.clock.draw(screen)
        if self.status == 'win':
            screen.fill('black')
            text = pygame.transform.scale_by(self.BIGGER_GLOBAL_FONT.render("6:00 AM", True, "white"), 3)
            rect = text.get_rect()
            rect.center = (screen.get_width()/2, screen.get_height()/2)
            screen.blit(text, rect)
        if self.kill_anim is not None:
            self.kill_anim.draw(screen)

    def update_animatronics(self):
        for animatronic in self.animatronics:
            animatronic.update_images()

    def stop_timer(self):
        pass

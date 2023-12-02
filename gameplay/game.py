from gameplay.office import Office
from gameplay.systems import Cameras
from gameplay.buttons import *
from AppData.GameData.constants import *


class Game:
    def __init__(self):
        self.timer = 0
        self.power = 100
        self.power_remaining = 100000
        self.power_usage = 1
        self.utils = {}
        self.animatronics = []
        self.systems = {"Cameras": Cameras()}
        self.buttons = []
        self.POWER_DIFFICULTY = 7
        self.GLOBAL_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 55)
        self.BIGGER_GLOBAL_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 65)
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
        return min(power_usage, 5)

    def tick(self, event: pygame.event.Event):
        if event.type == UPDATE_POWER:
            self.update_power()

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

    def global_draw(self):
        screen = pygame.display.get_surface()
        self.office.draw()
        for system in self.systems.values():
            system.draw()
        for animatronic in self.animatronics:
            animatronic.draw()
        for button in self.buttons:
            button.draw(screen)
        self.draw_power(screen)

    def draw_power(self, screen):
        self.draw_power_percentage(screen)
        self.draw_power_usage(screen)

    def draw_power_usage(self, surface):
        width = 25
        height = 40
        y_offset = 30
        padding = 3
        text = self.GLOBAL_FONT.render("Usage: ", True, 'white')
        text_rect = text.get_rect()
        text_rect.topleft = (y_offset,
                             surface.get_height() - (30 + height + padding + self.BIGGER_GLOBAL_FONT.size('100')[1]))
        surface.blit(text, text_rect)
        for i in range(self.power_usage):
            usage_bar = pygame.Rect(text_rect.midright[0] + i*(width + padding),
                                    text_rect.topright[1] - (text_rect.height - height)/2,
                                    width,
                                    height)
            shader = pygame.Rect(0, 0, int(width/4), height)
            shader.midright = usage_bar.midright
            if i <= 1:
                color = (35, 235, 31)
                shade_color = (16, 131, 27)
            elif i == 2:
                color = (255, 243, 0)
                shade_color = (225, 128, 9)
            else:
                color = (255, 35, 35)
                shade_color = (198, 0, 0)
            pygame.draw.rect(surface, color, usage_bar)
            pygame.draw.rect(surface, shade_color, shader)

    def draw_power_percentage(self, surface):
        screen_y = pygame.display.get_surface().get_height()

        # Get text
        power_left_text = self.GLOBAL_FONT.render(f"Power Left: ", True, 'White')
        power_percentage = self.BIGGER_GLOBAL_FONT.render(f"{self.power}", True, 'White')
        power_percent = self.GLOBAL_FONT.render(f"%", True, 'White')

        # Creating rectangles
        power_left_text_rect = power_left_text.get_rect()
        power_percentage_rect = power_percentage.get_rect()
        power_percent_rect = power_percent.get_rect()

        # Setting rectangles
        power_left_text_rect.bottomleft = (30, screen_y - 30)
        power_percentage_rect.bottomleft = power_left_text_rect.bottomright
        power_percent_rect.bottomleft = (power_percentage_rect.width + power_left_text_rect.bottomright[0],
                                         power_left_text_rect.bottomright[1])

        # Drawing
        surface.blit(power_left_text, power_left_text_rect)
        surface.blit(power_percentage, (power_percentage_rect.x, power_left_text_rect.y - 3))
        surface.blit(power_percent, power_percent_rect)

    def kill(self):
        if not self._win:
            self._killed = True
            self.stop_timer()

    def stop_timer(self):
        pass

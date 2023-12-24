from data.game.constants import *


class Clock:
    def __init__(self, night):
        self.night = night
        self.time = 12
        self.hour = 0
        self.HOUR_DURATION = 60
        self.HOUR_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 100)
        self.NIGHT_FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 50)
        self.active = True

    def start(self, night):
        self.night = night
        self.hour = 0
        self.time = 12
        pygame.time.set_timer(CLOCK, self.HOUR_DURATION * 1000)

    def update_time(self):
        if self.active:
            self.hour += 1
            self.time = int((self.hour - 1) % 12 + 1)
            if self.time == 6:
                pygame.event.post(pygame.event.Event(WIN))
                self.active = False

    def tick(self, event: pygame.event.Event):
        if event.type == CLOCK:
            self.update_time()

    def draw(self, screen: pygame.Surface):
        width = screen.get_width()
        render = self.HOUR_FONT.render(f"{self.time} AM", True, 'white')
        rect = render.get_rect()
        rect.topright = (width - 15, 15)
        screen.blit(render, rect)
        night = self.NIGHT_FONT.render(f"Night {self.night}", True, 'white')
        night_rect = night.get_rect()
        night_rect.topright = (width - 15, rect.height - 5)
        screen.blit(night, night_rect)


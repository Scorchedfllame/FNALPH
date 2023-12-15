from data.game.constants import *


class Clock:
    def __init__(self):
        self.time = 12
        self.hour = 0
        self.HOUR_DURATION = 10
        self.FONT = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 100)
        self.active = True

    def start(self):
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
        render = self.FONT.render(f"{self.time} AM", True, 'white')
        screen.blit(render, (width-render.get_width(), 0))

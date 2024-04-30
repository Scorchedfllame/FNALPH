from data.game.constants import *
from math import ceil


class PowerManager:
    def __init__(self, power_penalty):
        self.font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 55)
        self.large_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 65)
        self.power_penalty = power_penalty
        self.usage = Usage(self.font, self.large_font)

        self.DIFFICULTY = None
        self.active = None
        self.percentage = None
        self.power_remaining = None

    def start(self):
        # set back to 10 when done testing
        self.DIFFICULTY = 10
        self.active = True
        self.percentage = 100
        self.power_remaining = 100000

        self.usage.start()
        pygame.time.set_timer(UPDATE_POWER, 100)
        pygame.time.set_timer(POWER_PENALTY, self.power_penalty)

    def stop(self):
        self.active = False

        pygame.time.set_timer(UPDATE_POWER, 0)
        pygame.time.set_timer(POWER_PENALTY, 0)

    def draw(self, surface):
        if self.active:
            self.draw_power_percentage(surface)
            self.usage.draw(surface)

    def resize(self):
        self.usage.resize()

    def update_power(self, usage: int):
        if self.active:
            self.usage.usage = usage
            self.power_remaining = max(self.power_remaining - self.DIFFICULTY * usage, 0)
            self.percentage = ceil(self.power_remaining / 1000)
            if self.power_remaining <= 0:
                pygame.event.post(pygame.event.Event(BLACKOUT))
                self.active = False

    def draw_power_percentage(self, surface):
        LINEUP_OFFSET = 5
        screen_y = pygame.display.get_surface().get_height()

        # Get text
        power_left_text = self.font.render(f"Power Left: ", True, 'White')
        power_percentage = self.large_font.render(f"{self.percentage}", True, 'White')
        power_percent = self.font.render(f"%", True, 'White')

        # Creating rectangles
        power_left_text_rect = power_left_text.get_rect()
        power_percentage_rect = power_percentage.get_rect()
        power_percent_rect = power_percent.get_rect()

        # Setting rectangles
        power_left_text_rect.bottomleft = (30, screen_y - 15)
        power_percentage_rect.bottomleft = power_left_text_rect.bottomright
        power_percent_rect.bottomleft = (power_percentage_rect.width + power_left_text_rect.bottomright[0],
                                         power_left_text_rect.bottomright[1])

        # Drawing
        surface.blit(power_left_text, power_left_text_rect)
        surface.blit(power_percentage, (power_percentage_rect.x, power_left_text_rect.y - LINEUP_OFFSET))
        surface.blit(power_percent, power_percent_rect)


class Usage:
    def __init__(self, font, large_font):
        self.large_font = large_font
        self.width = 25
        self.height = 40
        self.y_offset = 30
        self.padding = 3
        self.text = font.render("Usage: ", True, 'white')
        self.text_rect = self.text.get_rect()
        self.resize()

        self.usage = None

    def start(self):
        self.usage = 1

    def draw(self, surface):
        surface.blit(self.text, self.text_rect)
        self.draw_ghost(surface)
        self.draw_color(surface)

    def resize(self):
        screen = pygame.display.get_surface()
        x_offset = (15 + self.height + self.padding + self.large_font.size('100')[1])
        self.text_rect.topleft = (self.y_offset,
                                  screen.get_height() - x_offset)

    def draw_ghost(self, surface):
        for i in range(5):
            usage_bar = pygame.Rect(self.text_rect.midright[0] + i*(self.width + self.padding),
                                    self.text_rect.topright[1] - (self.text_rect.height - self.height)/2,
                                    self.width,
                                    self.height)
            color = (15, 16, 16, 150)
            draw = pygame.surface.Surface(usage_bar.size, pygame.SRCALPHA)
            pygame.draw.rect(draw, color, draw.get_rect())
            surface.blit(draw, usage_bar)

    def draw_color(self, surface):
        for i in range(self.usage):
            usage_bar = pygame.Rect(self.text_rect.midright[0] + i*(self.width + self.padding),
                                    self.text_rect.topright[1] - (self.text_rect.height - self.height)/2,
                                    self.width,
                                    self.height)
            shader = pygame.Rect(0, 0, int(self.width/4), self.height)
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

    def __int__(self):
        return self.usage

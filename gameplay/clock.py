from data.game.constants import *


class Clock:
    def __init__(self):
        self.time = 12
        self.seconds_passed = 0
        self.HOUR_DURATION = 2

    def update_time(self):
        self.seconds_passed += 1
        self.time = int((((self.seconds_passed / self.HOUR_DURATION) // 1) - 1) % 12 + 1)

    def tick(self, event: pygame.event.Event):
        if event.type == CLOCK:
            self.update_time()

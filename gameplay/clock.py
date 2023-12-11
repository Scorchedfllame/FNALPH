from data.game.constants import *


class Clock:
    def __init__(self):
        self.time = 12
        self.seconds_passed = 0
        self.HOUR_DURATION = 2
        self.active = True

    def update_time(self):
        if self.active:
            self.seconds_passed += 1
            self.time = int((((self.seconds_passed / self.HOUR_DURATION) // 1) - 1) % 12 + 1)
            if self.time >= 6:
                pygame.event.post(pygame.event.Event(WIN))
                self.active = False

    def tick(self, event: pygame.event.Event):
        if event.type == CLOCK:
            self.update_time()

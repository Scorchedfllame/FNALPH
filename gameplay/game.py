from .office import Office
import pygame


class Game:
    def __init__(self):
        self.timer = 0
        self.utils = {}
        self.animatronics = []
        self.update_animatronics = []
        self.systems = {}
        self.office = Office()
        self._win = False
        self._killed = False

    def start(self):
        pass

    def global_tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            for animatronic in self.update_animatronics:
                animatronic.tick(event)

    def kill(self):
        if not self._win:
            self._killed = True
            self.stop_timer()

    def stop_timer(self):
        pass



class Game:
    def __init__(self):
        self.timer = 0
        self.utils = {}
        self.animatronics = []
        self.update_animatronics = []
        self.systems = {}
        self._win = False
        self._killed = False

    def start(self):
        pass

    def global_update(self):
        for animatronic in self.update_animatronics:
            animatronic.update()

    def kill(self):
        if not self._win:
            self._killed = True
            self.stop_timer()

    def stop_timer(self):
        pass



class Game:
    def __init__(self):
        self.timer = 0
        self.animatronics = []
        self.systems = []
        self.win = False
        self.killed = False

    def global_update(self):
        for animatronic in self.animatronics:
            animatronic.update()


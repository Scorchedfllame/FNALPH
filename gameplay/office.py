class Office:
    def __init__(self):
        self.door_left = False
        self.door_right = False
        self.vent_door = False
        self.light_left = False
        self.light_right = False
        self.active = True
        self._locked = False

    def lock(self):
        self._locked = True

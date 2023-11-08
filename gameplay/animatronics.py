import json


class Jumpscare:
    def __init__(self, image_path: str, kill: bool, length: float, effect: None):
        self.image_path = image_path
        self.kill = kill
        self.length = length
        self.effect = effect

    @classmethod
    def load_data(cls, path: str) -> None:
        with open(path, 'r') as f:
            jumpscares = json.loads(f.read())
            for jumpscare in jumpscares:
                cls.__init__(jumpscare[0], jumpscare[1], jumpscare[2])


class Animatronic:
    def __init__(self, name: str, image_path: str, description: str, jumpscare: Jumpscare = None):
        self.name = name
        self.image_path = image_path
        self.description = description
        self.jumpscare = jumpscare

    @classmethod
    def load_data(cls, path: str) -> None:
        animatronic_list = []
        with open(path, 'r') as f:
            animatronics = json.loads(f.read())
            for animatronic in animatronics:
                animatronic_list.append(cls(animatronic[0], animatronic[1], animatronic[2]))

    def start_jumpscare(self):
        if self.jumpscare is not None:
            pass


class CameraAnimatronic(Animatronic):
    def __init__(self, name: str, image_path: str, description: str, camera_index: int):
        super().__init__(name, image_path, description)
        self.camera_index = camera_index


import json
from .game import Game
from .buttons import Button


class System:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path
        self.buttons = []


class Camera:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path
        self.active = False
        self._buttons = []
        self._shocked = False

    @property
    def buttons(self):
        return self._buttons

    def add_button(self, button: Button):
        self._buttons.append(button)

    def shock(self, game: Game):
        self._shocked = True
        game.global_update()
        self._shocked = False


class Cameras(System):
    def __init__(self):
        super().__init__("Cams System", 'resources/background/test.png')
        self._camera_list = Cameras.load_cameras('Appdata/GameData/cameras.json')
        self.enabled = True
        self.active = False

    @staticmethod
    def load_cameras(load_path: str) -> list[Camera]:
        cameras = []
        with open(load_path, 'r') as f:
            cameras_list = json.load(f)
            for camera in cameras_list:
                cameras.append(Camera(camera[0], camera[1]))
            return cameras

    def disable_cameras(self):
        for camera in self.camera_list:
            camera.active = False

    def activate_camera(self, camera_index: int):
        self.disable_cameras()
        self.camera_list[camera_index].active = True


class Vents(System):
    def __init__(self):
        super().__init__("Vent System", 'resources/background/test.png')


class Repairs(System):
    def __init__(self, game: Game):
        super().__init__("Maintenance Panel", 'resources/background/test.png')


class Lure:
    def __init__(self, position: tuple[int], radius: int):
        self.position = position
        self.radius = radius


class Ducts(System):
    def __init__(self):
        super().__init__("Duct System", 'resources/background/test.png')
        self.lures = []
        self.open_duct = 0
        self.closed_duct = 1

    def open_ducts(self, duct: int(1 | 0)) -> None:
        self.open_duct = duct
        self.closed_duct = int(not duct)

    def new_lure(self, position: tuple[int], radius: int) -> Lure:
        new_lure = Lure(position, radius)
        self.lures.append(new_lure)
        return new_lure

    def del_lure(self, index: int) -> Lure:
        del_lure = self.lures[index]
        del self.lures[index]
        return del_lure

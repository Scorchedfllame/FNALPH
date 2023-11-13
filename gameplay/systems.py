import json
from .game import Game
from .buttons import Button
from .animatronics import Animatronic
import pygame


class System:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path
        self.buttons = []


class Camera:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path
        self.background = pygame.image.load(self.background_path).convert()
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

    def draw(self, screen, animatronics: list[Animatronic]) -> None:
        screen.blit(self.background)
        for animatronic in animatronics:
            animatronic.draw(screen)


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
        for camera in self._camera_list:
            camera.active = False

    def activate_camera(self, camera_index: int):
        self.disable_cameras()
        self._camera_list[camera_index].active = True

    def draw_cameras(self, screen, game):
        for camera in self._camera_list:
            if camera.active:
                camera.draw(screen, game.animatronics)


class Vents(System):
    def __init__(self):
        super().__init__("Vent System", 'resources/background/test.png')

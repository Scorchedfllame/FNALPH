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

    @classmethod
    def generate_cameras(cls, cameras: list) -> list:
        final = []
        for name, background_path in cameras:
            final.append(cls(name, background_path))
        return final

    @property
    def buttons(self):
        return self._buttons

    def add_button(self, button: Button):
        self._buttons.append(button)

    def draw(self, screen, animatronics: list[Animatronic]) -> None:
        screen.blit(self.background)
        for animatronic in animatronics:
            animatronic.draw(screen)


class Cameras(System):
    def __init__(self):
        super().__init__("Cams System", 'resources/background/test.png')
        self._camera_list = Camera.generate_cameras(self.load_data('objects'))
        self.enabled = True
        self.active = False
        camera_buttons = self.load_data('Camera_Buttons')
        camera_font = pygame.font.Font('arial', 32)
        for i in range(len(self._camera_list)):
            text = camera_font.render(self._camera_list[i].name, True, 'white')
            self.buttons.append(Button(text, tuple(camera_buttons['Positions'][str(i)])))

    @staticmethod
    def load_data(data: str) -> any:
        with open('Appdata/GameData/cameras.json', 'r') as f:
            cameras_list = json.load(f)
            return cameras_list[data]

    def disable_cameras(self):
        for camera in self._camera_list:
            camera.active = False

    def activate_camera(self, camera_index: int):
        self.disable_cameras()
        self._camera_list[camera_index].active = True

    def draw_cameras(self, game):
        for camera in self._camera_list:
            if camera.active:
                camera.draw(game.animatronics)
        for button in self.buttons:
            button.draw()

    def tick(self, event: pygame.event.Event):
        if self.active:
            self.draw_cameras()
            for button in self.buttons:
                button.tick(event)


class Vents(System):
    def __init__(self):
        super().__init__("Vent System", 'resources/background/test.png')

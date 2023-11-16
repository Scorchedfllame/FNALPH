import json
from .buttons import Button
from .animatronics import Animatronic
from AppData.GameData.constants import *
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

    def draw(self) -> None:
        if self.active:
            pygame.display.get_surface().blit(self.background, (0, 10))


class Cameras(System):
    def __init__(self):
        super().__init__("Cams System", 'resources/background/test.png')
        self._camera_list = Camera.generate_cameras(self.load_data('objects'))
        self.enabled = True
        self.active = False
        self._last_camera = 0
        self.buttons = []
        self.generate_buttons()
        self.activate_camera_event = pygame.event.Event(ACTIVATE_CAMERA)

    @staticmethod
    def load_data(data: str) -> any:
        with open('Appdata/GameData/cameras.json', 'r') as f:
            cameras_list = json.load(f)
            return cameras_list[data]

    def generate_buttons(self):
        camera_buttons = self.load_data('Camera_Buttons')
        camera_font = pygame.font.SysFont('Arial', 32)
        for i in range(len(self._camera_list)):
            text = camera_font.render(self._camera_list[i].name, True, 'white')
            pos = tuple(camera_buttons['Positions'][str(i)])
            self.buttons.append(Button(text,
                                pos,
                                self.activate_camera,
                                camera_index=i))

    def activate(self):
        self.active = True
        self.activate_camera(self._last_camera)

    def deactivate(self):
        self.active = False
        self._last_camera = self.get_active_camera()
        self.disable_cameras()

    def disable_cameras(self):
        for camera in self._camera_list:
            camera.active = False

    def get_active_camera(self):
        for i in range(len(self._camera_list)):
            if self._camera_list[i].active:
                return i

    def activate_camera(self, camera_index: int):
        self.disable_cameras()
        camera = self._camera_list[camera_index]
        camera.active = True
        self._last_camera = camera_index

    def draw(self):
        if self.active:
            for camera in self._camera_list:
                camera.draw()
            for button in self.buttons:
                button.draw()

    def tick(self, event: pygame.event.Event):
        if event.type == CAMERA_FLIPPED_DOWN:
            self.deactivate()
        if event.type == CAMERA_FLIPPED_UP:
            self.activate()
        for button in self.buttons:
            button.tick(event)


class Vents(System):
    def __init__(self):
        super().__init__("Vent System", 'resources/background/test.png')

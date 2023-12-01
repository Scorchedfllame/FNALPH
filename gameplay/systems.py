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
        self.font = pygame.sysfont.SysFont('Arial', 30)
        self.font_color = 'White'
        self.FONT_POS = (200, 300)
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

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def add_button(self, button: Button):
        self._buttons.append(button)

    def draw(self) -> None:
        if self.active:
            screen = pygame.display.get_surface()
            screen.blit(self.background, (0, 10))
            text = self.font.render(self.name, True, self.font_color)
            screen.blit(text, self.FONT_POS)


class Cameras(System):
    def __init__(self):
        super().__init__("Cams System", 'resources/background/test.png')
        self._camera_list = Camera.generate_cameras(self.load_data('Camera_Buttons')['objects'])
        self.font = pygame.font.SysFont('Arial', 32)
        self.enabled = True
        self.active = False
        self._last_camera = 0
        self.active_icons = []
        self.inactive_icons = []
        self.generate_buttons()
        self.activate_camera_event = pygame.event.Event(ACTIVATE_CAMERA)

    def load_camera_buttons(self, data):
        icons = data["Icons"]
        for icon in icons:
            self.active_icons.append(pygame.image.load(icon['Active']).convert())
            self.inactive_icons.append(pygame.image.load(icon['Inactive']).convert())

    @staticmethod
    def load_data(data: str) -> any:
        with open('Appdata/GameData/cameras.json', 'r') as f:
            cameras_list = json.load(f)
            return cameras_list[data]

    def generate_buttons(self):
        camera_buttons = self.load_data('Camera_Buttons')
        self.load_camera_buttons(camera_buttons)
        for i in range(len(self._camera_list)):
            pos = tuple(camera_buttons['Positions'][str(i)])
            icon = pygame.transform.scale_by(self.inactive_icons[i], .5)
            self.buttons.append(Button(icon,
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
        for i, camera in enumerate(self._camera_list):
            self.buttons[i].change_surface(self.inactive_icons[i])
            camera.deactivate()

    def get_active_camera(self):
        for i in range(len(self._camera_list)):
            if self._camera_list[i].active:
                return i

    def activate_camera(self, camera_index: int):
        self.disable_cameras()
        camera = self._camera_list[camera_index]
        self.buttons[camera_index].change_surface(self.active_icons[camera_index])
        camera.activate()
        self._last_camera = camera_index

    def draw(self):
        if self.active:
            for i, camera in enumerate(self._camera_list):
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

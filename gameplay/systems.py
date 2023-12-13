import json
from .buttons import Button
from .animatronics import Animatronic
from data.game.constants import *
import pygame
import math


class System:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path
        self.buttons = []


class Camera:
    def __init__(self, name: str, background_path: str):
        self.name = name
        self.background_path = background_path
        screen = pygame.display.get_surface()
        self.background = pygame.image.load(self.background_path).convert()
        self.background = pygame.transform.scale_by(self.background, screen.get_height()/self.background.get_height())
        self.active = False
        self.font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 60)
        self.font_color = 'White'
        self.font_pos = [0, 0]
        self.resize()
        self._buttons = []

    def resize(self):
        screen = pygame.display.get_surface()
        self.font_pos[0] = screen.get_width() * 7/12
        self.font_pos[1] = int(screen.get_width()/2 * (850/1290) + screen.get_height())

    @classmethod
    def generate_cameras(cls, cameras: list[dict]) -> list:
        final = []
        for camera in cameras:
            final.append(cls(camera['name'], camera['background']))
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

    def draw(self, surface, offset: int = 0) -> None:
        if self.active:
            surface.blit(self.background, (offset, 0))
            text = self.font.render(self.name, True, self.font_color)
            surface.blit(text, tuple(self.font_pos))


class Cameras(System):
    def __init__(self):
        super().__init__("Cams System", 'resources/background/test.png')
        self._camera_list = Camera.generate_cameras(self.load_data('cameras'))
        self.map_image = self.init_images()
        self.font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 90)
        self.enabled = True
        self.active = False
        self._last_camera = 0
        self.MAX_ROTATION = 90
        self.active_icons = []
        self.inactive_icons = []
        self.generate_buttons()
        pygame.time.set_timer(pygame.event.Event(CAMERA_ROTATION), 3000)
        self.current_rotation = 0
        self.rotation_cycle = 0

    @staticmethod
    def init_images():
        screen = pygame.display.get_surface()
        map_image = pygame.image.load('resources/ui/map.png').convert_alpha()
        scale_factor = Cameras.get_scaler(screen, map_image)
        map_image = pygame.transform.scale_by(map_image, scale_factor)
        return map_image

    def load_camera_buttons(self, data: list[dict]):
        active_path = "resources/ui/buttons/camera_icons/active"
        inactive_path = "resources/ui/buttons/camera_icons/inactive"
        for camera in data:
            self.active_icons.append(pygame.image.load(active_path + "/" + camera['label'] + ".png").convert())
            self.inactive_icons.append(pygame.image.load(inactive_path + "/" + camera['label'] + ".png").convert())

    @staticmethod
    def load_data(data: str) -> any:
        with open('data/game/cameras.json', 'r') as f:
            cameras_list = json.load(f)
            return cameras_list[data]

    def resize(self):
        self.map_image = self.init_images()
        camera_data = self.load_data('cameras')
        for i in range(len(self._camera_list)):
            self._camera_list[i].resize()
            x, y = tuple(camera_data[i]["position"])
            regular_size = (1290, 655)
            rect = self.map_image.get_rect()
            rect.bottomright = pygame.display.get_surface().get_size()
            rect_x, rect_y = rect.topleft
            pos_x = rect_x + (rect.width * (x / regular_size[0]))
            pos_y = rect_y + (rect.height * (y / regular_size[1]))
            self.buttons[i].resize((pos_x, pos_y), pygame.display.get_surface().get_width() / 4500)

    def generate_buttons(self):
        camera_buttons = self.load_data('cameras')
        self.load_camera_buttons(camera_buttons)
        for i in range(len(self._camera_list)):
            self.buttons.append(Button(self.inactive_icons[i],
                                (0, 0),
                                self.activate_camera,
                                camera_index=i))
        self.resize()

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

    @staticmethod
    def get_scaler(surface: pygame.Surface, rect: pygame.Surface | pygame.Rect):
        return surface.get_width()/(2*rect.get_width())

    def draw_map(self, surface: pygame.surface.Surface):
        rect = self.map_image.get_rect()
        rect.bottomright = surface.get_size()
        surface.blit(self.map_image, rect)

    @staticmethod
    def get_pos_from_rot(screen_x, image_x, rotation, max_rotation):
        # normalization 0-1
        normalized = (rotation + max_rotation)/(2*max_rotation)

        # turn into other stuff
        return normalized * (screen_x - image_x)

    def draw(self):
        if self.rotation_cycle == 0:
            self.current_rotation += 1
        elif self.rotation_cycle == 2:
            self.current_rotation -= 1
        self.current_rotation = max(-self.MAX_ROTATION, min(self.current_rotation, self.MAX_ROTATION))
        if self.active:
            screen = pygame.display.get_surface()
            for i, camera in enumerate(self._camera_list):
                offset = self.get_pos_from_rot(screen.get_width(),
                                               camera.background.get_width(),
                                               self.current_rotation,
                                               self.MAX_ROTATION)
                camera.draw(screen, offset)
            self.draw_map(screen)
            for button in self.buttons:
                button.draw(screen)

    def tick(self, event: pygame.event.Event):
        for button in self.buttons:
            button.tick(event)
        if event.type == CAMERA_FLIPPED_UP:
            self.activate()
        if event.type == CAMERA_FLIPPED_DOWN:
            self.deactivate()
        if event.type == CAMERA_ROTATION:
            self.rotation_cycle += 1
            if self.rotation_cycle == 4:
                self.rotation_cycle = 0
            match self.rotation_cycle:
                case 0:
                    self.current_rotation = -90
                case 1:
                    self.current_rotation = 90
                case 2:
                    self.current_rotation = 90
                case 3:
                    self.current_rotation = -90


class Vents(System):
    def __init__(self):
        super().__init__("Vent System", 'resources/background/test.png')

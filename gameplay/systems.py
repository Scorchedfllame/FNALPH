import json
import random

from .buttons import Button
from data.game.constants import *
import pygame
from .animation import Animator
import os


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
        self._background = self.background.__copy__()
        self.active = False
        self.font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 70)
        self.glitch_sound = pygame.mixer.Sound('resources/sounds/Garble1.mp3')
        self.glitch_sound.set_volume(.5)
        self.font_color = 'White'
        self.font_pos = [0, 0]
        self.resize()
        self._buttons = []
        self.glitch_timer = 0
        self.MAX_GLITCH_TIMER = self.glitch_sound.get_length() * 60
        self.glitch = False

    def start(self):
        self.glitch = False
        self.glitch_timer = 0
        self.active = False
        self.glitch_sound.set_volume(.5)
        self.reset_background()

    def small_glitch(self):
        pygame.mixer.find_channel().play(self.glitch_sound)
        self.glitch = True

    def reset_background(self):
        self.background = self._background.__copy__()

    def resize(self):
        screen = pygame.display.get_surface()
        self.font_pos[0] = int(screen.get_width() * 6/12)
        self.font_pos[1] = int(screen.get_height() * 8/15)

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
        self.glitch_sound.set_volume(.5)

    def deactivate(self):
        self.active = False
        self.glitch_sound.set_volume(0)

    def add_button(self, button: Button):
        self._buttons.append(button)

    def draw(self, surface, offset: int = 0) -> None:
        if self.glitch:
            self.glitch_timer += 1
            if self.glitch_timer > self.MAX_GLITCH_TIMER:
                self.glitch_timer = 0
                self.glitch = False
        if self.active:
            surface.blit(self.background, (offset, 0))
            if self.glitch:
                black = pygame.Surface(surface.get_size())
                black.fill('black')
                surface.blit(black, (0, 0))

    def draw_text(self, surface: pygame.Surface):
        if self.active:
            text = self.font.render(self.name, True, self.font_color)
            surface.blit(text, tuple(self.font_pos))


class Cameras(System):
    def __init__(self):
        super().__init__("Cams System", 'resources/background/test.png')
        self.animation = Animator(pygame.image.load('resources/animations/Camera_Flip.png').convert_alpha(),
                                  pygame.rect.Rect(0, 0, 1920, 1080),
                                  speed=.5)
        self.camera_list = Camera.generate_cameras(self.load_data('cameras'))
        self.map_image = self.init_images()
        self.font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 90)
        self.enabled = True
        self.active = False
        self.blackout = False
        self._last_camera = 0
        self.MAX_ROTATION = 90
        self.active_icons = []
        self.inactive_icons = []
        self.generate_buttons()
        self.current_rotation = 0
        self.rotation_cycle = 0
        self.camera_switch_sound = pygame.mixer.Sound('resources/sounds/static.mp3')
        self.camera_switch_sound.set_volume(.25)
        self.camera_pan_sound = pygame.mixer.Sound('resources/sounds/camera_pan.mp3')
        self.static = []
        for frame in os.listdir('resources/animations/static/'):
            image = pygame.image.load(f'resources/animations/static/{frame}').convert_alpha()
            self.static.append(image)
        self.record_icon = RecordIcon((30, 30), 7, 3)

    @staticmethod
    def init_images():
        screen = pygame.display.get_surface()
        map_image = pygame.image.load('resources/ui/map1.png').convert_alpha()
        scale_factor = Cameras.get_scaler(screen, map_image)
        map_image = pygame.transform.scale_by(map_image, scale_factor)
        map_image.set_alpha(200)
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
        for i in range(len(self.camera_list)):
            self.camera_list[i].resize()
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
        for i in range(len(self.camera_list)):
            self.buttons.append(Button(self.inactive_icons[i],
                                (0, 0),
                                self.activate_camera,
                                camera_index=i))
        self.resize()

    def activate(self):
        self.activate_camera(self._last_camera)
        self.active = True
        self.animation.play_forward()

    def activate_blackout(self):
        self.blackout = True
        pygame.event.post(pygame.event.Event(CAMERA_FLIPPED_DOWN))

    def deactivate(self):
        self.active = False
        self._last_camera = self.get_active_camera()
        self.disable_cameras()
        self.animation.play_backward()

    def disable_cameras(self):
        for i, camera in enumerate(self.camera_list):
            self.buttons[i].change_surface(self.inactive_icons[i])
            camera.deactivate()

    def get_active_camera(self):
        for i in range(len(self.camera_list)):
            if self.camera_list[i].active:
                return i

    def activate_camera(self, camera_index: int):
        if self.active:
            self.camera_switch_sound.play(fade_ms=100)
            self.camera_switch_sound.fadeout(200)
        self.disable_cameras()
        camera = self.camera_list[camera_index]
        self.buttons[camera_index].change_surface(self.active_icons[camera_index])
        camera.activate()
        self._last_camera = camera_index

    @staticmethod
    def get_scaler(surface: pygame.Surface, rect: pygame.Surface | pygame.Rect):
        return surface.get_width()/(2.1*rect.get_width())

    def draw_map(self, surface: pygame.surface.Surface):
        rect = self.map_image.get_rect()
        rect.bottomright = (surface.get_width() - 20, surface.get_height() - 25)
        font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 100)
        self.map_image.blit(font.render("YOU", True, "white"), (640, 530))
        surface.blit(self.map_image, rect)

    @staticmethod
    def get_pos_from_rot(screen_x, image_x, rotation, max_rotation):
        # normalization 0-1
        normalized = (rotation + max_rotation)/(2*max_rotation)
        # turn into other stuff
        return normalized * (screen_x - image_x)

    def draw(self):
        if self.active:
            self.camera_pan_sound.set_volume(.2)
        else:
            self.camera_pan_sound.set_volume(0)
        if self.rotation_cycle == 0:
            self.current_rotation += 1
        elif self.rotation_cycle == 2:
            self.current_rotation -= 1
        self.current_rotation = max(-self.MAX_ROTATION, min(self.current_rotation, self.MAX_ROTATION))
        screen = pygame.display.get_surface()
        if self.active and not self.animation.active:
            for i, camera in enumerate(self.camera_list):
                offset = self.get_pos_from_rot(screen.get_width(),
                                               camera.background.get_width(),
                                               self.current_rotation,
                                               self.MAX_ROTATION)
                camera.draw(screen, offset)
            self.draw_static(screen, self.static)
            for i in self.camera_list:
                i.draw_text(screen)
            self.draw_map(screen)
            for button in self.buttons:
                button.draw(screen)
            pygame.draw.rect(screen, (170, 170, 170), pygame.rect.Rect(10, 10, 1900, 1060), 2, 1)
            self.record_icon.draw(screen)
        self.animation.draw(screen)

    @staticmethod
    def draw_static(screen: pygame.surface.Surface, static):
        frame = random.randint(0, len(static) - 1)
        screen.blit(static[frame], (0, 0))
        screen.blit(static[(frame + 1) % len(static)], (0, 0))

    def start(self):
        self.current_rotation = 0
        self.animation.start()
        for camera in self.camera_list:
            camera.start()
        self.disable_cameras()
        self.active = False
        pygame.time.set_timer(pygame.event.Event(CAMERA_ROTATION), 4000)
        self._last_camera = 0

    def stop(self):
        self.active = False
        pygame.time.set_timer(CAMERA_ROTATION, 0)

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
                    self.camera_pan_sound.play(maxtime=3300)
                case 1:
                    self.camera_pan_sound.set_volume(0)
                    self.current_rotation = 90
                case 2:
                    self.current_rotation = 90
                    self.camera_pan_sound.play(maxtime=3300)
                case 3:
                    self.camera_pan_sound.set_volume(0)
                    self.current_rotation = -90


class RecordIcon:
    def __init__(self, pos: tuple[int, int], radius: int, flash_time: float):
        self.pos = pos
        self.radius = radius
        self.surface = self.create_surface()
        self.frame = 0
        self.MAX_FRAMES = flash_time * 60

    def create_surface(self) -> pygame.Surface:
        size = self.radius * 2
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, "red", (size // 2, size // 2), self.radius)
        surface = pygame.transform.scale_by(surface, 20/self.radius)
        return surface

    def draw(self, screen):
        self.frame = (self.frame + 1) % self.MAX_FRAMES
        if self.frame <= self.MAX_FRAMES/2:
            screen.blit(self.surface, self.pos)


class Vents(System):
    def __init__(self):
        super().__init__("Vent System", 'resources/background/test.png')

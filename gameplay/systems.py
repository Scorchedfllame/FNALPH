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
        screen = pygame.display.get_surface()
        self.font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 70)
        self.glitch_sound = pygame.mixer.Sound('resources/sounds/Garble1.mp3')
        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.scale_by(self.background, screen.get_height()/self.background.get_height())
        self._background = self.background.__copy__()
        self.font_pos = [0, 0]
        self.resize()

        self.glitch_sound.set_volume(.5)
        self._buttons = []
        self.font_color = 'White'

        self.name = name
        self.background_path = background_path

        self.MAX_GLITCH_TIMER = None
        self.active = None
        self.glitch_timer = None
        self.glitch = None

    def start(self):
        self.MAX_GLITCH_TIMER = self.glitch_sound.get_length() * 60
        self.active = False
        self.glitch_timer = 0
        self.glitch = False

    def stop(self):
        self.reset_background()

    def draw(self, surface, offset: int = 0) -> None:
        if self.glitch:
            self.glitch_timer += 1
            if self.glitch_timer + random.randint(0, 50) > self.MAX_GLITCH_TIMER:
                self.glitch_sound.stop()
                self.glitch_timer = 0
                self.glitch = False
        if self.active:
            cache = self.background.copy()
            surface.blit(self.background, (offset, 0))
            self.background = cache
            if self.glitch:
                black = pygame.Surface(surface.get_size())
                black.fill('black')
                surface.blit(black, (0, 0))

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

    def activate(self):
        self.active = True
        self.glitch_sound.set_volume(.5)

    def deactivate(self):
        self.active = False
        self.glitch_sound.set_volume(0)

    def add_button(self, button: Button):
        self._buttons.append(button)

    def draw_text(self, surface: pygame.Surface):
        if self.active:
            text = self.font.render(self.name, True, self.font_color)
            surface.blit(text, tuple(self.font_pos))


class Cameras(System):
    def __init__(self):
        super().__init__("Cams System", 'resources/background/test.png')

        # Load Resources
        self.camera_pan_sound = pygame.mixer.Sound('resources/sounds/camera_pan.mp3')
        self.font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 90)
        self.camera_switch_sound = pygame.mixer.Sound('resources/sounds/static.mp3')
        self.camera_switch_sound.set_volume(1)
        self.animation = Animator(pygame.image.load('resources/animations/Camera_Flip.png').convert_alpha(),
                                  pygame.rect.Rect(0, 0, 1920, 1080),
                                  speed=.5)
        self.camera_list = Camera.generate_cameras(self.load_data('cameras'))
        self.map_image = self.init_images()
        self.static = []
        for frame in os.listdir('resources/animations/static/'):
            image = pygame.image.load(f'resources/animations/static/{frame}').convert_alpha()
            image.set_alpha(100)
            self.static.append(image)
        self.switches = []
        for frame in os.listdir('resources/animations/switch/'):
            image = pygame.image.load(f"resources/animations/switch/{frame}").convert_alpha()
            self.switches.append(image)
        self.active_icons, self.inactive_icons = self.load_camera_buttons(self.load_data('cameras'))

        # Init Subsets
        self.generate_buttons()
        self.record_icon = RecordIcon((30, 30), 10, 3)
        self.camera_switch_sound.set_volume(.25)

        # Declare Variables
        self.SWITCH_TIME = None
        self.MAX_ROTATION = None
        self.enabled = None
        self.active = None
        self._last_camera = None
        self.current_rotation = None
        self.rotation_cycle = None
        self.switching = None
        self.switch_count = None

    def start(self):
        self.SWITCH_TIME = 4
        self.MAX_ROTATION = 90
        self.enabled = True
        self.active = False
        self._last_camera = 0
        self.current_rotation = 0
        self.rotation_cycle = 0
        self.switching = False
        self.switch_count = 0

        self.animation.start()
        self.disable_cameras()
        for camera in self.camera_list:
            camera.start()
        pygame.time.set_timer(pygame.event.Event(CAMERA_ROTATION), 3300)

    def stop(self):
        self.active = False
        for camera in self.camera_list:
            camera.stop()
        pygame.time.set_timer(CAMERA_ROTATION, 0)

    def tick(self, event: pygame.event.Event):
        for button in self.buttons:
            button.tick(event)
        if event.type == CAMERA_FLIPPED_UP:
            self.activate()
        if event.type == CAMERA_FLIPPED_DOWN:
            self.deactivate()
        if event.type == CAMERA_ROTATION:
            self.calculate_rotation()

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
                offset = self.get_pos_from_rot(screen.get_width(), camera.background.get_width())
                camera.draw(screen, offset)
            self.draw_static(screen, self.static)
            if self.switching:
                self.draw_switch(screen)
            for i in self.camera_list:
                i.draw_text(screen)
            self.draw_map(screen)
            for button in self.buttons:
                button.draw(screen)

            pygame.draw.rect(screen, (170, 170, 170), pygame.rect.Rect(10, 10, 1900, 1060), 2, 1)
            self.record_icon.draw(screen)

        self.animation.draw(screen)

    def draw_switch(self, screen):
        screen.blit(self.switches[random.randint(0, len(self.switches) - 1)], (0, 0))
        self.switch_count += 1
        if self.switch_count == self.SWITCH_TIME:
            self.switching = False
            self.switch_count = 0

    def activate(self):
        if not self.active:
            self.active = True
            self.activate_camera(self._last_camera)
            self.animation.play_forward()

    def deactivate(self):
        if self.active:
            self.active = False
            self._last_camera = self.get_active_camera()
            self.disable_cameras()
            self.animation.play_backward()

    def get_pos_from_rot(self, screen_x, image_x):
        # normalization 0-1
        normalized = (self.current_rotation + self.MAX_ROTATION)/(2*self.MAX_ROTATION)
        # turn into other stuff
        return normalized * (screen_x - image_x)

    def blackout(self):
        if self.active:
            pygame.event.post(pygame.event.Event(CAMERA_FLIPPED_DOWN))

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
            self.switching = True
        self.disable_cameras()
        camera = self.camera_list[camera_index]
        self.buttons[camera_index].change_surface(self.active_icons[camera_index])
        camera.activate()
        self._last_camera = camera_index

    def calculate_rotation(self):
        self.rotation_cycle += 1
        if self.rotation_cycle == 4:
            self.rotation_cycle = 0
        match self.rotation_cycle:
            case 0:
                self.current_rotation = -90
                self.camera_pan_sound.play(maxtime=3600)
            case 1:
                self.camera_pan_sound.set_volume(0)
                self.current_rotation = 90
            case 2:
                self.current_rotation = 90
                self.camera_pan_sound.play(maxtime=3600)
            case 3:
                self.camera_pan_sound.set_volume(0)
                self.current_rotation = -90

    def draw_map(self, surface: pygame.surface.Surface):
        rect = self.map_image.get_rect()
        rect.bottomright = (surface.get_width() - 20, surface.get_height() - 25)
        font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 100)
        self.map_image.blit(font.render("YOU", True, "white"), (640, 530))
        surface.blit(self.map_image, rect)

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
        for i in range(len(self.camera_list)):
            self.buttons.append(Button(self.inactive_icons[i],
                                (0, 0),
                                self.activate_camera,
                                camera_index=i))
        self.resize()

    @staticmethod
    def init_images():
        screen = pygame.display.get_surface()
        map_image = pygame.image.load('resources/ui/map.png').convert_alpha()
        scale_factor = Cameras.get_scaler(screen, map_image)
        map_image = pygame.transform.scale_by(map_image, scale_factor)
        map_image.set_alpha(200)
        return map_image

    @staticmethod
    def load_camera_buttons(data: list[dict]):
        active_path = "resources/ui/buttons/camera_icons/active"
        inactive_path = "resources/ui/buttons/camera_icons/inactive"
        scale_factor = 2
        active_icons = []
        inactive_icons = []
        for camera in data:
            active = pygame.image.load(active_path + "/" + camera['label'] + ".png").convert_alpha()
            inactive = pygame.image.load(inactive_path + "/" + camera['label'] + ".png").convert_alpha()
            active = pygame.transform.scale_by(active, scale_factor)
            inactive = pygame.transform.scale_by(inactive, scale_factor)
            active_icons.append(active)
            inactive_icons.append(inactive)
        return active_icons, inactive_icons

    @staticmethod
    def load_data(data: str) -> any:
        with open('data/game/cameras.json', 'r') as f:
            cameras_list = json.load(f)
            return cameras_list[data]

    @staticmethod
    def get_scaler(surface: pygame.Surface, rect: pygame.Surface | pygame.Rect):
        return surface.get_width()/(2.1*rect.get_width())

    @staticmethod
    def draw_static(screen: pygame.surface.Surface, static):
        frame = random.randint(0, len(static) - 1)
        image = static[frame]
        screen.blit(image, (0, 0))


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
        surface = pygame.transform.scale_by(surface, 30/self.radius)
        return surface

    def draw(self, screen):
        self.frame = (self.frame + 1) % self.MAX_FRAMES
        if self.frame <= self.MAX_FRAMES/2:
            screen.blit(self.surface, self.pos)


class Vents(System):
    def __init__(self):
        super().__init__("Vent System", 'resources/background/test.png')

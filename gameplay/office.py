import random
from data.game.constants import *
from .buttons import ToggleButton
from .animation import Animator
import json


class Office:
    def __init__(self):
        self.ambience = pygame.mixer.Sound('resources/sounds/office_ambience.mp3')
        self.ambience.set_volume(.2)
        self.camera_toggle_sound = pygame.mixer.Sound('resources/sounds/camera_pull.mp3')
        self.doors = Door.generate_doors()
        self.image = pygame.image.load('resources/backgrounds/office.png').convert()
        self.image = pygame.transform.scale_by(self.image,
                                               pygame.display.get_surface().get_height()/self.image.get_size()[1])
        self.surface = pygame.surface.Surface(self.image.get_size())
        self.rot_x = 0
        self.MAX_ROTATION = 90
        self.active = True
        self._locked = False

    def start(self):
        self.active = True
        self.rot_x = 0
        self.ambience.play()
        for door in self.doors:
            door.start()

    def get_power_usage(self):
        power_usage = 0
        for i in self.doors:
            if i.door_status == 'closed':
                power_usage += 1
            if i.light_status == 'light':
                power_usage += 1
        return power_usage

    def stop(self):
        self.ambience.stop()
        for door in self.doors:
            door.stop()

    def tick(self, event: pygame.event.Event):
        if self.active:
            for door in self.doors:
                door.tick(event)
        if event.type == CAMERA_FLIPPED_UP:
            self.active = False
            self.ambience.set_volume(.1)
            self.camera_toggle_sound.play()
        if event.type == CAMERA_FLIPPED_DOWN:
            self.active = True
            self.ambience.set_volume(.2)
            self.camera_toggle_sound.play()

    def frame(self):
        if self.active:
            self.rot_x += self.get_rot_from_mouse(pygame.mouse.get_pos())
            self.rot_x = max(-self.MAX_ROTATION, self.rot_x)
            self.rot_x = min(self.MAX_ROTATION, self.rot_x)

    @staticmethod
    def get_rot_from_mouse(mouse_pos):
        mouse_x, _ = mouse_pos
        screen_x, _ = pygame.display.get_surface().get_size()
        normalized = (2 * mouse_x/screen_x - 1)
        if screen_x * 3/7 > mouse_x or mouse_x > screen_x * 4/7:
            return normalized * 10
        return 0

    def get_pos_from_rot(self):
        screen_x, _ = pygame.display.get_surface().get_size()
        image_x, _ = self.image.get_size()
        # normalization 0-1
        normalized = (self.rot_x + self.MAX_ROTATION)/(2*self.MAX_ROTATION)

        # turn into other stuff
        return normalized * (screen_x - image_x)

    def draw(self):
        if self.active:
            screen = pygame.display.get_surface()
            self.surface.blit(self.image, (0, 0))
            screen.blit(self.surface, (self.get_pos_from_rot(), 0))
            for door in self.doors:
                door.draw(screen, pygame.Vector2(self.get_pos_from_rot(), 0))


class Door:
    def __init__(self, image_paths: dict[str], positions: dict):
        self.light_off_sound = pygame.mixer.Sound('resources/sounds/light_stuck.mp3')
        self.light_on_sound = pygame.mixer.Sound('resources/sounds/light_button.mp3')
        self.door_toggle_sound = pygame.mixer.Sound('resources/sounds/door_close.mp3')
        self._default_images = {key: pygame.image.load(value).convert_alpha() for key, value in image_paths.items()}
        scalar = pygame.display.get_surface().get_height()/self._default_images['open_dark'].get_size()[1]
        for key, image in self._default_images.items():
            self._default_images[key] = pygame.transform.scale_by(image, scalar)
        self.curr_images = self._default_images.copy()
        self.light_noise = pygame.mixer.Sound('resources/sounds/light_noise.mp3')
        self.light_status = 'dark'
        self.door_status = 'open'
        self.relative_pos = positions
        self.flicker_counter = 1
        self.current_surface = self.curr_images[self.get_status()]
        self.rect = self.current_surface.get_rect()
        self.rect.topleft = self.relative_pos['door']
        self.light_button = ToggleButton(self.curr_images['button'],
                                         self.relative_pos['light'],
                                         self.light_on,
                                         self.light_off)
        self.door_button = ToggleButton(self.curr_images['button'],
                                        self.relative_pos['door'],
                                        self.close_door,
                                        self.open_door)
        anim_rect = self.current_surface.get_rect()
        self.animator = Animator(self.curr_images['animation'], anim_rect)
        self.button_fail_sound = pygame.mixer.Sound('resources/sounds/light_stuck.mp3')
        self.door_toggle_sound.set_volume(.5)

    def start(self):
        self.light_status = 'dark'
        self.door_status = 'open'
        self.door_button.active = False
        self.light_button.active = False

    def stop(self):
        self.button_fail_sound.stop()
        self.door_toggle_sound.stop()
        self.light_noise.stop()
        self.light_on_sound.stop()
        self.light_off_sound.stop()

    def reset(self):
        self.curr_images = self._default_images.copy()

    @classmethod
    def generate_doors(cls) -> list:
        door_list = []
        with open('data/game/office.json', 'r') as f:
            dictionary = json.loads(f.read())
            for door in dictionary['doors']:
                door_list.append(Door(door['images'], {
                    k: tuple(v) for k, v in door['positions'].items()}))
        return door_list

    def tick(self, event: pygame.event.Event):
        if event.type == CAMERA_FLIPPED_UP:
            self.light_button.check_deactivate()
        self.door_button.tick(event)
        self.light_button.tick(event)

    def get_flicker(self):
        if self.light_status == 'light':
            if self.flicker_counter > 0:
                if random.randint(self.flicker_counter, 101) >= 100:
                    self.flicker_counter = -1
                    self.light_noise.stop()
                    return 'dark'

                else:
                    self.flicker_counter += 1

                    return 'light'

            elif self.flicker_counter < 0:
                if random.randint(-10, self.flicker_counter) <= -8:
                    self.flicker_counter = 1
                    pygame.mixer.find_channel(True).play(self.light_noise, loops=100)
                    return 'light'
                else:
                    return 'dark'
        return 'dark'

    def draw(self, surface: pygame.Surface, vector: pygame.Vector2):
        if not self.animator.active:
            light = self.get_flicker()
            self.current_surface = self.curr_images[f"{self.door_status}_{light}"]
            light_positions = self.relative_pos['light']
            door_positions = self.relative_pos['door']
            button_positions = self.relative_pos['button']
            self.rect.topleft = (0, 0)
            self.rect.move_ip(vector)
            surface.blit(self.current_surface, (self.rect.x + door_positions[0], self.rect.y + door_positions[1]))
            self.door_button.resize((self.rect.x + button_positions[0], self.rect.y + button_positions[1]), scale=1.2)
            self.light_button.resize((self.rect.x + light_positions[0], self.rect.y + light_positions[1]), scale=1.2)
        self.animator.draw(surface, vector)

    def lock(self):
        def fail():
            pygame.mixer.find_channel(True).play(self.button_fail_sound)
        self.door_button.activate = fail
        self.light_button.activate = fail
        self.door_button.deactivate = fail
        self.light_button.deactivate = fail

    def light_on(self):
        pygame.mixer.find_channel(True).play(self.light_noise, loops=100)
        pygame.mixer.find_channel(True).play(self.light_on_sound)
        self.light_status = 'light'

    def light_off(self):
        self.light_noise.stop()
        pygame.mixer.find_channel(True).play(self.light_off_sound)
        self.light_status = 'dark'

    def get_status(self):
        return f"{self.door_status}_{self.light_status}"

    def open_door(self):
        pygame.mixer.find_channel(True).play(self.door_toggle_sound)
        self.animator.play_backward()
        self.door_status = 'open'
        self.current_surface = self.curr_images[f"open_{self.light_status}"]

    def close_door(self):
        pygame.mixer.find_channel(True).play(self.door_toggle_sound)
        self.animator.play_forward()
        self.door_status = 'closed'
        self.current_surface = self.curr_images[f"closed_{self.light_status}"]

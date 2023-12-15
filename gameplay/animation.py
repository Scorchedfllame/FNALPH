import time

import pygame


class Animator:
    def __init__(self,
                 frames: pygame.Surface,
                 image_rect: pygame.Rect,
                 current_frame: int = 0,
                 direction: str = 'forward',
                 type: str = 'once'):
        self.frames = frames
        self.image_rect = image_rect
        self.MAX_FRAME = int(frames.get_height()/image_rect.height)
        self.current_frame = current_frame
        self.direction = direction
        self.active = False
        self.type = type

    def update_rect(self):
        self.image_rect.y = self.current_frame * self.image_rect.height

    def one_forward(self):
        self.current_frame += 1
        if self.current_frame > self.MAX_FRAME:
            match self.type:
                case 'loops':
                    self.current_frame = 0
                case 'stay':
                    self.current_frame = self.MAX_FRAME
                case 'once':
                    self.active = False

    def one_backward(self):
        self.current_frame -= 1
        if self.current_frame < 0:
            match self.type:
                case 'loops':
                    self.current_frame = self.MAX_FRAME
                case 'stay':
                    self.current_frame = 0
                case 'once':
                    self.active = False

    def draw(self, surface: pygame.Surface, vector: pygame.Vector2 = pygame.Vector2(0, 0)):
        if self.active:
            self.update_rect()
            surface.blit(self.frames, vector, self.image_rect)
            if self.direction == 'backward':
                self.one_backward()
            elif self.direction == 'forward':
                self.one_forward()

    def play_forward(self):
        self.active = True
        self.direction = 'forward'
        self.current_frame = 0

    def play_backward(self):
        self.active = True
        self.direction = 'backward'
        self.current_frame = self.MAX_FRAME

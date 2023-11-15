import pygame
from typing import Callable


class Button:
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int] = None,
                 activate: pygame.event.Event | Callable = None,
                 deactivate: pygame.event.Event | Callable = None,
                 draw_type: str = None,
                 **kwargs):
        if type(base) == pygame.Rect:
            self.rect = base
            self.surface = None
        elif type(base) == pygame.surface.Surface:
            self.rect = base.get_rect()
            self.surface = base
        if pos is not None:
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        self.draw_type = draw_type
        self.activate = activate
        self.deactivate = deactivate
        self.kwargs = kwargs

    def tick(self, event: pygame.event.Event):
        activate_type = type(self.activate)
        deactivate_type = type(self.deactivate)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.activate is not None:
                    if activate_type == Callable:
                        self.activate(**self.kwargs)
                    elif activate_type == pygame.event.Event:
                        pygame.event.post(self.activate)
        if event.type == pygame.MOUSEBUTTONUP:
            if not self.rect.collidepoint(event.pos):
                if self.deactivate is not None:
                    if deactivate_type == Callable:
                        self.deactivate(**self.kwargs)
                    elif deactivate_type == pygame.event.Event:
                        pygame.event.post(self.deactivate)

    def draw(self):
        print('draw')
        if self.surface:
            if self.draw_type is not None:
                try:
                    pygame.display.get_surface().blit(self.surface, self.rect.__getattribute__(self.draw_type))
                except TypeError:
                    pass
            else:
                pygame.display.get_surface().blit(self.surface, self.rect)


class Flick(Button):
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int] = None,
                 activate: Callable | pygame.event.Event = None,
                 deactivate: Callable | pygame.event.Event = None,
                 **kwargs):
        super().__init__(base, pos=pos, **kwargs)
        self.activate = activate
        self.deactivate = deactivate
        self.mouse_y = 0
        self.activated = False
        self.hovering = False

    def tick(self, event: pygame.event.Event):
        # Don't touch the IF monster
        activate_type = type(self.activate)
        deactivate_type = type(self.deactivate)
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if self.mouse_y < pygame.mouse.get_pos()[1] and not self.activated:
                    if not self.hovering:
                        if activate_type == Callable:
                            self.activate(**self.kwargs)
                        elif activate_type == pygame.event.Event:
                            pygame.event.post(self.activate)
                        self.hovering = True
                    else:
                        if deactivate_type == Callable:
                            self.deactivate(**self.kwargs)
                        elif deactivate_type == pygame.event.Event:
                            pygame.event.post(self.deactivate)
                        self.hovering = False
                    self.activated = True
            else:
                self.activated = False
            self.mouse_y = event.pos[1]

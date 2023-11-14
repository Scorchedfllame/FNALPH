import pygame


class Button:
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int] = None,
                 activate: callable = None,
                 deactivate: callable = None):
        if type(base) == pygame.Rect:
            self.rect = base
            self.surface = None
        elif type(base) == pygame.surface.Surface:
            self.rect = base.get_rect()
            self.surface = base
        if pos is not None:
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        self.activate = activate
        self.deactivate = deactivate

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.activate is not None:
                    self.activate()
        if event.type == pygame.MOUSEBUTTONUP:
            if not self.rect.collidepoint(event.pos):
                if self.deactivate is not None:
                    self.deactivate()

    def draw(self, draw_type: str = None):
        if self.surface:
            if draw_type is not None:
                try:
                    pygame.display.get_surface().blit(self.surface, self.rect.__getattribute__(draw_type))
                except TypeError:
                    pass
            else:
                pygame.display.get_surface().blit(self.surface, self.rect)


class Flick(Button):
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int] = None,
                 activate: callable = None):
        super().__init__(base, pos=pos, activate=activate)
        self.mouse_y = 0

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                if self.mouse_y < pygame.mouse.get_pos()[1]:
                    self.activate()
            self.mouse_y = event.pos[1]

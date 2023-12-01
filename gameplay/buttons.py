import pygame


class Button:
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int],
                 activate: any = None,
                 deactivate: any = None,
                 draw_type: str = "topleft",
                 **kwargs):
        if type(base) == pygame.Rect:
            self.rect = base
            self.surface = None
        elif type(base) == pygame.surface.Surface:
            self.rect = base.get_rect()
            self.surface = base
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.draw_type = draw_type
        self.activate = activate
        self.deactivate = deactivate
        self.kwargs = kwargs

    def change_surface(self, surface: pygame.surface.Surface):
        self.surface = pygame.transform.scale(surface, self.rect.size)

    def check_type(self, action: any):
        if type(action) == pygame.event.Event:
            pygame.event.post(action)
        else:
            action(**self.kwargs)

    def check_activate(self, event: pygame.event.Event):
        if self.rect.collidepoint(event.pos) and self.activate is not None:
            self.check_type(self.activate)

    def check_deactivate(self, event: pygame.event.Event):
        if not self.rect.collidepoint(event.pos) and self.deactivate is not None:
            self.check_type(self.deactivate)

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_activate(event)
        if event.type == pygame.MOUSEBUTTONUP:
            self.check_deactivate(event)

    def draw(self, surface):
        if self.surface:
            surface.blit(self.surface, self.rect.__getattribute__(self.draw_type))


class Flick(Button):
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int] = None,
                 activate: any = None,
                 deactivate: any = None,
                 **kwargs):
        super().__init__(base, pos, **kwargs)
        self.activate = activate
        self.deactivate = deactivate
        self.mouse_y = 0
        self.activated = False
        self.hovering = False

    def check_activate(self, event: pygame.event.Event):
        if self.mouse_y < pygame.mouse.get_pos()[1] and not self.activated:
            self.activated = True
            if not self.hovering:
                self.check_type(self.activate)
                self.hovering = True
            else:
                self.check_deactivate(event)

    def check_deactivate(self, event: pygame.event.Event):
        self.check_type(self.deactivate)
        self.hovering = False

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.check_activate(event)
            else:
                self.activated = False
            self.mouse_y = event.pos[1]

import pygame


class Button:
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int],
                 activate: any = None,
                 deactivate: any = None,
                 draw_type: str = None,
                 **kwargs):
        if type(base) == pygame.Rect:
            self.rect = base
            self.surface = None
        elif type(base) == pygame.surface.Surface:
            self.rect = base.get_rect()
            self.surface = base
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        if draw_type is not None:
            pos = self.rect.__getattribute__(draw_type)
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        self.activate = activate
        self.deactivate = deactivate
        self.kwargs = kwargs

    def tick(self, event: pygame.event.Event):
        activate_type = type(self.activate)
        deactivate_type = type(self.deactivate)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.activate is not None:
                    if activate_type == pygame.event.Event:
                        pygame.event.post(self.activate)
                    else:
                        self.activate(**self.kwargs)
        if event.type == pygame.MOUSEBUTTONUP:
            if not self.rect.collidepoint(event.pos):
                if self.deactivate is not None:
                    if deactivate_type == pygame.event.Event:
                        pygame.event.post(self.deactivate)
                    else:
                        self.deactivate(**self.kwargs)

    def draw(self):
        if self.surface:
            pygame.display.get_surface().blit(self.surface, self.rect)


class Flick(Button):
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int] = None,
                 activate: any = None,
                 deactivate: any = None,
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
                        if activate_type == pygame.event.Event:
                            pygame.event.post(self.activate)
                        else:
                            self.activate(**self.kwargs)
                        self.hovering = True
                    else:
                        if deactivate_type == pygame.event.Event:
                            pygame.event.post(self.deactivate)
                        else:
                            self.deactivate(**self.kwargs)
                        self.hovering = False
                    self.activated = True
            else:
                self.activated = False
            self.mouse_y = event.pos[1]


class CameraButton(Button):
    def __init__(self, base: pygame.Rect | pygame.surface.Surface,
                 pos: tuple[int, int],
                 active_icon_path: str,
                 inactive_icon_path: str,
                 activate: any = None,
                 deactivate: any = None,
                 draw_type: str = None,
                 **kwargs):
        super().__init__(self, base, pos, activate, deactivate, draw_type, **kwargs)

    def draw(self):

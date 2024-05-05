import os
from gameplay import Cameras, Game, Button
from data.game.constants import *
from data.saves.save import SaveManager
import random


class Menu:
    def __init__(self, directory: str):
        self.background = pygame.image.load(directory + "background.png").convert()

        self.main_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 500)
        self.secondary_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 50)

        scalar = pygame.display.get_surface().get_width()/self.background.get_width()
        self.background = pygame.transform.scale_by(self.background, scalar)
        self.buttons = []
        self.parent = None

    def start(self):
        pass

    def back(self):
        if self.parent is not None:
            pygame.event.post(pygame.event.Event(MENU_CHANGE, {'func': 'change', 'target': self.parent}))


class MainMenu(Menu):
    def __init__(self):
        super().__init__("resources/ui/menus/main_menu/")

        self.static = []
        for frame in os.listdir('resources/animations/static/'):
            image = pygame.image.load(f'resources/animations/static/{frame}').convert_alpha()
            image.set_alpha(50)
            self.static.append(image)

        self.save_manager = SaveManager()
        self.buttons = self.init_buttons()

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        for button in self.buttons.values():
            button.tick(event)

    def start(self):
        self.save_manager.load_data()

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.background, (0, 0))
        screen.blit(random.choice(self.static), (0, 0))
        for button in self.buttons.values():
            button.draw(screen)
        night = self.secondary_font.render(f"Night {self.save_manager.data['night']}",
                                           True,
                                           (201, 0, 7))
        night_rect = night.get_rect()
        cont_button = self.buttons['continue']
        night_rect.topleft = cont_button.rect.bottomleft
        night_rect.y -= 25
        screen.blit(night, night_rect)

    def new_game(self):
        self.save_manager.reset_night()
        self.start_game()

    def start_game(self):
        pygame.display.get_surface().fill('black')
        pygame.display.flip()
        pygame.event.post(pygame.event.Event(MENU_CHANGE, {'func': 'start_game'}))

    def continue_game(self):
        self.start_game()

    def init_buttons(self) -> dict[str: Button]:
        color = (201, 0, 7)
        continue_surface = self.main_font.render('Continue', True, color)
        play_surface = self.main_font.render('New Game', True, color)
        quit_surface = self.main_font.render('Quit', True, color)
        options_surface = self.main_font.render('Options', True, color)
        continue_button = Button(continue_surface, (960, 600), scale=.2,
                                 activate=self.continue_game, draw_type='center')
        play_game = Button(play_surface, (960, 700), scale=.2,
                           activate=self.new_game, draw_type='center')
        options_button = Button(options_surface, (960, 800), scale=.2,
                                activate=pygame.event.Event(MENU_CHANGE, {'func': 'change', 'target': 1}),
                                draw_type='center')
        quit_button = Button(quit_surface, (960, 900), scale=.2,
                             activate=pygame.event.Event(pygame.QUIT), draw_type='center')
        return {"play": play_game, "continue": continue_button, "quit": quit_button, "options": options_button}


class Options(Menu):
    def __init__(self, parent):
        super().__init__('resources/ui/menus/options_menu/')
        self.parent = parent
        self.back_button = Button(self.main_font.render("Back", True, 'white'),
                                  (140, 800), scale=.2, activate=self.back)
        self.cheat_button = Button(self.main_font.render("Cheats", True, 'white'),
                                   (140, 900), scale=.2, activate=pygame.event.Event(MENU_CHANGE, {'func': 'change', 'target': 2}))

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()
        self.back_button.tick(event)
        self.cheat_button.tick(event)

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.background, (0, 0))
        self.back_button.draw(surface)
        self.cheat_button.draw(surface)


class Cheat(Menu):
    def __init__(self, parent):
        super().__init__('resources/ui/menus/cheat_menu/')
        self.parent = parent
        self.input = StrInput()
        self.save_manager = SaveManager()
        self.night_input = Button(self.main_font.render("Night", True, "white"),
                                  (140, 900), scale=.2, activate=self.input.start)
        self.back_button = Button(self.main_font.render("Back", True, 'white'),
                                  (140, 800), scale=.2, activate=self.back)

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()
            if event.key == pygame.K_RETURN:
                self.input.stop()
                try:
                    self.save_manager.load_data()
                    self.save_manager.data['night'] = int(self.input.final)
                    self.save_manager.save_game()
                except ValueError:
                    pass
        self.input.tick(event)
        self.night_input.tick(event)
        self.back_button.tick(event)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.back_button.draw(surface)
        self.night_input.draw(surface)
        inp = self.secondary_font.render(self.input.input, True, 'white')
        inp_rect = inp.get_rect()
        inp_rect.bottomleft = (0, 1080)
        surface.blit(inp, inp_rect)


class StrInput:
    def __init__(self):
        self.input = None
        self.final = None

    def start(self):
        self.input = ''
        self.final = ''
        pygame.key.start_text_input()

    def stop(self):
        pygame.key.stop_text_input()
        self.final = self.input
        self.input = ''
        return self.final

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.TEXTINPUT:
            self.input += event.text

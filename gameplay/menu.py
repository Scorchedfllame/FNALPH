import os
from gameplay import Button, ToggleButton
from data.game.constants import *
from data.saves.save import SaveManager
from pygame_widgets.textbox import TextBox
from pygame_widgets.slider import Slider
import random


class Menu:
    red = (201, 0, 7)
    dark_red = (55, 25, 27)

    def __init__(self, directory: str):
        self.background = pygame.image.load(directory + "background.png").convert()

        self.main_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 500)
        self.secondary_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 50)
        self.tertiary_font = pygame.font.Font('resources/fonts/Book Antiqua.ttf', 25)

        scalar = pygame.display.get_surface().get_width()/self.background.get_width()
        self.background = pygame.transform.scale_by(self.background, scalar)
        self.buttons = []
        self.parent = None

        self.color = (201, 0, 7)

    def start(self):
        pass

    def stop(self):
        pass

    def back(self):
        if self.parent is not None:
            pygame.event.post(pygame.event.Event(MENU_CHANGE, {'func': 'change', 'target': self.parent}))


class MainMenu(Menu):
    def __init__(self):
        super().__init__("resources/ui/menus/main_menu/")
        self._background = self.background.copy()

        self.secret_background = pygame.image.load('resources/ui/menus/main_menu/secret_background.png').convert()

        self.static = []
        for frame in os.listdir('resources/animations/static/'):
            image = pygame.image.load(f'resources/animations/static/{frame}').convert_alpha()
            image.set_alpha(50)
            self.static.append(image)

        self.save_manager = SaveManager()

        self.save_manager.load_data()
        data = self.save_manager.data
        if data['night'] == 0:
            self.new = True
        else:
            self.new = False

        self.buttons = self.init_buttons()

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        for button in self.buttons.values():
            button.tick(event)

    def start(self):
        self.save_manager.load_data()
        data = self.save_manager.data
        if data['night'] == 0:
            self.new = True
        else:
            self.new = False
        self.buttons = self.init_buttons()

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.background, (0, 0))
        screen.blit(random.choice(self.static), (0, 0))
        for button in self.buttons.values():
            button.draw(screen)
        if not self.new:
            night = self.secondary_font.render(f"Night {self.save_manager.data['night']}",
                                               True,
                                               self.color)
            night_rect = night.get_rect()
            cont_button = self.buttons['continue']
            night_rect.topleft = cont_button.rect.bottomleft
            night_rect.y -= 25
            screen.blit(night, night_rect)
        version_text = self.tertiary_font.render('v0.2.1', True, self.color)
        version_rect = version_text.get_rect()
        version_rect.bottomright = (1900, 1060)
        screen.blit(version_text, version_rect)

    def cheat_background(self):
        self.background = self.secret_background
        self.color = (255, 255, 255)
        self.buttons = self.init_buttons()

    def end_cheat_background(self):
        self.background = self._background
        self.color = Menu.red
        self.buttons = self.init_buttons()

    def new_game(self):
        self.save_manager.reset_night()
        self.start_game()

    def start_game(self):
        pygame.event.post(pygame.event.Event(MENU_CHANGE, {'func': 'start_game'}))

    def continue_game(self):
        self.start_game()

    def init_buttons(self) -> dict[str: Button]:
        if self.new:
            continue_surface = self.main_font.render('Continue', True, (41, 25, 27))
            continue_button = Button(continue_surface, (960, 600), scale=.2, draw_type='center')
        else:
            continue_surface = self.main_font.render('Continue', True, self.color)
            continue_button = Button(continue_surface, (960, 600), scale=.2,
                                     activate=self.continue_game, draw_type='center')
        play_surface = self.main_font.render('New Game', True, self.color)
        quit_surface = self.main_font.render('Quit', True, self.color)
        options_surface = self.main_font.render('Options', True, self.color)
        play_game = Button(play_surface, (960, 700), scale=.2,
                           activate=self.new_game, draw_type='center')
        options_button = Button(options_surface, (960, 800), scale=.2,
                                activate=pygame.event.Event(MENU_CHANGE, {'func': 'change', 'target': 1}),
                                draw_type='center')
        quit_button = Button(quit_surface, (960, 900), scale=.2,
                             activate=pygame.event.Event(pygame.QUIT), draw_type='center')
        return {"play": play_game, "continue": continue_button, "quit": quit_button, "options": options_button}


def set_volume(value: int):
    for i in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(i).set_volume(value/100)


class Options(Menu):
    def __init__(self, parent):
        super().__init__('resources/ui/menus/options_menu/')
        self.background.fill('black')
        border = pygame.Rect(10, 10, 1900, 1060)
        pygame.draw.rect(self.background, self.color, border, 5)

        self.parent = parent
        self.volume_slider = Slider(pygame.display.get_surface(), 140, 800, 500, 20, max=100, min=0,
                                    colour=Menu.dark_red, borderColour=Menu.red, handleColour=Menu.red)
        self.volume_slider.hide()
        self.volume_slider.disable()

        self.save_manager = SaveManager()
        self.save_manager.load_data()

        self.back_button = Button(self.main_font.render("Back", True, self.color),
                                  (140, 900), scale=.2, activate=self.back)
        self.credits_button = Button(self.main_font.render("Credits", True, self.color),
                                     (1900, 900), scale=.2, draw_type='bottomright',
                                     activate=pygame.event.Event(MENU_CHANGE, {'func': 'change', 'target': 3}))
        self.cheat_button = Button(self.main_font.render("Cheats", True, self.color),
                                   (1900, 1000), scale=.2, draw_type='bottomright',
                                   activate=pygame.event.Event(MENU_CHANGE, {'func': 'change', 'target': 2}))
        set_volume(self.save_manager.data['volume'])

    def start(self):
        self.volume_slider.enable()
        self.volume_slider.show()
        self.save_manager.load_data()
        self.volume_slider.setValue(self.save_manager.data['volume'])

    def stop(self):
        self.volume_slider.disable()
        self.volume_slider.hide()
        self.save_manager.data['volume'] = self.volume_slider.getValue()
        self.save_manager.save_game()

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()
        set_volume(self.volume_slider.getValue())
        self.back_button.tick(event)
        self.cheat_button.tick(event)
        self.credits_button.tick(event)

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.background, (0, 0))
        self.back_button.draw(surface)
        self.cheat_button.draw(surface)
        self.credits_button.draw(surface)
        self.volume_slider.draw()
        volume = self.secondary_font.render('Volume', True, self.red)
        surface.blit(volume, (130, 750))


class Credits(Menu):
    def __init__(self, parent):
        super().__init__('resources/ui/menus/credits_menu/')
        border = pygame.Rect(10, 10, 1900, 1060)
        pygame.draw.rect(self.background, self.color, border, 5)
        self.parent = parent
        self.back_button = Button(self.main_font.render("Back", True, self.red),
                                  (140, 900), scale=.2, activate=self.back)

    def tick(self, event: pygame.event.Event):
        self.back_button.tick(event)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))
        self.back_button.draw(surface)


class Cheat(Menu):
    def __init__(self, parent):
        super().__init__('resources/ui/menus/cheat_menu/')
        self.background.fill('black')
        border = pygame.Rect(10, 10, 1900, 1060)
        pygame.draw.rect(self.background, self.color, border, 5)
        self.parent = parent
        self.night_input = TextBox(pygame.display.get_surface(), 140, 800, 300, 60, borderColour=Menu.red,
                                   textColour=Menu.red, placeholderText='night', font=self.secondary_font, fontSize=10,
                                   placeholderTextColour=Menu.red,
                                   placeholderTextSize=Menu.red, colour=(0, 0, 0), onSubmit=self.submit_night_input)
        self.night_input.disable()
        self.night_input.hide()
        self.save_manager = SaveManager()
        self.back_button = Button(self.main_font.render("Back", True, self.red),
                                  (140, 900), scale=.2, activate=self.back)
        self.change_background = ToggleButton(self.main_font.render("Background", True, self.color),
                                              (140, 700), scale=.2, activate=self.go_background,
                                              deactivate=self.end_background)

    def start(self):
        self.night_input.enable()
        self.night_input.show()
        super().start()

    def stop(self):
        self.night_input.disable()
        self.night_input.hide()
        super().stop()

    def submit_night_input(self):
        try:
            self.save_manager.load_data()
            self.save_manager.data['night'] = int(self.night_input.getText())
            self.night_input.setText('')
            self.save_manager.save_game()
        except ValueError:
            pass

    def tick(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()
        self.back_button.tick(event)
        self.change_background.tick(event)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.back_button.draw(surface)
        self.change_background.draw(surface)
        self.night_input.draw()

    def go_background(self):
        pygame.event.post(pygame.event.Event(MENU_CHANGE, {'func': 'go_background'}))
        self.change_background.change_surface(self.main_font.render("Background", True, 'white'))

    def end_background(self):
        pygame.event.post(pygame.event.Event(MENU_CHANGE, {'func': 'end_background'}))
        self.change_background.change_surface(self.main_font.render("Background", True, Menu.red))

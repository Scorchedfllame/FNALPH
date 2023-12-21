import os
import pygame_widgets
import pygame.transform
from gameplay import *
from data.saves.save import SaveManager


class Menu:
    def __init__(self, directory: str):
        self.directory = directory
        self.main_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 500)
        self.secondary_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 400)
        self.background_sound = pygame.mixer.Sound('resources/sounds/main_menu.mp3')
        self.background = pygame.image.load(self.directory + "background.png").convert()
        self.background = pygame.transform.scale_by(self.background, pygame.display.get_surface().get_width()/self.background.get_width())
        self.buttons = []
        self.active = False
        self.save_manager = SaveManager()
        self.background_sound.play(loops=10)

    def activate(self):
        self.active = True


class MainMenu(Menu):
    def __init__(self):
        super().__init__("resources/ui/menus/main_menu/")
        self.buttons = self.init_buttons()
        self.active = False
        self.game_round = None

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            for button in self.buttons.values():
                button.tick(event)

    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        for button in self.buttons.values():
            button.draw(screen)

    def new_game(self):
        self.save_manager.reset_save()
        self.start_game()

    def start_game(self):
        self.background_sound.stop()
        self.active = False
        self.game_round = Game(self.save_manager)
        self.game_round.start()

    def continue_game(self):
        self.start_game()

    def init_buttons(self) -> dict[str: Button]:
        continue_button = Button(self.main_font.render('Continue', True, 'white'),
                                 (140, 800),
                                 activate=self.continue_game, scale=.2)
        play_game = Button(self.main_font.render('New Game', True, 'white'),
                           (140, 900),
                           activate=self.new_game, scale=.2)
        quit_button = Button(self.main_font.render('Quit', True, 'white'),
                      (140, 1000),
                      activate=pygame.event.Event(pygame.QUIT), scale=.2)
        return {"play": play_game, "continue": continue_button, "quit": quit_button}


class Options(Menu):
    pass

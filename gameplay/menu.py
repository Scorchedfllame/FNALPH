import os

import pygame.transform
from gameplay import *
from data.saves.save import SaveManager


class Menu:
    def __init__(self, directory: str):
        self.directory = directory
        self.background = pygame.image.load(self.directory + "background.png").convert()
        self.background = pygame.transform.scale_by(self.background, pygame.display.get_surface().get_width()/self.background.get_width())
        self.buttons = []
        self.active = False
        self.save_manager = SaveManager()

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
                    pygame.quit()
                    exit()
            for button in self.buttons:
                button.tick(event)

    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(screen)

    def new_game(self):
        self.save_manager.reset_save()
        self.start_game()

    def start_game(self):
        self.active = False
        self.game_round = Game(self.save_manager.load_data()['night'])
        self.game_round.start()

    def continue_game(self):
        self.start_game()

    def init_buttons(self) -> list[Button]:
        play_game = Button(pygame.image.load(self.directory + "buttons/new_game.png"),
                           (160, 900),
                           activate=self.new_game, scale=.2)
        options = Button(pygame.image.load(self.directory + "buttons/continue.png"),
                         (160, 1000),
                         activate=self.continue_game, scale=.2)
        return [play_game, options]


class Options(Menu):
    pass

import os
from gameplay import *


class Menu:
    def __init__(self, directory: str):
        self.directory = directory
        self.background = pygame.image.load(self.directory + "background.png").convert()
        self.buttons = []
        self.active = False

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
            for button in self.buttons:
                button.tick(event)

    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(screen)

    def start_game(self):
        self.active = False
        self.game_round = Game()
        self.game_round.start()

    def open_options(self):
        pass

    def init_buttons(self) -> list[Button]:
        play_game = Button(pygame.image.load(self.directory + "buttons/new_game.png"),
                           (100, 800),
                           activate=self.start_game, scale=.25)
        options = Button(pygame.image.load(self.directory + "buttons/continue.png"),
                         (100, 900),
                         activate=self.open_options(), scale=.25)
        return [play_game, options]


class Options(Menu):
    pass

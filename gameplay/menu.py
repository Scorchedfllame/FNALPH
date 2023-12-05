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
        play_game = Button(pygame.image.load(self.directory + "buttons/play.png"),
                           (100, 100),
                           activate=self.start_game)
        options = Button(pygame.image.load(self.directory + "buttons/options.png"),
                         (100, 200),
                         activate=self.open_options())
        return [play_game, options]


class Options(Menu):
    pass

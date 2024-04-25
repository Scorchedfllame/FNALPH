import os
import pygame.transform
from gameplay import Cameras, Game, Button
from data.saves.save import SaveManager


class Menu:
    def __init__(self, directory: str):
        self.directory = directory
        self.background = pygame.image.load(self.directory + "background.png").convert()
        scalar = pygame.display.get_surface().get_width()/self.background.get_width()
        self.background = pygame.transform.scale_by(self.background, scalar)
        self.buttons = []
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


class MainMenu(Menu):
    def __init__(self):
        super().__init__("resources/ui/menus/main_menu/")
        self.main_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 500)
        self.secondary_font = pygame.font.Font('resources/fonts/five-nights-at-freddys.ttf', 50)
        self.background_sound = pygame.mixer.Sound('resources/sounds/main_menu.mp3')
        self.save_manager = SaveManager()
        self.static = []
        for frame in os.listdir('resources/animations/static/'):
            image = pygame.image.load(f'resources/animations/static/{frame}').convert_alpha()
            self.static.append(image)
        self.buttons = self.init_buttons()
        self.game = Game(self.save_manager)

    def activate(self):
        self.background_sound.play(loops=10)
        self.active = True

    def deactivate(self):
        self.background_sound.stop()
        self.active = False

    def tick(self):
        events = pygame.event.get()
        for event in events:
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
        Cameras.draw_static(screen, self.static)
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
        self.save_manager.reset_save()
        self.start_game()

    def start_game(self):
        self.save_manager.load_data()
        self.deactivate()
        pygame.display.get_surface().fill('black')
        pygame.display.flip()
        self.game.start()

    def continue_game(self):
        self.start_game()

    def init_buttons(self) -> dict[str: Button]:
        color = (201, 0, 7)
        continue_surface = self.main_font.render('Continue', True, color)
        play_surface = self.main_font.render('New Game', True, color)
        quit_surface = self.main_font.render('Quit', True, color)
        continue_button = Button(continue_surface, (140, 800), scale=.2, activate=self.continue_game)
        play_game = Button(play_surface, (140, 900), scale=.2, activate=self.new_game)
        quit_button = Button(quit_surface, (140, 1000), scale=.2, activate=pygame.event.Event(pygame.QUIT))
        return {"play": play_game, "continue": continue_button, "quit": quit_button}


class Options(Menu):
    pass

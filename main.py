# import gc

import pygame.display
from gameplay import *
# from data.saves.save import SaveManager
# import time


def fade_image(image: pygame.surface.Surface, screen: pygame.surface.Surface, len_dir: range):
    for i in len_dir:
        black = pygame.surface.Surface((1920, 1080))
        black.fill((0, 0, 0))
        black.set_alpha(i)
        screen.blit(image, (0, 0))
        screen.blit(black, (0, 0))
        pygame.display.flip()


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(10)
    pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Five Nights At Lone Peak High')
    pygame.display.set_icon(pygame.image.load('resources/ui/icon.png').convert())
    loading_image = pygame.image.load('resources/ui/menus/main_menu/teamLogoScreen.png').convert_alpha()
    fade_image(loading_image, pygame.display.get_surface(), range(255, 0, -1))
    pygame.display.get_surface().blit(loading_image, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    main_menu = MainMenu()
    fade_image(loading_image, pygame.display.get_surface(), range(255))
    main_menu.activate()

    # Window Loop
    while True:
        pygame.display.get_surface().fill("black")
        if main_menu.active:
            # Menu loop
            main_menu.tick()
            main_menu.draw()
        else:
            if main_menu.game.active:
                # Game loop
                main_menu.game.global_tick()
                main_menu.game.global_draw()
            elif main_menu.game.end_function == 'menu':
                main_menu.activate()
            elif main_menu.game.end_function == 'next':
                main_menu.continue_game()
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

import pygame.display
from gameplay import *
# from data.saves.save import SaveManager


def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(10)
    info = pygame.display.Info()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption('Five Nights At Lone Peak High')
    pygame.display.set_icon(pygame.image.load('resources/ui/icon.png').convert())
    clock = pygame.time.Clock()
    debugger = True
    main_menu = MainMenu()
    main_menu.activate()

    # Window Loop
    while True:
        pygame.display.get_surface().fill("black")
        if main_menu.active:
            # Menu loop
            main_menu.tick()
            main_menu.draw()
        else:
            if main_menu.game_round.active:
                # Game loop
                main_menu.game_round.global_tick()
                main_menu.game_round.global_draw()
            elif main_menu.game_round.end_function == 'menu':
                main_menu = MainMenu()
                main_menu.activate()
            elif main_menu.game_round.end_function == 'next':
                main_menu.continue_game()
        if debugger:
            screen.blit(pygame.font.SysFont('minecraftten', 25).render("%.1f" % clock.get_fps(),
                                                                       True,
                                                                       'pink'),
                        (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

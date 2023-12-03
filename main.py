import pygame.display
from gameplay import *
# from data.saves.save import SaveManager


def main():
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Five Nights At Lone Peak High')
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
            # Game loop
            main_menu.game_round.global_tick()
            main_menu.game_round.global_draw()
        if debugger:
            screen.blit(pygame.font.SysFont('minecraftten', 25).render("%.1f" % clock.get_fps(),
                                                                       True,
                                                                       'pink'),
                        (0, 0))
        pygame.display.update()
        clock.tick(120)


if __name__ == "__main__":
    main()

import pygame.display
from gameplay import *


def main():
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption('Five Nights At Lone Peak High')
    clock = pygame.time.Clock()
    game_round = Game()
    debugger = True
    game_round.start()

    while True:
        game_round.global_tick()
        screen.fill('black')
        game_round.global_draw()
        if debugger:
            screen.blit(pygame.font.SysFont('minecraftten', 25).render("%.1f" % clock.get_fps(),
                                                                       True, 'pink'),
                        (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

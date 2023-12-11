import pygame.display
from gameplay import *
from data.saves.save import SaveManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption('Five Nights At Lone Peak High')
    pygame.display.set_icon(pygame.image.load('resources/ui/icon.png').convert())
    clock = pygame.time.Clock()
    game_round = Game()
    debugger = True
    game_round.start()
    save_manager = SaveManager()

    while True:
        game_round.global_tick()
        screen.fill('black')
        game_round.global_draw()
        if debugger:
            screen.blit(pygame.font.SysFont('minecraftten', 25).render("%.1f" % clock.get_fps(),
                                                                       True,
                                                                       'pink'),
                        (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

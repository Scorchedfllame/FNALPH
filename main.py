from sys import exit
from gameplay import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Five Nights At Lone Peak')
    clock = pygame.time.Clock()
    test_surface = pygame.image.load('resources/backgrounds/offices/test.png').convert()
    game = Game()

    while True:
        game.global_tick()

        screen.fill('black')
        game.global_draw()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

import pygame
from sys import exit
from gameplay import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    pygame.display.set_caption('Five Nights At Lone Peak')
    clock = pygame.time.Clock()
    test_surface = pygame.image.load('resources/backgrounds/offices/test.png').convert()
    jumpscare_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(jumpscare_timer, 4000)
    x_pos = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == jumpscare_timer:
                x_pos = 0

        screen.fill('black')
        screen.blit(test_surface, (x_pos, 0))
        x_pos += 1

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

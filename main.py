# import gc
import pygame.display
import pygame_widgets
from gameplay import *
# from data.saves.save import SaveManager
# import time


def fade_image(image: pygame.surface.Surface, screen: pygame.surface.Surface, len_dir: range, color=False):
    for i in len_dir:
        img = image.copy()
        black = pygame.surface.Surface((1920, 1080))
        black.fill((0, 0, 0))
        black.set_alpha(i)
        screen.blit(img, (0, 0))
        if color:
            img.fill((207, 0, 7), special_flags=pygame.BLEND_RGB_MULT)
            img.set_alpha(i)
            screen.blit(img, (0, 0))
        screen.blit(black, (0, 0))
        pygame.display.flip()


def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.set_num_channels(64)
    pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption('Five Nights At Lone Peak High')
    pygame.display.set_icon(pygame.image.load('resources/ui/icon.png').convert())
    loading_image = pygame.image.load('resources/ui/menus/main_menu/LogoLoadingScreen.png').convert_alpha()
    background_sound = pygame.mixer.Sound('resources/sounds/main_menu.mp3')
    fade_image(loading_image, pygame.display.get_surface(), range(255, 0, -1))
    pygame.display.get_surface().blit(loading_image, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    menus = [MainMenu(), Options(0), Cheat(1), Credits(1)]
    game = Game()
    save_manager = SaveManager()
    active_menu = menus[0]
    active_menu.start()
    playing = False
    fade_image(loading_image, pygame.display.get_surface(), range(255), True)
    save_manager.load_data()
    background_sound.play(loops=-1)
    for i in range(64):
        pygame.mixer.Channel(i).set_volume(save_manager.data['volume']/100)

    # Window Loop
    while True:
        pygame.display.get_surface().fill("black")
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == MENU_CHANGE:
                if event.func == 'menu':
                    save_manager.load_data()
                    background_sound.play(loops=-1)
                    for i in range(64):
                        pygame.mixer.Channel(i).set_volume(save_manager.data['volume']/100)
                    playing = False
                    active_menu = menus[0]
                    active_menu.start()
                elif event.func == 'next':
                    menus[0].continue_game()
                elif event.func == 'change':
                    active_menu.stop()
                    active_menu = menus[event.target]
                    active_menu.start()
                elif event.func == 'continue_game':
                    for i in range(0, 255):
                        black = pygame.surface.Surface((1920, 1080))
                        black.set_alpha(i)
                        pygame.display.get_surface().blit(black, (0, 0))
                        pygame.display.flip()
                        clock.tick(60)
                    playing = True
                    game.start()
                elif event.func == 'start_game':
                    background_sound.fadeout(4000)
                    for i in range(0, 255):
                        black = pygame.surface.Surface((1920, 1080))
                        black.set_alpha(i)
                        menus[0].draw(pygame.display.get_surface())
                        pygame.display.get_surface().blit(black, (0, 0))
                        pygame.display.flip()
                        clock.tick(60)
                    playing = True
                    game.start()
                elif event.func == 'go_background':
                    menus[0].cheat_background()
                elif event.func == 'end_background':
                    menus[0].end_cheat_background()
            if playing:
                game.global_tick(event)
            else:
                active_menu.tick(event)
        if playing:
            game.global_draw()
        else:
            active_menu.draw(pygame.display.get_surface())
        pygame_widgets.update(events)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

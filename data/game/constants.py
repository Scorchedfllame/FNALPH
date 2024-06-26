# Mainly events used for the transfer of information form animatronics to game logic and vice versa
import pygame

# Events

#   Timers
PUPPET_TIMER = pygame.USEREVENT + 1
BONNIE_TIMER = pygame.USEREVENT + 5
CHICA_TIMER = pygame.USEREVENT + 12
KNIGHT_TIMER = pygame.USEREVENT + 13
LEFTY_TIMER = pygame.USEREVENT + 14
UPDATE_POWER = pygame.USEREVENT + 7
GAME_TIMER = pygame.USEREVENT + 16
POWER_PENALTY = pygame.USEREVENT + 17
CLOCK = pygame.USEREVENT + 9
CAMERA_ROTATION = pygame.USEREVENT + 11
FOXY_DOOR = pygame.USEREVENT + 15
HITCH_TIMER = pygame.USEREVENT + 19
RANDOM_EVENT_SOUND = pygame.USEREVENT + 22

#   General
CAMERA_FLIPPED_UP = pygame.USEREVENT + 3
CAMERA_FLIPPED_DOWN = pygame.USEREVENT + 4
ACTIVATE_CAMERA = pygame.USEREVENT + 8
MUTE_TIME = pygame.USEREVENT + 18
MENU_CHANGE = pygame.USEREVENT + 21

#   Game States
KILL = pygame.USEREVENT + 2
POWER_OUT = pygame.USEREVENT + 6
WIN = pygame.USEREVENT + 10
POWER_RESET = pygame.USEREVENT + 20

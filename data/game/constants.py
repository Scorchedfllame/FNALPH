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
CLOCK = pygame.USEREVENT + 9
CAMERA_ROTATION = pygame.USEREVENT + 11
FOXY_DOOR = pygame.USEREVENT + 15

#   General
CAMERA_FLIPPED_UP = pygame.USEREVENT + 3
CAMERA_FLIPPED_DOWN = pygame.USEREVENT + 4
ACTIVATE_CAMERA = pygame.USEREVENT + 8

#   Game States
KILL = pygame.USEREVENT + 2
BLACKOUT = pygame.USEREVENT + 6
WIN = pygame.USEREVENT + 10

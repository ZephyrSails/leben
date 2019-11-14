from game.game import Game
from game.utils import Action
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
import pygame


def pressed_keys_to_actions():
    moves = set([])
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_UP]:
        moves.add(Action.F)
    if pressed_keys[K_DOWN]:
        moves.add(Action.B)
    if pressed_keys[K_LEFT]:
        moves.add(Action.L)
    if pressed_keys[K_RIGHT]:
        moves.add(Action.R)
    return moves


def human_player():
    game = Game()
    while game.running:
        game.update(pressed_keys_to_actions())

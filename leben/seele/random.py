from game.game import Game
from game.utils import Action
import random


def random_select_action():
    return set([Action(random.randint(0, len(Action) - 1))])


def random_player():
    game = Game()
    while game.running:
        game.update(random_select_action())

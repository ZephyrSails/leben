from game.main import Game
from game.utils import Action
import random


def random_select_action():
    return Example(random.randint(0, len(Example) - 1))


def main():
    game = Game()
    while game.running:
        game.update(random_select_action())


if __name__ == "__main__":
    main()

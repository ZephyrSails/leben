import argparse
from seele.human import human_player
from seele.random import random_player

parser = argparse.ArgumentParser()
parser.add_argument(
    '--seele', type=str, help='who controls the game: [human, random]')



if __name__ == "__main__":
    args = parser.parse_args()

    if args.seele == "human":
        human_player()
    elif args.seele == "random":
        random_player()

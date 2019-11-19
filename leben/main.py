import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--seele',
    type=str,
    help='Who controls the game? See main.py about options')

if __name__ == "__main__":
    args = parser.parse_args()

    if args.seele == "human":
        from seele.human import human_player
        human_player()
    elif args.seele == "random":
        from seele.random import random_player
        random_player()
    elif args.seele == "rulebase":
        from seele.rulebase import rulebase_player
        rulebase_player()

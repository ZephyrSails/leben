import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--seele',
    type=str,
    help='Who controls the game? See main.py about options')
parser.add_argument(
    '--mode',
    type=str,
    default="eval"
    help='eval or train mode')

def evaluate(args):
    if args.seele == "human":
        from seele.human import human_player
        human_player()
    elif args.seele == "random":
        from seele.random import random_player
        random_player()
    elif args.seele == "rulebase":
        from seele.rulebase import rulebase_player
        rulebase_player()

if __name__ == "__main__":
    args = parser.parse_args()

    if args.help == "eval":
        evaluate(args)
    if args.help == "train":
        
        pass

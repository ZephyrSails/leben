import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--seele',
                    type=str,
                    default="human",
                    help='Who controls the game? See main.py about options')
parser.add_argument('--mode',
                    type=str,
                    default="eval",
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
    elif args.seele == "reinforcement_simplified":
        from seele.reinforcement_simplified import reinforcement_player
        reinforcement_player()


if __name__ == "__main__":
    args = parser.parse_args()

    if args.mode == "eval":
        evaluate(args)
    if args.mode == "train":
        if args.seele == "reinforcement_simplified":
            from seele.reinforcement_simplified import train, NeuralNetwork
            model = NeuralNetwork()
            train(model)
        if args.seele == "reinforcement_residual":
            from seele.reinforcement_residual import train, NeuralNetwork
            model = NeuralNetwork()
            train(model)
            pass

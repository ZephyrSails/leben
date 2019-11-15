from game.game import Game, Action
import random


def rulebase_actions(vision):
    objs = list(map(lambda a: a != (0, 0, 0), vision))
    length = len(objs)
    middle_idx_l = length // 2 - length // 20
    middle_idx_r = length // 2 + length // 20
    middle_objs = objs[middle_idx_l:middle_idx_r]
    left_objs = objs[:middle_idx_l]
    right_objs = objs[middle_idx_r:length]

    actions = set([])

    # Have something in the middle of the view, go forward
    if sum(middle_objs) > 0:
        actions.add(Action.F)

    # See which direction has more objs, go to that direction
    if sum(left_objs) > sum(right_objs):
        actions.add(Action.L)
    elif sum(right_objs) > sum(left_objs):
        actions.add(Action.R)

    if len(actions) > 0:
        return actions

    # When no actions can be made, backward and make one random action
    actions.add(Action.B)
    actions.add(Action(random.randint(0, len(Action) - 1)))
    return actions


def rulebase_player():
    game = Game()
    while game.running:
        game.update(rulebase_actions(game.get_1d_vision(100)))

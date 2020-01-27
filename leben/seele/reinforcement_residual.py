import torch
from torch import nn
from torch.nn import functional as F
from game.game import Game, Action
from seele.rulebase import rulebase_actions
import numpy as np
import random
import time
import sys

VISION_RESOLUION = 126


def reinforcement_player():
    model = NeuralNetwork()
    model.load_state_dict(
        torch.load("pretrained_model/residual/current_model_175000.pt"))
    model.cpu()
    model.eval()
    game = Game()
    while game.running:
        state, _reward, _terminal = get_model_state(game)
        output = model(state)
        game.update(set([idx_2_action(output_2_action_argmax_idx(output))]))


def rulebase_teacher(game):
    actions = rulebase_actions(game.get_1d_vision(126))
    action_list = [action.value for action in actions]
    return random.sample(action_list, 1)[0]


def random_teacher(model):
    return random.randint(0, model.number_of_actions - 1)


def output_2_distribution(output):
    return nn.functional.softmax(output, dim=0)


def output_2_action_idx(output):
    distribution = output_2_distribution(output)
    return torch.multinomial(distribution, 1).item()


def output_2_action_argmax_idx(output):
    return torch.torch.argmax(output).item()


def idx_2_action(index):
    return Action(index)


def init_output():
    return torch.tensor([[1 / len(Action)] * len(Action)])


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        self.number_of_actions = 4
        self.gamma = 0.99
        self.final_epsilon = 0.001
        self.initial_epsilon = 0.2
        self.number_of_iterations = 5000000
        self.replay_memory_size = 10000
        self.minibatch_size = 32

        self.conv1 = nn.Conv1d(4, 32, 8, 4)
        self.conv2 = nn.Conv1d(32, 64, 4, 2)
        self.conv3 = nn.Conv1d(64, 64, 3, 1)
        self.fc4 = nn.Linear(768, 124)
        self.fc5 = nn.Linear(128, self.number_of_actions)

    def forward(self, state, last_out):
        out = self.conv1(state)
        out = F.relu(out, inplace=True)
        out = self.conv2(out)
        out = F.relu(out, inplace=True)
        out = self.conv3(out)
        out = F.relu(out, inplace=True)
        out = out.view(out.size()[0], -1)
        out = self.fc4(out)
        out = F.relu(out, inplace=True)
        out = torch.cat((out, last_out), 1)
        out = self.fc5(out)

        return out


def get_model_state(game):
    vision = game.get_1d_vision_binary(VISION_RESOLUION)
    hp, reward = game.get_state()
    vision = torch.tensor(vision).float()
    hp = torch.tensor([hp]).float()
    reward = torch.tensor([reward]).float()
    state = torch.cat((vision, hp, reward)).unsqueeze(0)
    state = torch.cat((state, state, state, state)).unsqueeze(0).float()
    return state, reward, 0


def train(model):
    start = time.time()
    model.train()
    if torch.cuda.is_available():  # put on GPU if CUDA is available
        model = model.cuda()
    # define Adam optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    # initialize mean squared error loss
    criterion = nn.MSELoss()

    # instantiate game
    game = Game()

    # initialize replay memory
    replay_memory = []

    # initial action is do nothing
    action = torch.zeros([model.number_of_actions], dtype=torch.float32)
    action[0] = 1

    state, _reward, _terminal = get_model_state(game)

    # initialize epsilon value
    epsilon = model.initial_epsilon
    iteration = 0

    epsilon_decrements = np.linspace(model.initial_epsilon,
                                     model.final_epsilon,
                                     model.number_of_iterations)
    output = init_output()
    if torch.cuda.is_available():
        output = output.cuda()
    # main infinite loop
    while iteration < model.number_of_iterations:
        if torch.cuda.is_available():  # put on GPU if CUDA is available
            state = state.cuda()
        # get output from the neural network
        last_output = output.clone().detach()
        output = model(state, last_output)
        output_val = output[0]
        # initialize action
        action = torch.zeros([model.number_of_actions], dtype=torch.float32)
        if torch.cuda.is_available():  # put on GPU if CUDA is available
            action = action.cuda()

        # epsilon greedy exploration
        use_teacher = random.random() <= epsilon

        # teacher_action_index = rulebase_teacher(game)
        teacher_action_index = random_teacher(model)
        model_action_index = output_2_action_idx(output_val)
        action_index = teacher_action_index if use_teacher else model_action_index

        action[action_index] = 1
        # get next state and reward
        game.update(set([idx_2_action(action_index)]))
        state_1, reward, terminal = get_model_state(game)

        action = action.unsqueeze(0)
        reward = torch.from_numpy(np.array([reward],
                                           dtype=np.float32)).unsqueeze(0)

        # save transition to replay memory
        replay_memory.append(
            (state, action, reward, state_1, terminal, last_output, output))
        # if replay memory is full, remove the oldest transition
        if len(replay_memory) > model.replay_memory_size:
            replay_memory.pop(0)

        # epsilon annealing
        epsilon = epsilon_decrements[iteration]
        # sample random minibatch
        minibatch = random.sample(
            replay_memory, min(len(replay_memory), model.minibatch_size))

        # unpack minibatch
        state_batch = torch.cat(tuple(d[0] for d in minibatch))
        action_batch = torch.cat(tuple(d[1] for d in minibatch))
        reward_batch = torch.cat(tuple(d[2] for d in minibatch))
        state_1_batch = torch.cat(tuple(d[3] for d in minibatch))
        last_output_batch = torch.cat(tuple(d[5] for d in minibatch))
        next_output_batch = torch.cat(tuple(d[6] for d in minibatch))

        if torch.cuda.is_available():  # put on GPU if CUDA is available
            state_batch = state_batch.cuda()
            action_batch = action_batch.cuda()
            reward_batch = reward_batch.cuda()
            state_1_batch = state_1_batch.cuda()
            last_output_batch = last_output_batch.cuda()
            next_output_batch = next_output_batch.cuda()

        # get output for the next state
        # TODO what the hack? why this work?
        output_1_batch = model(state_1_batch, next_output_batch)

        # set y_j to r_j for terminal state, otherwise to r_j + gamma*max(Q)
        y_batch = torch.cat(
            tuple(reward_batch[i] if minibatch[i][4] else reward_batch[i] +
                  model.gamma * torch.max(output_1_batch[i])
                  for i in range(len(minibatch))))

        # extract Q-value
        q_value = torch.sum(model(state_batch, last_output_batch) *
                            action_batch,
                            dim=1)

        # PyTorch accumulates gradients by default, so they need to be reset in each pass
        optimizer.zero_grad()

        # returns a new Tensor, detached from the current graph, the result will never require gradient
        y_batch = y_batch.detach()

        # TODO: Why model not being updated
        # calculate loss
        loss = criterion(q_value, y_batch)

        # do backward pass
        loss.backward()
        # print("loss:", loss, q_value, y_batch)
        optimizer.step()

        # set state to be state_1
        state = state_1

        iteration += 1

        if iteration % 25000 == 0:
            torch.save(
                model.state_dict(),
                "pretrained_model/residual/current_model_" + str(iteration) +
                ".pt")
        dist = output_2_distribution(output_val)
        print(
            "\riter: {} time: {:0.2f} epsilon: {:0.6f} action: {} reward: {:0.2f} Qmax: {:0.4f} isT:{},TA{},MA{} F:{:0.2f},B:{:0.2f},L:{:0.2f},R:{:0.2f} {}"
            .format(iteration,
                    time.time() - start, epsilon, action_index,
                    reward.numpy()[0][0],
                    np.max(output_val.cpu().detach().numpy()),
                    "T" if use_teacher else "F", teacher_action_index,
                    model_action_index, dist[0], dist[1], dist[2], dist[3],
                    game.leben.get_status_str()),
            end='')
        sys.stdout.flush()

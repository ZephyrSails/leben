import torch
from torch import nn
from game.game import Game, Action
import numpy as np

VISION_RESOLUION = 126


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        self.number_of_actions = len(Action)
        self.gamma = 0.99
        self.final_epsilon = 0.0001
        self.initial_epsilon = 0.1
        self.number_of_iterations = 2000000
        self.replay_memory_size = 10000
        self.minibatch_size = 32

        self.conv1 = nn.Conv1d(4, 32, 8, 4)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv1d(32, 64, 4, 2)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv3 = nn.Conv1d(64, 64, 3, 1)
        self.relu3 = nn.ReLU(inplace=True)
        self.fc4 = nn.Linear(768, 128)
        self.relu4 = nn.ReLU(inplace=True)
        self.fc5 = nn.Linear(128, self.number_of_actions)

    def forward(self, state):
        out = self.conv1(state)
        out = self.relu1(out)
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.conv3(out)
        out = self.relu3(out)
        out = out.view(out.size()[0], -1)
        out = self.fc4(out)
        out = self.relu4(out)
        out = self.fc5(out)

        return out


def train(model, start):
    print("define Adam optimizer")
    # define Adam optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-6)

    print("initialize mean squared error loss")
    # initialize mean squared error loss
    criterion = nn.MSELoss()

    print("instantiate game")
    # instantiate game
    game = Game()

    print("initialize replay memory")
    # initialize replay memory
    replay_memory = []

    print("initial action is do nothing")
    # initial action is do nothing
    action = torch.zeros([model.number_of_actions], dtype=torch.float32)
    action[0] = 1

    vision = game.get_1d_vision(VISION_RESOLUION)
    hp, curr_delta = game.get_state()
    vision = torch.tensor(vision)
    hp = torch.tensor([hp])
    curr_delta = torch.tensor([curr_delta])
    state = torch.cat((vision, hp, curr_delta))

    print("initialize epsilon value")
    # initialize epsilon value
    epsilon = model.initial_epsilon
    iteration = 0

    epsilon_decrements = np.linspace(
        model.initial_epsilon, model.final_epsilon, model.number_of_iterations)

    print("main infinite loop")
    # main infinite loop
    while iteration < model.number_of_iterations:
        print("get output from the neural network")
        # get output from the neural network
        output = model(state)[0]
        print("initialize action")
        # initialize action
        action = torch.zeros([model.number_of_actions], dtype=torch.float32)
        if torch.cuda.is_available():  # put on GPU if CUDA is available
            action = action.cuda()
        print("epsilon greedy exploration")
        # epsilon greedy exploration
        random_action = random.random() <= epsilon
        if random_action:
            print("Performed random action!")
        action_index = [
            torch.randint(
                model.number_of_actions, torch.Size([]), dtype=torch.int)
            if random_action else torch.argmax(output)
        ][0]

        if torch.cuda.is_available():  # put on GPU if CUDA is available
            action_index = action_index.cuda()

        action[action_index] = 1
        print("get next state and reward")
        # get next state and reward
        image_data_1, reward, terminal = game_state.frame_step(action)
        image_data_1 = resize_and_bgr2gray(image_data_1)
        image_data_1 = image_to_tensor(image_data_1)
        state_1 = torch.cat((state.squeeze(0)[1:, :, :],
                             image_data_1)).unsqueeze(0)

        action = action.unsqueeze(0)
        reward = torch.from_numpy(np.array([reward],
                                           dtype=np.float32)).unsqueeze(0)

        print("save transition to replay memory")
        # save transition to replay memory
        replay_memory.append((state, action, reward, state_1, terminal))
        print("if replay memory is full, remove the oldest transition")
        # if replay memory is full, remove the oldest transition
        if len(replay_memory) > model.replay_memory_size:
            replay_memory.pop(0)

        print("epsilon annealing")
        # epsilon annealing
        epsilon = epsilon_decrements[iteration]
        print("sample random minibatch")
        # sample random minibatch
        minibatch = random.sample(
            replay_memory, min(len(replay_memory), model.minibatch_size))

        print("unpack minibatch")
        # unpack minibatch
        state_batch = torch.cat(tuple(d[0] for d in minibatch))
        action_batch = torch.cat(tuple(d[1] for d in minibatch))
        reward_batch = torch.cat(tuple(d[2] for d in minibatch))
        state_1_batch = torch.cat(tuple(d[3] for d in minibatch))

        if torch.cuda.is_available():  # put on GPU if CUDA is available
            state_batch = state_batch.cuda()
            action_batch = action_batch.cuda()
            reward_batch = reward_batch.cuda()
            state_1_batch = state_1_batch.cuda()

        print("get output for the next state")
        # get output for the next state
        output_1_batch = model(state_1_batch)

        print(
            "set y_j to r_j for terminal state, otherwise to r_j + gamma*max(Q)"
        )
        # set y_j to r_j for terminal state, otherwise to r_j + gamma*max(Q)
        y_batch = torch.cat(
            tuple(reward_batch[i] if minibatch[i][4] else reward_batch[i] +
                  model.gamma * torch.max(output_1_batch[i])
                  for i in range(len(minibatch))))

        print("extract Q-value")
        # extract Q-value
        q_value = torch.sum(model(state_batch) * action_batch, dim=1)

        print(
            "PyTorch accumulates gradients by default, so they need to be reset in each pass"
        )
        # PyTorch accumulates gradients by default, so they need to be reset in each pass
        optimizer.zero_grad()

        print(
            "returns a new Tensor, detached from the current graph, the result will never require gradient"
        )
        # returns a new Tensor, detached from the current graph, the result will never require gradient
        y_batch = y_batch.detach()

        print("calculate loss")
        # calculate loss
        loss = criterion(q_value, y_batch)

        print("do backward pass")
        # do backward pass
        loss.backward()
        optimizer.step()

        print("set state to be state_1")
        # set state to be state_1
        state = state_1
        iteration += 1

        if iteration % 25000 == 0:
            torch.save(
                model,
                "pretrained_model/current_model_" + str(iteration) + ".pth")

        print("iteration:", iteration, "elapsed time:",
              time.time() - start, "epsilon:", epsilon, "action:",
              action_index.cpu().detach().numpy(), "reward:",
              reward.numpy()[0][0], "Q max:",
              np.max(output.cpu().detach().numpy()))

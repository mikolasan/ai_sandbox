
import copy
import torch
import random
import numpy as np
from attention.model import Attention
from collections import deque
from game import SnakeGameAI, Direction, Point, BOARD_SIZE
from model import DQN, SnakeDQN
from helper import plot
from replay import ReplayMemory, Transition
import math

STATE_LAYERS = 1 # snake, food
TIME_SEQUENCE = 3 # to understand direction

N_HIDDEN_NEURONS = 32
N_HIDDEN_NEURONS_2 = 12
N_ACTIONS = 3

N_GAMES_FULL_EXPLORATION = 100

MAX_MEMORY = 100_000
BATCH_SIZE = 10000
LR = 0.0005

class DeepAgent:

    def __init__(self):
        self.n_games = 0
        self.n_moves = 0
        self.epsilon = 0.8 # randomness
        self.gamma = 0.95 # discount rate was 0.95
        self.memory = ReplayMemory(MAX_MEMORY)
        self.buffer = deque([], maxlen=200)
        
        input_size = 10 #BOARD_SIZE * BOARD_SIZE * STATE_LAYERS
        self.input_size = input_size
        layer_size = [TIME_SEQUENCE * input_size, N_HIDDEN_NEURONS, N_HIDDEN_NEURONS_2, N_ACTIONS]
        self.policy_net = DQN(layer_size)
        self.target_net = DQN(layer_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.trainer = SnakeDQN(self.policy_net, self.target_net, lr=LR, gamma=self.gamma)
        self.time_seq = torch.zeros(TIME_SEQUENCE, input_size)
    
    def make_time_seq(self, state, save=False):
        new_seq = torch.tensor(self.time_seq)
        if self.n_moves < TIME_SEQUENCE:
            new_seq[self.n_moves, :] = state
        else:
            new_seq = torch.roll(new_seq, -1, 0)
            # new_seq[:2, :] = new_seq[1:3, :]
            new_seq[TIME_SEQUENCE - 1, :] = state
        if save:
            self.time_seq = new_seq
        return new_seq.flatten()

    def remember(self, *args):
        self.buffer.append(Transition(*args))
        # self.memory.push(*args)
    
    def train_long_memory(self):
        self.time_seq = torch.zeros(TIME_SEQUENCE, self.input_size)
        self.n_moves = 0
        
        if len(self.buffer) > 0:
            total_reward = 0.0
            for t in self.buffer:
                total_reward += t.reward
            print(f'Total reward: {total_reward}')
            # if total_reward > -50.0:
            #     p = random.random()
            #     if p > 0.3:
            #         self.buffer.clear()
            #         return
            for t in self.buffer:
                self.memory.memory.append(t)
            self.buffer.clear()
        
        if len(self.memory) < BATCH_SIZE:
            return
    
        transitions = self.memory.sample(BATCH_SIZE)
        # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
        # detailed explanation). This converts batch-array of Transitions
        # to Transition of batch-arrays.
        batch = Transition(*zip(*transitions))
        self.trainer.train_from_game(batch, BATCH_SIZE)
        
        if len(self.memory) > 100000:
            print("FORGET!!!")
            self.memory.clear()

    def get_action(self, state: torch.Tensor, game):
        # random moves: tradeoff exploration / exploitation
        min_games = N_GAMES_FULL_EXPLORATION
        if self.n_games > min_games:
            self.epsilon = 0.05 + (min_games / self.n_games) * 0.95 * 0.8
        # else:
        #     return game.get_action()
        
        p = random.random()
        action = torch.zeros((N_ACTIONS), dtype=torch.long)
        if p < self.epsilon: # reducing probalility of being random #was 200
            move = random.randint(0, N_ACTIONS - 1)
            # print(f'random move ({p}) {move}')
            action[move] = 1
        else:
            # print('USE MODEL')
            with torch.no_grad():
                state_u = state.unsqueeze(0)
                q = self.policy_net(state_u)
                idx = q.max(1).indices.item()
                action[idx] = 1
            # print(f'predicted move {move} from {prediction}')
        
        return action

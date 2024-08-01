
import copy
import torch
import random
import numpy as np
from attention.model import Attention, TIME_SEQUENCE
from attention.trainer import AttentionTrainer
from collections import deque
from game import SnakeGameAI, Direction, Point, BOARD_SIZE
from helper import plot
from replay import ReplayMemory, Transition
import math


N_ACTIONS = 4

N_GAMES_FULL_EXPLORATION = 500

MAX_MEMORY = 100_000
BATCH_SIZE = 100
LR = 0.0001


def insert_tensor(orig, move, state):
    new_seq = torch.tensor(orig)
    l = len(state)
    if move < TIME_SEQUENCE:
        new_seq[move * l: (move + 1) * l] = state
    else:
        new_seq = torch.roll(new_seq, -l)
        new_seq[-l:] = state
    return new_seq


class AttentionAgent:

    def __init__(self):
        self.n_games = 0
        self.n_moves = 0
        self.epsilon = 0.8 # randomness
        self.gamma = 0.99 # discount rate was 0.95
        self.memory = ReplayMemory(MAX_MEMORY)
        self.buffer = deque([], maxlen=200)
        
        input_size = BOARD_SIZE * BOARD_SIZE
        self.input_size = input_size
        self.policy_net = Attention(1, input_size, TIME_SEQUENCE, N_ACTIONS)
        self.target_net = Attention(1, input_size, TIME_SEQUENCE, N_ACTIONS)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.trainer = AttentionTrainer(self.policy_net, self.target_net, lr=LR, gamma=self.gamma)
        self.q_seq = torch.zeros(TIME_SEQUENCE * input_size)
        self.k_seq = torch.zeros(TIME_SEQUENCE * input_size)
    
    def make_time_seq(self, state, save=False):
        q_seq = insert_tensor(self.q_seq, self.n_moves, state[:35])
        k_seq = insert_tensor(self.k_seq, self.n_moves, state[36:])
        if save:
            self.q_seq = q_seq
            self.k_seq = k_seq
        return torch.cat((q_seq.flatten(), k_seq.flatten()))

    def remember(self, *args):
        self.buffer.append(Transition(*args))
        # self.memory.push(*args)
    
    def train_long_memory(self):
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
                
                q = self.policy_net(state)
                idx = q.max(1).indices.item()
                action[idx] = 1
            # print(f'predicted move {move} from {prediction}')
        
        return action

import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point, BOARD_SIZE
from helper import plot
from replay import ReplayMemory, Transition
import math

MAX_MEMORY = 100_000
N_ACTIONS = 3

class QuAgent:
    def __init__(self):
        self.transitions = torch.tensor((BOARD_SIZE * BOARD_SIZE, N_ACTIONS))
        self.n_games = 0
        self.n_moves = 0
        self.epsilon = 0.8 # randomness
        self.gamma = 0.97 # discount rate was 0.95
        self.memory = ReplayMemory(MAX_MEMORY)
    
    def make_time_seq(self, state, save=False):
        return state
    
    def remember(self, *args):
        self.memory.push(*args)
    
    def train_long_memory(self):
        self.train()
        
        self.n_moves = 0
        
        if len(self.memory) > 100000:
            print("FORGET!!!")
            self.memory.clear()
    
    def train(self):
        pass
    
    def convert_state(self, state):
        return state
    
    def get_action(self, state: torch.Tensor, game):
        # random moves: tradeoff exploration / exploitation
        min_games = 500
        if self.n_games > min_games:
            self.epsilon = 0.1 + (1.0 / self.n_games) * min_games * 0.9 * 0.8
        # else:
        #     return game.get_action()
        
        p = random.random()
        action = torch.zeros((3), dtype=torch.long)
        if p < self.epsilon: # reducing probalility of being random #was 200
            move = random.randint(0, 2)
            # print(f'random move ({p}) {move}')
            action[move] = 1
        else:
            # print('USE MODEL')
            p = self.transitions[state]
            action_id = p.max(1).indices.item()
            action[action_id] = 1
            # print(f'predicted move {move} from {prediction}')
        
        return action
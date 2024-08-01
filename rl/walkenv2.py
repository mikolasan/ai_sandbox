from enum import Enum
import torch
import random


UP = [1,0,0,0]
LEFT = [0,1,0,0]
RIGHT = [0,0,1,0]
DOWN = [0,0,0,1]

N_ACTIONS = 4

BOARD_SIZE = 6
MAX_STEPS = 100

class WalkEnvModelFree:
    def __init__(self):
        self.position = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
        # self.position = None
        self.target = None
        self.board = None
        self.score = 0
        self.reset()
    
    def reset(self):
        self.board = torch.zeros((BOARD_SIZE, BOARD_SIZE))
        self.target = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
        while self.target == self.position:
            self.target = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
        self.steps = 0
        # self.score = 0
    
    def play_step(self, action_tensor):
        # self.score = self.steps
        self.steps += 1
        action = action_tensor.tolist()
        reward = 0
        pos = self.position
        if action == UP:
            if pos[1] - 1 < 0:
                reward = -1
            else:
                pos[1] -= 1
        elif action == LEFT:
            if pos[0] - 1 < 0:
                reward = -1
            else:
                pos[0] -= 1
        elif action == RIGHT:
            if pos[0] + 1 >= BOARD_SIZE:
                reward = -1
            else:
                pos[0] += 1
        elif action == DOWN:
            if pos[1] + 1 >= BOARD_SIZE:
                reward = -1
            else:
                pos[1] += 1
        else:
            raise Exception("impossible action")
        
        if pos == self.target:
            reward = 1.0
            game_over = True
        else:
            game_over = reward < 0 or self.steps > MAX_STEPS
        
        if reward < 0:
            self.score = 0
        else:
            self.score += 1
    
        return reward, game_over, self.score
            
    def get_current_state(self):
        agent = torch.zeros((BOARD_SIZE, BOARD_SIZE))
        agent[self.position[0], self.position[1]] = 1.0
        
        target = torch.zeros((BOARD_SIZE, BOARD_SIZE))
        target[self.target[0], self.target[1]] = 1.0
        return torch.cat((agent.flatten(), target.flatten()))
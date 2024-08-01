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

class WalkEnv:
    def __init__(self):
        self.position = None
        self.target = None
        self.board = None
        self.score = 0
        self.reset()
    
    def reset(self):
        self.board = torch.zeros((BOARD_SIZE, BOARD_SIZE))
        self.position = [random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)]
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
        pos = self.position
        dx = pos[0] - self.target[0]
        dy = pos[1] - self.target[1]
        wall_left = 1.0 if pos[0] - 1 < 0 else 0.0
        wall_right = 1.0 if pos[0] + 1 < 0 else 0.0
        wall_up = 1.0 if pos[1] - 1 >= BOARD_SIZE else 0.0
        wall_down = 1.0 if pos[1] + 1 >= BOARD_SIZE else 0.0
        state = [dx, dy,
                 wall_left, wall_right, wall_up, wall_down]
        return torch.tensor(state)
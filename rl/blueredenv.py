from enum import Enum
import torch
import random


RED = [1,0]
BLUE = [0,1]

N_ACTIONS = 2

class BlueRedEnv:
    def __init__(self):
        self.selected_color = None
        self.reset()
    
    def reset(self):
        colors = [BLUE, RED]
        self.selected_color = random.choice(colors)
        self.steps = 0
        self.score = 0
    
    def play_step(self, action_tensor):
        self.steps += 1
        action = action_tensor.tolist()
        reward = 0
        if action == BLUE:
            if self.selected_color == RED:
                reward = 1.0
                self.score += 1
                self.selected_color = BLUE
            else:
                reward = -1.0
        elif action == RED:
            if self.selected_color == BLUE:
                reward = 1.0
                self.score += 1
                self.selected_color = RED
            else:
                reward = -1.0
        else:
            raise Exception("impossible action")
        
        game_over = self.steps > 100
        return reward, game_over, self.score
            
    def get_current_state(self):
        return torch.tensor(self.selected_color)
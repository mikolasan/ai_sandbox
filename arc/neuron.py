import math
import random

import torch
import torch.nn as nn
import torch.optim as optim

import matplotlib.pyplot as plt
import matplotlib.cm as cm

class NeuronWithThreshold:
    def __init__(self, pos, 
                 field_height,
                 field_width,
                 column_height, 
                 column_width, 
                 n_dendrites, 
                 n_synapses,
                 threshold=4.0):
        self.pos = pos
        self.max_pos_y = field_height
        self.max_pos_x = field_width
        self.column_height = column_height
        self.column_width = column_width
        self.n_dendrites = n_dendrites
        self.n_synapses = n_synapses
        self.threshold = threshold
        
        n_post_neurons = column_height * (column_width * column_width)
        # n = n_post_neurons * n_dendrites * n_synapses
        
        # self.weight = torch.randn((1, n_post_neurons))
        self.weight = torch.full((1, n_post_neurons), 0.1)
        self.accum_y = torch.zeros_like(self.weight)
        
        self.learning_rate = 0.05

    def i_to_neuron_pos(self, i):
        if self.column_width % 2 == 0:
            # no neuron on the same position above the current one
            start_pos = - (self.column_width // 2) + 1
        else:
            start_pos = - (self.column_width // 2)
        
        fix_x = 0
        fix_y = 0
        
        # if start_pos + self.pos[0] < 0:
        #     # start_pos + self.pos[0] + fix_x = 0
        #     fix_x = -(start_pos + self.pos[0])
        # elif start_pos + self.pos[0] + self.column_width >= self.max_pos_x:
        #     # start_pos + self.pos[0] + fix_x = self.max_pos_x - 1 - self.column_width
        #     fix_x = -(start_pos + self.pos[0]) + self.max_pos_x - 1 - self.column_width
            
        # if start_pos + self.pos[1] < 0:
        #     fix_y = -(start_pos + self.pos[1])
        # elif start_pos + self.pos[1] + self.column_width >= self.max_pos_y:
        #     fix_y = -(start_pos + self.pos[1]) + self.max_pos_y - 1 - self.column_width
        
        #print("fix", fix_x, fix_y)
        level = i // (self.column_width * self.column_width)
        level_i = i % (self.column_width * self.column_width)
        
        return (start_pos + self.pos[0] + fix_x + level_i % self.column_width,
                start_pos + self.pos[1] + fix_y + level_i // self.column_width,
                level)
        # if level < 1:
        #     # first level
        #     return (start_pos + self.pos[0] + i % self.column_width,
        #             start_pos + self.pos[1] + i // self.column_width,
        #             0)
        # else:
        #     # not the first level
        #     # print(i, level, "not the first level")
        #     level_i = i % (self.column_width * self.column_width)
        #     return (start_pos + self.pos[0] + level_i % self.column_width,
        #             start_pos + self.pos[1] + level_i // self.column_width,
        #             level)
    
    def forward(self, x):
        """
        x is a scalar.
        It basically indicates if this column is activated or not.
        and if it is then it works as a multiplier 
        (maybe important during summation and threshold within an activation function)
        
        The output is an array of neurons across this column
        """
        y = x * self.weight + self.accum_y
        self.accum_y = y
        return torch.relu(y - self.threshold)

    def reset(self):
        self.accum_y = torch.zeros_like(self.weight)

    def update_weights(self, x, y):
        """
        propagate negative diff to weights
        reduce threshold
        """
        oja_diff = y * (x - y * self.weight)
        total_diff = oja_diff.sum()
        if total_diff != 0.0:
            print(f'update \'{self.pos}\' : {total_diff}')
        self.weight += self.learning_rate * oja_diff
import math
import random

import torch
import torch.nn as nn
import torch.optim as optim

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from neuron import NeuronWithThreshold

class Network:
    def __init__(self,
                 field_height,
                 field_width,
                 column_height,
                 column_width
                 ):
        self.field_height = field_height
        self.field_width = field_width
        self.column_height = column_height
        self.column_width = column_width
        
        self.neurons = []

        n_dendrites = 12 # some of them are in the column width but some can lie outside
        n_synapses = 4 # possible duplicate connections between pre-synaptic axon and post-synaptic dendrites

        for h in range(column_height):
            self.neurons.append([])
            for x in range(field_width):
                for y in range(field_height):
                    neuron = NeuronWithThreshold(
                        (x, y, h),
                        field_height=field_height,
                        field_width=field_width,
                        column_height=column_height,
                        column_width=column_width,
                        n_dendrites=n_dendrites,
                        n_synapses=n_synapses,
                        threshold=0.2
                    )
                    self.neurons[h].append(neuron)
    
    def forward(self, level, input_data):
        y_total = torch.zeros(self.column_height, self.field_width, self.field_height)

        for n in self.neurons[level]:
            xx = input_data[level][n.pos[0], n.pos[1]]
            y = n.forward(xx)
            for i in range(y.shape[1]):
                p = n.i_to_neuron_pos(i)
                if p[0] < 0 or p[0] >= self.field_width or p[1] < 0 or p[1] >= self.field_height:
                    continue
                y_total[p[2], p[0], p[1]] += y[0,i]
        
        return y_total
        
    def train(self, train_data):
        for h in range(self.column_height):
            y_total = self.forward(h, train_data)
            train_data.append(y_total[h])
            self.update(h, train_data, y_total)
            
    
    def update(self, level, input_data, y_total):
        n_column_neurons = self.column_width * self.column_width * self.column_height
        
        for n in self.neurons[level]:
            xx = input_data[level][n.pos[0], n.pos[1]]
            yy = torch.zeros(1, n_column_neurons)
            for i in range(n_column_neurons):
                p = n.i_to_neuron_pos(i)
                if p[0] < 0 or p[0] >= self.field_width or p[1] < 0 or p[1] >= self.field_height:
                    continue
                yy[0, i] = y_total[p[2], p[0], p[1]]

            n.update_weights(xx, yy)
    
    def test(self, test_data):
        y = self.forward(0, test_data)
        return y
    
    def test_chain(self, test_data, chain):
        states = []
        for l, active_level in enumerate(chain):
            y = self.forward(active_level, test_data)
            next_level = chain[l+1] if l < len(chain) - 1 else chain[-1]
        test_data.append(y[next_level])
        states.append(y.clone().detach())
        return states
    
    def plot_level_activations(self, y_total, level):
        plt.figure(figsize=(4, 4))
        x_mat = plt.imshow(y_total[level], cmap=cm.coolwarm)
        plt.colorbar(x_mat)
        plt.title("Activation on layer 3")
        plt.tight_layout()
        plt.show()
        
    def plot_avg_activations(self, y_total):
        plt.figure(figsize=(4, 4))
        x_mat = plt.imshow(torch.mean(y_total, dim=0), cmap=cm.coolwarm)
        plt.colorbar(x_mat)
        plt.title("Activation on layer 3")
        plt.tight_layout()
        plt.show()
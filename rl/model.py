import copy
import math
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import random
from collections import deque


class DQN(nn.Module):
    def __init__(self, sizes):
        super(DQN, self).__init__()
        in_states, h1_nodes, h2_nodes, out_actions = sizes
        self.layer1 = nn.Linear(in_states, h1_nodes)
        self.layer2 = nn.Linear(h1_nodes, h2_nodes)
        # self.layer3 = nn.Linear(100, h2_nodes)
        self.layer4 = nn.Linear(h2_nodes, out_actions)
         
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        # x = F.tanh(self.layer3(x))
        x = self.layer4(x)
        return x
        
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)



class SnakeDQN: # needs changing... episodes as a param?
    def __init__(self, policy_net, target_net, lr, gamma, device):
        self.device = device
        self.lr = lr   # 0.001         # learning rate (alpha)
        self.gamma = gamma
        self.policy_net = policy_net
        self.target_net = target_net
        # self.optimizer = optim.Adam(policy_net.parameters(), lr=0.1, weight_decay=1e-2)
        self.optimizer = optim.Adam(policy_net.parameters(), lr=lr)
        # self.optimizer = optim.SGD(policy_net.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.loss_vals = []
        self.q_vals = []

    def get_avg_q(self):
        if len(self.q_vals) > 0:
            return sum(self.q_vals) / len(self.q_vals)
        else:
            return 0.0
    
    def retrieve_avg_loss(self):
        if len(self.loss_vals) > 0:
            return sum(self.loss_vals) / len(self.loss_vals)
        else:
            return 0.0
        
    def train_from_game(self, batch, batch_size):
        
        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                            batch.next_state)), dtype=torch.bool, device=self.device)
        non_final_next_states = [s.unsqueeze(0) for s in batch.next_state if s is not None]
        if len(non_final_next_states) > 0:
            non_final_next_states = torch.cat(non_final_next_states)
            
        state_batch = torch.stack(batch.state)
        action_batch = torch.stack(batch.action)
        reward_batch = torch.stack(batch.reward)
        
        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        q = self.policy_net(state_batch)
        a = action_batch.max(1).indices.view(batch_size, 1)
        state_action_values = q.gather(1, a)
        # state_action_values = state_action_values.clip(min=-1.0, max=1.0)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1).values
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(batch_size, device=self.device)
        if len(non_final_next_states) > 0:
            with torch.no_grad():
                v = self.target_net(non_final_next_states)
                next_state_values[non_final_mask] = v.max(1).values
        # Compute the expected Q values
        expected_state_action_values = (next_state_values.unsqueeze(1) * self.gamma) + reward_batch
        # expected_state_action_values = expected_state_action_values.clip(min=-1.0, max=1.0)

        # print(expected_state_action_values)
        # loss = torch.mean(torch.zeros((batch_size, 1), requires_grad=True)) #
        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values)
        # loss = self.criterion(state_action_values, expected_state_action_values)

        # Optimize the model
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()
        
        self.loss_vals.append(loss.item())
        
        TAU = 0.8
        target_net_state_dict = self.target_net.state_dict()
        policy_net_state_dict = self.policy_net.state_dict()
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        self.target_net.load_state_dict(target_net_state_dict)

        with torch.no_grad():
            new_q = self.target_net(state_batch)
            self.q_vals.append(torch.mean(new_q).item())


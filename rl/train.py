
import torch
import random
import numpy as np
from collections import deque
from agent import DeepAgent, BATCH_SIZE
from attention.agent import AttentionAgent
from game import SnakeGameAI, Direction, Point, BOARD_SIZE
from model import DQN, SnakeDQN
from blueredenv import BlueRedEnv
from walkenv import WalkEnv
from walkenv2 import WalkEnvModelFree
from helper import plot, hist
import math


# if GPU is to be used
device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

plot_score = []
plot_q = []
plot_duration = []
plot_loss = []
total_score = 0
record = 0
episodes_length = []

agent = AttentionAgent()
# agent = DeepAgent()
# agent = QuAgent()
# game = SnakeGameAI()
# game = BlueRedEnv()
game = WalkEnvModelFree()

 
def on_game_done(reward, score):
    # train long memory, plot result
    n_moves = agent.n_moves
    game.reset()
    agent.n_games += 1
    global record
    if score > record:
        record = score
        # agent.target_net.save()

    print('Game', agent.n_games, 'Reward', reward, 'Score', score, 'Record:', record)
    agent.train_long_memory()


    plot_score.append(score)
    plot_duration.append(n_moves)
    plot_q.append(agent.trainer.get_avg_q())
    agent.trainer.q_vals = []
    
    plot_loss.append(agent.trainer.retrieve_avg_loss())
    agent.trainer.loss_vals = []
    
    # if agent.n_games % 1000 == 0:
    #     plot(plot_score, plot_loss, plot_q)

    hist(episodes_length)
    
    starting_state = game.get_current_state()
    return starting_state


def step(state):

    state_to_save = agent.make_time_seq(state, save=True)
    agent.n_moves += 1
    
    # get move
    action = agent.get_action(state_to_save, game)
    
    # perform move and get new state
    reward, done, score = game.play_step(action)
    # print(f'step reward {reward}')
    
    if done:
        new_state = None
        new_state_to_save = None
    else:
        new_state = game.get_current_state()
        new_state_to_save = agent.make_time_seq(new_state)


    agent.remember(state_to_save, action, new_state_to_save, torch.tensor([reward]))
    # agent.remember(state, action, new_state, torch.tensor([reward]))
    
    if done:
        return new_state, True, reward, score
    return new_state, False, reward, 0


if __name__ == '__main__':
    state = game.get_current_state()
    
    # while agent.n_games < 10:
    while True:
        state, game_done, reward, play_score = step(state)
        # if agent.n_moves > 40*(play_score+1):
        #     game_done = True
        if game_done:
            state = on_game_done(reward, play_score)

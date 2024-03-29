import random

N = 5
M = 5


class World(object):
  def __init__(self):
    # self.grid = [['_']*N]*M # array copies are bad
    self.grid = [[0]*N for _ in range(M)]
    self.add_food_randomly()    
  
  def add_food_randomly(self):
    x_r = random.randint(0, N)
    y_r = random.randint(0, M)
    self.grid[x_r][y_r] = 'f'
    print(f'added food to ({x_r}, {y_r})')

  def reward(self, x, y):
    if self.grid[x][y] == 'f':
      return 1
    else:
      return -0.5

  def apply_action(self, agent, action):
    x = agent.state['x_pos']
    y = agent.state['y_pos']
    no_effect = {"agent": ""}
    bad_effect = {"agent": "hit the wall"}
    if (x < 0 or x >= N or y < 0 or y >= M):
      effect = bad_effect
    elif self.grid[x][y] == 'f':
      effect = {"agent": "found food"}
      self.grid[x][y] = '_'
      self.add_food_randomly()
    else:
      effect = no_effect
    return effect
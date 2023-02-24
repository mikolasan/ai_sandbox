import random

N = 5
M = 5


class World(object):
  grid = [['_']*N]*M
  
  def add_food_randomly(self):
    x_r = random.randint(0, N)
    y_r = random.randint(0, M)
    self.grid[x_r][y_r] = 'f'

  def reward(self, x, y):
    if self.grid[x][y] == 'f':
      return 1
    else:
      return -0.5

  def apply_action(self, agent, action):
    no_effect = {"agent": ""}
    bad_effect = {"agent": "alive = False"}
    if (agent.x_pos < 0 or agent.x_pos >= N
        or agent.y_pos < 0 or agent.y_pos >= M):
      effect = bad_effect
    else:
      effect = no_effect
    return effect
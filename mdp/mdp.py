import random
from actions import Actions

class MDP(object):
  # current proprtion bewtween exploration and exploitation
  # 1 = full exploration
  # 0 = full exploitation
  epsilon = 1.0 
  transitions = []
  reward = 0
  states = []
  prev_action = None
  
  def __init__(self, world):
    for y in range(0, len(world.grid)):
      for x in range(0, len(world.grid[y])):
        self.states.append({
          "pos": (x, y),
          "id": len(self.states),
        })
  
  # def decide_on_next_action(self, agent, world):
  #   return self.actions["go right"]
  
  def decide_on_next_action(self, agent, world):
    x = agent.state['x_pos']
    y = agent.state['y_pos']
    if x == 0 and y == 0:
      print('rule: if you see a wall, then turn left')
      action = Actions.go_down
    elif x == 0 and y == len(world.grid) - 1:
      print('rule: if you see a wall, then turn left')
      action = Actions.go_right
    elif y == 0 and x == len(world.grid[y]) - 1:
      print('rule: if you see a wall, then turn left')
      action = Actions.go_left
    elif y == len(world.grid) - 1 and x == len(world.grid[y]) - 1:
      print('rule: if you see a wall, then turn left')
      action = Actions.go_up
    elif self.epsilon > 0.5:
      # random action
      print('random action')
      all_actions = []
      if y < len(world.grid) - 1:
        all_actions.append(Actions.go_down)
      if y > 0:
        all_actions.append(Actions.go_up)
      if x < len(world.grid[y]) - 1:
        all_actions.append(Actions.go_right)
      if x > 0: 
        all_actions.append(Actions.go_left)

      r = random.randint(0, len(all_actions) - 1)
      return all_actions[r]
      # return self.prev_action
    
    self.prev_action = action
    return self.prev_action

class MDP(object):
  def __init__(self) -> None:
    pass
  
  transitions = []
  reward = 0
  states = {} # ?
  actions = {
    "go left": "x_pos -= 1",
    "go right": "x_pos += 1",
    "go up": "y_pos -= 1",
    "go down": "y_pos += 1",
  }
  prev_action = None
  
  # def decide_on_next_action(self, agent, world):
  #   return self.actions["go right"]
  
  def decide_on_next_action(self, agent, world):
    
    # if you see a wall, then turn left
    x = agent.x_pos
    y = agent.y_pos
    if x == 0 and y == 0:
      action = self.actions["go down"]
    elif x == 0 and y == len(world.grid) - 1:
      action = self.actions["go right"]
    elif y == 0 and x == len(world.grid[y]) - 1:
      action = self.actions["go left"]
    elif y == len(world.grid) - 1 and x == len(world.grid[y]) - 1:
      action = self.actions["go up"]
    else:
      return self.prev_action
    
    self.prev_action = action
    return self.prev_action
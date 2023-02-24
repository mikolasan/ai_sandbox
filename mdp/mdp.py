
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
  
  def decide_on_next_action(self, agent, world):
    return self.actions["go left"]
from mdp import MDP

class Agent(object):
  alive = True
  model = MDP()
  x_pos = 0
  y_pos = 0
  
  def decide_on_next_action(self, world):
    action = self.model.decide_on_next_action(self, world)
    return action
  
  def apply_action(self, action):
    if action == "x_pos -= 1":
      self.x_pos -= 1
    elif action == "x_pos += 1":
      self.x_pos += 1
    elif action == "y_pos -= 1":
      self.y_pos -= 1
    elif action == "y_pos += 1":
      self.y_pos += 1
    else:
      print('action does not apply')
  
  def apply_effect(self, effect):
    if effect["agent"] == "alive = False":
      print('smashed the head against a wall')
      self.alive = False
    else:
      print('effect does not apply')
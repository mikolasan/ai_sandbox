from actions import Actions
from mdp import MDP
    
class Agent(object):
  alive = True
  x_pos = 0
  y_pos = 0
  
  def __init__(self, world):
    self.model = MDP(world)
    
  def decide_on_next_action(self, world):
    action = self.model.decide_on_next_action(self, world)
    return action
  
  def apply_action(self, action):
    if action == Actions.go_left:
      self.x_pos -= 1
    elif action == Actions.go_right:
      self.x_pos += 1
    elif action == Actions.go_up:
      self.y_pos -= 1
    elif action == Actions.go_down:
      self.y_pos += 1
    else:
      print('action does not apply')
  
  def apply_effect(self, effect):
    if effect["agent"] == "hit the wall":
      print('smashed the head against a wall')
      self.alive = False
    elif effect["agent"] == "found food":
      print('found food')
    else:
      print('effect does not apply')
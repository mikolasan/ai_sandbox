
class World(object):
  grid = [[0]*3]
  
  def apply_action(self, action):
    effect = {"agent": "alive = False"}
    return effect
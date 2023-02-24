
N = 5
M = 5

class World(object):
  grid = [[0]*N]*M
  
  def apply_action(self, agent, action):
    no_effect = {"agent": ""}
    bad_effect = {"agent": "alive = False"}
    if (agent.x_pos < 0 or agent.x_pos >= N
        or agent.y_pos < 0 or agent.y_pos >= M):
      effect = bad_effect
    else:
      effect = no_effect
    return effect
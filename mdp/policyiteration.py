"""
Read this: http://incompleteideas.net/book/ebook/node41.html
Wrong (?): https://medium.com/@ngao7/markov-decision-process-policy-iteration-42d35ee87c82
"""
import random


class PolicyIteration:
  def __init__(self, states, actions, reward_func, transition_func):
    self.states = states
    self.actions = actions
    self.reward_func = reward_func
    self.transition_func = transition_func
    self.values = dict(zip(self.states, [0] * len(self.states))) # all zeroes
    self.policy = dict(zip(self.states, random.choices(self.actions, k=4))) # random actions
    self.discount = 0.9 # usually denoted as gamma
    self.convergence_threshold = 0.1 # usually denoted as theta
    
  def evaluate_policy(self, max_iter=50):
    i = 0
    delta = self.convergence_threshold + 1
    while i < max_iter and delta > self.convergence_threshold:
      i += 1
      delta = 0
      for state in self.states:
        old_value = self.values[state]
        action = self.policy[state]
        new_value = self.value(state, action)
        self.values[state] = new_value
        delta = max(delta, abs(old_value - new_value))
      print(f'eval {i}, delta {delta}')
    return delta
  
  def improve_policy(self):
    policy_changed = False
    for state in self.states:
      old_action = self.policy[state]
      action_value = dict(zip(self.actions, [0] * len(self.actions)))
      for action in self.actions:
        action_value[action] = self.value(state, action)
      print(f'from state {state} test new actions {action_value}')
      new_action = max(action_value, key=action_value.get) # argmax
      self.policy[state] = new_action
      policy_changed = policy_changed or (new_action != old_action)
    return policy_changed
  
  def value(self, state, action):
    new_value = 0
    for _state in self.states:
      prob = self.transition_func(state, action, _state)
      reward = self.reward_func(state, action, _state)
      # new_value += reward + self.discount * prob* self.values[_state]
      print(f' + {prob * (reward + self.discount * self.values[_state])} (p={prob}, r={reward}, g={self.discount}, v={self.values[_state]}')
      new_value += prob * (reward + self.discount * self.values[_state])
    return new_value
      
  def iterate(self, max_epoch=500):
    print(f'initial values {self.values}')
    print(f'initial policy {self.policy}')
    epoch = 0
    while epoch < max_epoch:
      epoch += 1
      print(f'epoch {epoch}')
      delta = self.evaluate_policy()
      print(f'evaluate policy {self.values} (delta={delta})')
      changed = self.improve_policy()
      print(f'improve policy {self.policy}')
      if not changed:
        break


if __name__ == '__main__':
  def reward(s, a, _s):
    if s == 3:
      return 10 / (a + 1)
    else:
      return -20
  
  def transition_model(s, a, _s):
    if abs(s - _s) == a:
      return 1
    return 0

  solver = PolicyIteration(
    states=[3,4,5,6], 
    actions=[0,1,2],
    reward_func=reward,
    transition_func=transition_model)
  
  solver.iterate()
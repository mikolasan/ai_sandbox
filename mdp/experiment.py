import time
from agent import Agent
from world import World


def main():
  """
  https://medium.com/@ngao7/markov-decision-process-basics-3da5144d3348
  https://medium.com/@ngao7/markov-decision-process-value-iteration-2d161d50a6ff
  """
  agent = Agent()
  world = World()
  
  iter = 0
  while agent.alive:
    print('')
    print(f'iteration {iter}')
    
    action = agent.decide_on_next_action(world)
    print(f'next action: {action}')
    agent.apply_action(action)
    print(f'agent position ({agent.x_pos}, {agent.y_pos})')
    effect = world.apply_action(agent, action)
    agent.apply_effect(effect)
    
    iter += 1
    print('...')
    time.sleep(1)
    
  print(f'agent died on iteration {iter}')


if __name__ == "__main__":
  main()
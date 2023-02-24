from agent import Agent
from world import World


def main():
  agent = Agent()
  world = World()
  
  iter = 0
  while agent.alive:
    print(f'iteration {iter}')
    action = agent.decide_on_next_action(world)
    print(f'next action: {action}')
    agent.apply_action(action)
    effect = world.apply_action(action)
    agent.apply_effect(effect)
    iter += 1
    
  print(f'agent died on iteration {iter}')


if __name__ == "__main__":
  main()
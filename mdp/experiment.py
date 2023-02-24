from agent import Agent
from world import World


def main():
  agent = Agent()
  world = World()
  
  while agent.alive:
    action = agent.decide_on_next_action(world)
    agent.apply_action(action)
    effect = world.apply_action(action)
    agent.apply_effect(effect)


if __name__ == "__main__":
  main()
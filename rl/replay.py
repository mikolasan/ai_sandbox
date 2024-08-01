from collections import deque, namedtuple
import random

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    
    def clear(self):
        l = self.memory.maxlen
        self.memory = deque([], maxlen=l)

    # def consequtive(self, )

    def __len__(self):
        return len(self.memory)
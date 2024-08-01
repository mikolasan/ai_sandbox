

import matplotlib.pyplot as plt
from IPython import display
import numpy as np

plt.ion()

def plot(score, q, duration):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    # plt.plot(score)
    # plt.plot(q)
    plt.plot(duration)
    # plt.ylim(ymin=0)
    plt.text(len(score)-1, score[-1], str(score[-1]))
    # plt.text(len(moves)-1, moves[-1], str(moves[-1]))

    #plt.plot(regression_line)

    plt.show(block=False)
    plt.pause(.1)


def hist(episodes_length):
    n, bins, patches = plt.hist(episodes_length, 
                                bins=50, density=True, alpha=0.75)

    plt.xlabel('Data')
    plt.ylabel('Probability')
    plt.title('Histogram of Data')
    plt.grid(True)
    plt.show()
    plt.pause(.1)
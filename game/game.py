import sys
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
import math
from leben import Leben, Move
from matplotlib.patches import Wedge


class LebenGame():
    def __init__(self):
        self.leben = Leben()

    def move(self, move):
        pass


def press(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'Up':
        visible = xl.get_visible()
        xl.set_visible(not visible)
        main.canvas.draw()
    elif event.key == 'Down':
        visible = xl.get_visible()
        xl.set_visible(not visible)
        main.canvas.draw()
    elif event.key == 'Left':
        visible = xl.get_visible()
        xl.set_visible(not visible)
        main.canvas.draw()
    elif event.key == 'Right':
        visible = xl.get_visible()
        xl.set_visible(not visible)
        main.canvas.draw()


# Fixing random state for reproducibility
np.random.seed(19680801)

main, ax = plt.subplots()

main.canvas.mpl_connect('key_press_event', press)

ax.plot(np.random.rand(12), np.random.rand(12), 'go')
xl = ax.set_xlabel('easy come, easy go')
ax.set_title('Press a key')

Wedge((x1, y1), r, t1, t2)
plt.show()

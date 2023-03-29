import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update(num):
    # generate new data
    x = np.random.rand(100)
    y = np.random.rand(100)
    z = np.random.rand(100)

    # update scatter plot
    ax.clear()
    ax.scatter(x, y, z)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)

ani = FuncAnimation(fig, update, frames=range(5), interval=100)

plt.show()

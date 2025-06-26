import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('macosx')
from .upper_connections import UPPER_CONNECTIONS  # <-- Only this line is changed
from mpl_toolkits.mplot3d import Axes3D

# Specify the connections between points (indices)
connections = UPPER_CONNECTIONS

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def plot_connections(points):
    ax.clear()
    for i, connection in enumerate(connections):
        if connection in ((0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (5, 27), (4, 6)):
            color = "green"
            dot_color = "red"
        else:
            color = "blue"
            dot_color = "black"
        ax.plot([points[connection[0], 0], points[connection[1], 0]],
                [points[connection[0], 2], points[connection[1], 2]],
                [-points[connection[0], 1], -points[connection[1], 1]], color=color)
        ax.scatter(points[connection[0], 0], points[connection[0], 2], -points[connection[0], 1], color=dot_color)
        ax.scatter(points[connection[1], 0], points[connection[1], 2], -points[connection[1], 1], color=dot_color)

    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_zlabel('Y')

    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.5, 0.1)
    ax.set_zlim(-0.5, 0.1)

    plt.show(block=False)
    plt.pause(0.001)
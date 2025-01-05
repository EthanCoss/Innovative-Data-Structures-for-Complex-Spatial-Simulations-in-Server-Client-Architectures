import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import numpy as np
import cst


def actualiser_positions():
    nouvelles_positions = []
    for entity in entities.values():
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        nouvelles_positions.append((entity.position.x, entity.position.y))
    return nouvelles_positions


def init():
    positions = actualiser_positions()
    scatter.set_offsets(positions)
    return (scatter,)


def update(frame):
    positions = actualiser_positions()
    scatter.set_offsets(np.array(positions))
    return (scatter,)


def start(entity_list, xlim=(-1_000_000, 1_000_000), ylim=(-1_000_000, 1_000_000)):

    fig, ax = plt.subplots()
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_title("Real time map of entities")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    global scatter
    global entities
    entities = entity_list
    scatter = ax.scatter([], [], c="blue", s=50)

    ani = FuncAnimation(
        fig, update, init_func=init, frames=100, interval=cst.TPS, blit=True
    )

    plt.show()

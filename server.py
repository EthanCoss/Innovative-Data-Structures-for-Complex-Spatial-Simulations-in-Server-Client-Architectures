import threading
import time
import socket

from game.space import Space
from connexion.listener import listener
import cst
from game.TPS import TPS

from master_variables import *
import real_time

host = "127.0.0.1"
port = 65432


def main_init():
    space = Space()
    if draw_initial_bubble_tree:
        space.draw_initial_bubble_tree()

    tps = TPS(space)
    TPS_loop_thread = threading.Thread(target=tps.TPS_loop)
    listerner_loop = threading.Thread(target=listener)

    listerner_loop.start()
    TPS_loop_thread.start()
    if visualize:
        real_time.start(
            space.entities,
            xlim=(-3 * 149_597_870_700, 3 * 149_597_870_700),
            ylim=(-3 * 149_597_870_700, 3 * 149_597_870_700),
        )

    listerner_loop.join()
    TPS_loop_thread.join()


if __name__ == "__main__":
    main_init()

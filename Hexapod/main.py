#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Libraries
import time    #https://docs.python.org/fr/3/library/time.html
from Robot import Robot
from datetime import datetime as dt
import numpy as np

# function init 
def init():
    # robot.control_board.test_servos()
    pass


# function main 
def main():
    robot = Robot()

    while True():
        robot.tick()
    # robot.control_board.test_servos()

    # robot.move_leg_from_point_to_point(np.array[10, 10, -5], np.array(10, -10, -5), 3)

if __name__ == '__main__':
    init()
    main()
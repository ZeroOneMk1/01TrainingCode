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
    # robot.control_board.test_servos()
    time.sleep(5)
    for i in range(23):
        robot.move_leg_to_position(0, [0, 0, -38.5+i])
        time.sleep(0.5)
    time.sleep(2)
    robot.loosen()

    # robot.move_leg_from_point_to_point(np.array[10, 10, -5], np.array(10, -10, -5), 3)

if __name__ == '__main__':
    init()
    main()
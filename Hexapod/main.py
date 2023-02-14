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
    robot = Robot(13.50515, 18.4576)
    # robot.control_board.test_servos()
    # time.sleep(5)
    # for i in range(23):
    #     robot.move_leg_to_position(0, [0, 0, -38.5+i])
    #     time.sleep(0.5)

    h = -15
    w = 30
    l = 30

    robot.move_leg_to_position(0, [-w, l, h])

    robot.move_leg_to_position(1, [-w, 0, 2*h])

    robot.move_leg_to_position(2, [-w, -l, h])

    robot.move_leg_to_position(3, [w, l, 2*h])

    robot.move_leg_to_position(4, [w, 0, h])

    robot.move_leg_to_position(5, [w, -l, 2*h])
    time.sleep(10)

    robot.loosen()

    # robot.move_leg_from_point_to_point(np.array[10, 10, -5], np.array(10, -10, -5), 3)

if __name__ == '__main__':
    init()
    main()
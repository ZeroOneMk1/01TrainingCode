#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Libraries
import time    #https://docs.python.org/fr/3/library/time.html
from Robot import Robot
from datetime import datetime as dt
import numpy as np

# function main 
def main():
    robot = Robot(13.50515, 18.4576)

    robot.reset_leg_positions()

    # h = -20
    # w = 20
    # l = 20

    # # i=0

    # for i in range(150):
    #     robot.move_leg_to_position(0, [-w+i/10, l, h])

    #     robot.move_leg_to_position(1, [-w+i/10, 0, h])

    #     robot.move_leg_to_position(2, [-w+i/10, -l, h])

    #     robot.move_leg_to_position(3, [w+i/10, l, h])

    #     robot.move_leg_to_position(4, [w+i/10, 0, h])

    #     robot.move_leg_to_position(5, [w+i/10, -l, h])
    #     time.sleep(0.02)

    # time.sleep(5)

    for i in range(60):
        robot.tick()
        # time.sleep(0.1)

    robot.loosen()

    # robot.move_leg_from_point_to_point(np.array[10, 10, -5], np.array(10, -10, -5), 3)

if __name__ == '__main__':
    main()
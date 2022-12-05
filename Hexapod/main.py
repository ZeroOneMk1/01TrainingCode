#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Libraries
import time    #https://docs.python.org/fr/3/library/time.html
from Robot import Robot

# function init 
def init():
    robot = Robot()
    robot.control_board.test_servos()


# function main 
def main():
    pass


if __name__ == '__main__':
    init()
    main()
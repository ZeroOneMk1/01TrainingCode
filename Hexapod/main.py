#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Libraries
import time    #https://docs.python.org/fr/3/library/time.html
from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/
from ControlBoard import ControlBoard

# function init 
def init():
    pass


# function main 
def main():

    pcaScenario()


# function pcaScenario 
def pcaScenario():

    control_board = ControlBoard(1)

    """Scenario to test servo"""
    for i in range(control_board.nbPCAServo):
        for j in range(control_board.MIN_ANG[i],control_board.MAX_ANG[i],10):
            print("Send angle {} to Servo {}".format(j,i))
            control_board.servos[i].angle = j
            time.sleep(.5)
        for j in range(control_board.MAX_ANG[i],control_board.MIN_ANG[i],-10):
            print("Send angle {} to Servo {}".format(j,i))
            control_board.servos[i].angle = j
            time.sleep(.5)
        control_board.servos[i].angle=None #disable channel
        time.sleep(0.5)




if __name__ == '__main__':
    init()
    main()
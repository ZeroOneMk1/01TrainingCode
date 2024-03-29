#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Libraries
import time  # https://docs.python.org/fr/3/library/time.html
from adafruit_servokit import ServoKit # https://circuitpython.readthedocs.io/projects/servokit/en/latest/
import random as rd

class ControlBoard:

    # class init
    def __init__(self, num_servos: int, min_imp: int = 500, max_imp: int = 2500, min_ang: int = 0, max_ang: int = 180):

        # Constants
        self.nbPCAServo = num_servos

        # Parameters
        self.MIN_IMP = [min_imp for _ in range(num_servos)]
        self.MAX_IMP = [max_imp for _ in range(num_servos)]
        self.MIN_ANG = [min_ang for _ in range(num_servos)]
        self.MAX_ANG = [max_ang for _ in range(num_servos)]

        # Objects


        if self.nbPCAServo <= 16:
            self.pca = ServoKit(channels=16)

            self.servos = []

            for i in range(self.nbPCAServo):
                self.servos.append(self.pca.servo[i])
        
        elif self.nbPCAServo < 32:
            self.pca = ServoKit(channels=16)
            self.pca_two = ServoKit(channels=16, address=0x41) # TODO TEST IF IT HAS A DIFFERENT INDEX.

            self.servos = [] # TODO TEST IF THIS EVEN WORKS IN THE WAY I THINK IT DOES

            for i in range(0, 16):
                self.servos.append(self.pca.servo[i])

            for i in range(16, self.nbPCAServo):
                self.servos.append(self.pca_two.servo[i - 16])

        else:
            print("Can't hold this many servos right now. Sorry.")
            exit()

        for i in range(self.nbPCAServo):
            self.servos[i].set_pulse_width_range(
                self.MIN_IMP[i], self.MAX_IMP[i])


    def set_leg_servo_positions(self, leg_index: int, desired_position) -> None:
        """Given the index of the leg, and the desired position as a NumPy array of degree angles, sets the servos to the desired position."""
        
        zero_servo = 3*leg_index

        for i in range(3):
            self.servos[zero_servo + i].angle = desired_position[i]

            # TODO test if the servo's 0 positions align with what I imagine them to be at.

    def test_servos(self):

        """Scenario to test servo"""
        # self.servos[0].angle = 90
        # time.sleep(.5)
        
        # self.servos[1].angle = 90
        # time.sleep(.5)

        # self.servos[2].angle = 180
        # time.sleep(2)
        # for i in range(5):
        for j in range(6):
            self.servos[3*j].angle = 90
        # for k in range(5):
        for l in range(6):
            self.servos[3*l+1].angle = 0

        for m in range(5):
            for n in range(6):
                self.servos[3*n+2].angle = m * 45
        # time.sleep(1)   

        # for servo in self.servos:
        #     servo.angle = 0
        # time.sleep(1)
        for servo in self.servos:
            servo.angle=None

        # self.servos[2].angle=None #disable channel        
        # self.servos[1].angle=None
        # self.servos[0].angle=None
from Leg import Leg
# from ControlBoard import ControlBoard
import numpy as np
from time import sleep
from datetime import datetime as dt
import pygame
import math

class Robot:
    def __init__(self, hip_x, hip_y) -> None:
        self.legs = []
        self.hip_x = hip_x
        self.hip_y = hip_y

        self.legs.append(Leg(0, np.array([-hip_x, hip_y, 0]), 135)) # Front Left Leg
        self.legs.append(Leg(1, np.array([-hip_x, 0, 0]), 180)) # Center Left Leg
        self.legs.append(Leg(2, np.array([-hip_x, -hip_y, 0]), 225)) # Back Left Leg
        self.legs.append(Leg(3, np.array([hip_x, hip_y, 0]), 45)) # Front Right Leg
        self.legs.append(Leg(4, np.array([hip_x, 0, 0]), 0)) # Center Right Leg
        self.legs.append(Leg(5, np.array([hip_x, -hip_y, 0]), 315)) # Back Right Leg

        self.current_leg_positions = np.asarray([(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)])
        self.next_leg_positions = np.asarray([(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)])

        self.left_tripod = [self.legs[0], self.legs[2], self.legs[4]]
        self.right_tripod = [self.legs[1], self.legs[3], self.legs[5]]

        self.grounded_legs = self.left_tripod
        self.lifted_legs = self.right_tripod

        # self.control_board = ControlBoard(3)
    
    def move_leg_to_position(self, leg_index: int, desired_position) -> None:
        reachable, servo_positions = self.legs[leg_index].calculate_all_all_servo_positions(desired_position)
        if not reachable:
            print("Not Reachable!")
            return
        for i in range(len(servo_positions)):
            servo_positions[i] = np.clip(servo_positions[i], 0, 180)
        # self.control_board.set_leg_servo_positions(leg_index, servo_positions)
        self.legs[leg_index].position = desired_position # ! Maybe this fucks with data types, check if I could make it more consistent
    
    def move_legs_from_current_to_next(self, time:float):
        """Goes from self.current to self.next positions, time is in seconds"""

        start = dt.now()
        end = start + dt.timedelta(seconds=time)
        now = dt.now()

        # self.move_leg_to_position(leg.index, destination)
        # sleep(5) # ? remember why this was important. Remove if it works fine while commented.

        substeps = 0

        while now < end:
            substeps += 1

            for leg in self.legs:

                line = np.asarray(self.next_leg_positions[leg.index]) - np.asarray(self.current_leg_positions[leg.index])

                destination = self.next_leg_positions[leg.index]

                t = dt.now() - start
                t_sec = t.total_seconds()
                destination = np.asarray(np.asarray(self.current_leg_positions[leg.index]) + line * t_sec / time)
                self.move_leg_to_position(leg.index, destination)
        
        for leg in self.legs:
            self.move_leg_to_position(leg.index, self.next_leg_positions[leg.index])

        print(f"Number of substeps: {substeps}")

    def reset_leg_positions(self):
        self.reset_lifted_tripod()
        self.swap_tripods()
        self.reset_lifted_tripod()

    def tick(self):
        controller_input = self.get_controller_input()
        self.calculate_new_leg_positions(controller_input)
        self.move_legs_from_current_to_next()
        for i in range(len(self.current_leg_positions)):
            self.current_leg_positions[i] = self.next_leg_positions[i] # ! May have errors when next gets changed
        sleep(1/50)
    
    def get_controller_input(self):
        return np.asarray((0, 1)) # TODO actually set up the controller instead of just giving X=0 Y=1

    def calculate_new_leg_positions(self, input: tuple) -> None:
        if self.shift_lifted_leg_positions(input):
            self.shift_grounded_leg_positions(input)
        else:
            self.swap_legs()
    
    def swap_legs(self):
        self.grounded_legs, self.lifted_legs = self.lifted_legs, self.grounded_legs # ! Does this work with lists of objects in python? Or does this cause a pointer error?

    def shift_lifted_leg_positions(self, input: tuple) -> bool:
        d = self.get_COM_distance()

        if d == -1:
            return False
        
        for leg in self.lifted_legs:
            self.shift_leg_position(leg.index, input, d - 50) # TODO Tune d via different functions
        
        return True
    
    def shift_grounded_leg_positions(self, input: tuple) -> None:        
        for leg in self.grounded_legs:
            self.shift_leg_position(leg.index, input, -50)

    def shift_leg_position(self, leg_index: int,  vector: tuple, height: float) -> None:
        self.next_leg_positions[leg_index][0] = self.current_leg_positions[leg_index][0] + vector[0]
        self.next_leg_positions[leg_index][1] = self.current_leg_positions[leg_index][1] + vector[1]
        self.next_leg_positions[leg_index][2] = height

    def get_COM_distance(self):

        # TODO Include collision of legs as another distance parameter (IMPORTANT BEFORE FINAL IMPLEMENTATION!) not needed before visualization

        min_dist = self.legs[0].COXA_LENGTH + np.sqrt(self.hip_x**2 + self.hip_y**2)
        points = self.get_grounded_leg_positions()

        distances = []

        for point in points:
            dist = np.sqrt(point[0]**2+point[1]**2) - min_dist
            if dist < 0:
                return -1
            distances.append(dist)

        v1 = (points[1][0] - points[0][0], points[1][1] - points[0][1])
        v2 = (points[2][0] - points[0][0], points[2][1] - points[0][1])
        v3 = (points[2][0] - points[1][0], points[2][1] - points[1][1])

        vectors = [v1, v2, v3]

        A = np.array([[v1[0], v2[0]], [v1[1], v2[1]]])
        B = np.array([[-points[0][0]], [-points[0][1]]])

        ab = np.linalg.solve(A, B)

        a = ab[0]
        b = ab[1]

        if (0 <= a <= 1) and (0 <= b <= 1) and (a + b <= 1):
            for i in range(len(points)):
                distances.append(np.linalg.norm(np.cross(vectors[i], points[i]))/np.linalg.norm(vectors[i]))
        else:
            return -1
        
        return min(distances)
    

    def get_grounded_leg_positions(self) -> list:
        positions = []
        for leg in self.grounded_legs:
            positions.append(leg.position)
        return positions   
    def loosen(self):
        for servo in self.control_board.servos:
            servo.angle=None
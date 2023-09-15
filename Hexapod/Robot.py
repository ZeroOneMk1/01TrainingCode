from Leg import Leg
# from ControlBoard import ControlBoard
import numpy as np
from time import sleep
from datetime import datetime as dt
from datetime import timedelta
import math

THETA_WEIGHT = 0.4
POINTS_WEIGHT = 0.4
COM_WEIGHT = 1

class Robot:
    def __init__(self, hip_x, hip_y) -> None:
        self.legs = []
        self.servos = [0, 0, 0, 0, 0, 0]
        self.hip_x = hip_x
        self.hip_y = hip_y

        self.WORKING_HEIGHT = -11.5
        self.STANDARD_DISTANCE = 15

        # RECTANGULAR BODY

        # self.legs.append(Leg(0, np.array([-hip_x, hip_y, 0]), 135)) # Front Left Leg
        # self.legs.append(Leg(1, np.array([-hip_x, 0, 0]), 180)) # Center Left Leg
        # self.legs.append(Leg(2, np.array([-hip_x, -hip_y, 0]), 225)) # Back Left Leg
        # self.legs.append(Leg(3, np.array([hip_x, hip_y, 0]), 45)) # Front Right Leg
        # self.legs.append(Leg(4, np.array([hip_x, 0, 0]), 0)) # Center Right Leg
        # self.legs.append(Leg(5, np.array([hip_x, -hip_y, 0]), 315)) # Back Right Leg

        self.legs.append(Leg(0, np.array([-11.68, 16.68, 0]), 135)) # Front Left Leg
        self.legs.append(Leg(1, np.array([-14.318, 0, 0]), 180)) # Center Left Leg
        self.legs.append(Leg(2, np.array([-11.68, -16.68, 0]), 225)) # Back Left Leg
        self.legs.append(Leg(3, np.array([11.68, 16.68, 0]), 45)) # Front Right Leg
        self.legs.append(Leg(4, np.array([14.318, 0, 0]), 0)) # Center Right Leg
        self.legs.append(Leg(5, np.array([11.68, -16.68, 0]), 315)) # Back Right Leg

        self.current_leg_positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.next_leg_positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

        self.left_tripod = [self.legs[0], self.legs[2], self.legs[4]]
        self.right_tripod = [self.legs[1], self.legs[3], self.legs[5]]

        self.grounded_legs = self.left_tripod
        self.lifted_legs = self.right_tripod

        self.REMOVE = 0

        # self.control_board = ControlBoard(18)
    
    def move_leg_to_position(self, leg_index: int, desired_position) -> None:
        reachable, servo_positions = self.legs[leg_index].calculate_all_servo_positions(desired_position)
        if not reachable:
            print("Not Reachable!")
            return
        for i in range(len(servo_positions)):
            servo_positions[i] = np.clip(servo_positions[i], 0, 180)
        # self.control_board.set_leg_servo_positions(leg_index, servo_positions)
        self.servos[leg_index] = servo_positions
        self.legs[leg_index].position = desired_position
        # print(f"{desired_position}\n{servo_positions}\n\n")
    
    def move_legs_from_current_to_next(self, time:float):
        """Goes from self.current to self.next positions, time is in seconds"""

        """start = dt.now()
        # end = start + timedelta(seconds=time)
        # now = dt.now()

        # # self.move_leg_to_position(leg.index, destination)
        # # sleep(5) # ? remember why this was important. Remove if it works fine while commented.

        # substeps = 0

        # while now < end:

        #     substeps += 1

        #     for leg in self.legs:

        #         line = np.asarray(self.next_leg_positions[leg.index]) - np.asarray(self.current_leg_positions[leg.index])

        #         destination = self.next_leg_positions[leg.index]

        #         t = dt.now() - start
        #         t_sec = t.total_seconds()
        #         destination = np.asarray(np.asarray(self.current_leg_positions[leg.index]) + line * t_sec / time)
        #         self.move_leg_to_position(leg.index, destination)
            
        #     now = dt.now()""" 
        pass
        for leg in self.legs:
            self.move_leg_to_position(leg.index, self.next_leg_positions[leg.index])

        # print(f"Number of substeps: {substeps}")

    def reset_leg_positions(self):
        self.lift_all_legs()
        # sleep(2)
        self.drop_grounded_legs()

    def lift_all_legs(self):
        diag_dist = self.STANDARD_DISTANCE * np.sqrt(2)/2
        self.move_leg_to_position(0, [-self.hip_x - diag_dist,  self.hip_y + diag_dist, 5])
        self.move_leg_to_position(1, [-self.hip_x - self.STANDARD_DISTANCE,          0, 5])
        self.move_leg_to_position(2, [-self.hip_x - diag_dist, -self.hip_y - diag_dist, 5])
        self.move_leg_to_position(3, [ self.hip_x + diag_dist,  self.hip_y + diag_dist, 5])
        self.move_leg_to_position(4, [ self.hip_x + self.STANDARD_DISTANCE,          0, 5])
        self.move_leg_to_position(5, [ self.hip_x + diag_dist, -self.hip_y - diag_dist, 5])

        for leg in self.legs:
            self.current_leg_positions[leg.index] = leg.position

    def drop_grounded_legs(self):
        self.calculate_new_leg_positions((0, 0))
        self.move_legs_from_current_to_next(2)

    def tick(self):
        controller_input = self.get_controller_input()
        self.calculate_new_leg_positions(controller_input)
        self.move_legs_from_current_to_next(0.02)
        for i in range(len(self.current_leg_positions)):
            for j in range(len(self.current_leg_positions[i])):
                self.current_leg_positions[i][j] = self.next_leg_positions[i][j] # ! May have errors when next gets changed
        # sleep(1/50)
    
    def get_controller_input(self):
        # c, s = np.cos(self.REMOVE), np.sin(self.REMOVE)
        # self.REMOVE += np.pi/64
        return (0, 1) # TODO actually set up the controller instead of just giving X=0 Y=0.5

    

    def calculate_new_leg_positions(self, input: tuple) -> None:
        if self.shift_lifted_leg_positions(input):
            self.shift_grounded_leg_positions(input)
        else:
            self.swap_legs()
            
    def swap_legs(self):
        self.grounded_legs, self.lifted_legs = self.lifted_legs, self.grounded_legs # ! Does this work with lists of objects in python? Or does this cause a pointer error?

    def shift_lifted_leg_positions(self, input: tuple) -> bool:
        d = self.get_COM_distance(input)

        if d == -1:
            return False
        
        for leg in self.lifted_legs:
            self.shift_leg_position(leg.index, input, d + self.WORKING_HEIGHT) # TODO Tune d via different functions
        
        return True
    
    def shift_grounded_leg_positions(self, input: tuple) -> None:  
        reversed_input = (-input[0], -input[1])      
        for leg in self.grounded_legs:
            self.shift_leg_position(leg.index, reversed_input, self.WORKING_HEIGHT)

    def shift_leg_position(self, leg_index: int,  vector: tuple, height: float) -> None:
        self.next_leg_positions[leg_index][0] = self.current_leg_positions[leg_index][0] + vector[0]
        self.next_leg_positions[leg_index][1] = self.current_leg_positions[leg_index][1] + vector[1]
        self.next_leg_positions[leg_index][2] = height

    def get_COM_distance(self, vector):

        # TODO Include collision of legs as another distance parameter (IMPORTANT BEFORE FINAL IMPLEMENTATION!) not needed before visualization
        
        glegpos = self.get_grounded_leg_positions()
        points = []

        for i in range(len(glegpos)):
            points.append([])
            for j in range(len(glegpos[i])):
                points[i].append(glegpos[i][j])

        for i in range(len(points)):
            points[i][0] = points[i][0] - vector[0] # ! MAY BE POSITIVE
            points[i][1] = points[i][1] - vector[1]

        distances = []

        for i in range(len(points)):
            min_dist = self.grounded_legs[i].COXA_LENGTH + np.sqrt(self.grounded_legs[i].hipPos[0]**2 + self.grounded_legs[i].hipPos[1]**2)
            dist = np.sqrt(points[i][0]**2+points[i][1]**2) - min_dist
            if dist < 0:
                return -1
            distances.append(POINTS_WEIGHT * dist)

            rel_destination = self.grounded_legs[i].absolute_to_relative_destination(points[i])

            perp_destination, theta = self.grounded_legs[i].relative_to_perpendicular_destination(rel_destination)

            theta_dist = 45-abs(theta * 180 / np.pi)

            if theta_dist < 0:
                return -1

            distances.append(THETA_WEIGHT * theta_dist)

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
                distances.append(COM_WEIGHT * np.linalg.norm(np.cross(vectors[i], points[i]))/np.linalg.norm(vectors[i]))
        else:
            return -1
        
        # print(min(distances))

        return min(distances)
    

    def get_grounded_leg_positions(self) -> list:
        positions = []
        for leg in self.grounded_legs:
            positions.append(leg.position)
        return positions   
    
    def loosen(self):

        # for servo in self.control_board.servos:
        #     servo.angle=None
        pass


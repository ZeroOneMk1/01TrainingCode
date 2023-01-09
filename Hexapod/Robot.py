from Leg import Leg
# from ControlBoard import ControlBoard
import numpy as np
from time import sleep
from datetime import datetime as dt

class Robot:
    def __init__(self, hip_x, hip_y) -> None:
        self.legs = []
        self.hip_x = hip_x
        self.hip_y = hip_y

        self.legs.append(Leg(np.array([-hip_x, hip_y, 0]), 135)) # Front Left Leg
        self.legs.append(Leg(np.array([-hip_x, 0, 0]), 180)) # Center Left Leg
        self.legs.append(Leg(np.array([-hip_x, -hip_y, 0]), 225)) # Back Left Leg
        self.legs.append(Leg(np.array([hip_x, hip_y, 0]), 45)) # Front Right Leg
        self.legs.append(Leg(np.array([hip_x, 0, 0]), 0)) # Center Right Leg
        self.legs.append(Leg(np.array([hip_x, -hip_y, 0]), 315)) # Back Right Leg

        self.leg_positions = ()

        self.left_tripod = [self.legs[0], self.legs[2], self.legs[4]]
        self.right_tripod = [self.legs[1], self.legs[3], self.legs[5]]

        # self.control_board = ControlBoard(3)
    
    def move_leg_to_position(self, leg_index: int, desired_position) -> None:
        reachable, servo_positions = self.legs[leg_index].calculate_servo_positions(desired_position)
        if not reachable:
            print("Not Reachable!")
            return
        # self.control_board.set_leg_servo_positions(leg_index, servo_positions)
    
    def move_leg_from_point_to_point(self, a, b, time:float):
        """a and b must be numpy arrays, time is in seconds"""

        start = dt.now()
        end = start + dt.timedelta(seconds=time)
        now = dt.now()

        line = b - a

        destination = a
        self.move_leg_to_position(destination)
        # sleep(5) # TODO remember why this was important.

        substeps = 0

        while now < end:
            substeps += 1
            t = dt.now() - start
            t_sec = t.total_seconds()
            destination = np.array(a + line * t_sec / time)
            self.move_leg_to_position(destination)
        
        destination = b
        self.move_leg_to_position(destination)

        print(f"Number of substeps: {substeps}")

    def reset_leg_positions(self):
        self.reset_lifted_tripod()
        self.swap_tripods()
        self.reset_lifted_tripod()

    def tick(self):
        controller_input = self.get_controller_input()
        new_leg_positions = self.calculate_new_leg_positions(controller_input)
        self.move_legs_to_positions(new_leg_positions)
        sleep(1/50)
    
    def get_controller_input(self):
        return (0, 1) # TODO actually set up the controller instead of just giving X=0 Y=1

    def calculate_new_leg_positions(self, input: tuple) -> list:
        if self.shift_lifted_leg_positions(input):
            self.shift_grounded_leg_positions(input)
        else:
            self.swap_legs()
    
    def shift_lifted_leg_positions(self, input: tuple) -> bool:
        d = self.get_COM_distance()

        if d == -1:
            return False
        
        for leg in self.lifted_legs:
            leg.shift_position(input) # this function should be the one doing the math cause it saves nesting
        
        return True
    
    def shift_grounded_leg_positions(self, input: tuple) -> None:
        d = self.get_COM_distance()
        
        for leg in self.grounded_legs:
            leg.shift_position(input)


    def get_COM_distance(self):
        min_dist = self.legs[0].COXA_LENGTH + np.sqrt(self.hip_x**2 + self.hip_y**2)
        points = self.grounded_leg_positions()

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
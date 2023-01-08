from Leg import Leg
# from ControlBoard import ControlBoard
import numpy as np
from time import sleep
from datetime import datetime as dt

class Robot:
    def __init__(self) -> None:
        self.legs = []

        self.legs.append(Leg(np.array([-50, 50, 0]), 135)) # Front Left Leg
        self.legs.append(Leg(np.array([-50, 0, 0]), 180)) # Center Left Leg
        self.legs.append(Leg(np.array([-50, -50, 0]), 225)) # Back Left Leg
        self.legs.append(Leg(np.array([50, 50, 0]), 45)) # Front Right Leg
        self.legs.append(Leg(np.array([50, 0, 0]), 0)) # Center Right Leg
        self.legs.append(Leg(np.array([50, -50, 0]), 315)) # Back Right Leg

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
        sleep(5) # TODO add some sort of better wait time.

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

    def tick(self):
        controller_input = self.get_controller_input()
        new_leg_positions = self.calculate_new_leg_positions(controller_input)
        self.move_legs_to_positions(new_leg_positions)
        sleep(1/50)
    
    def get_controller_input(self):
        return (0, 1) # TODO actually set up the controller instead of just giving X=0 Y=1
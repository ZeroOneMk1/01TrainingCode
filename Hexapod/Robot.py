from Leg import Leg
from ControlBoard import ControlBoard
import numpy as np
from time import sleep
from datetime import datetime as dt

class Robot:
    def __init__(self) -> None:
        self.legs = []

        self.legs.append(Leg(np.array([0, 0, 0]), 0, 0)) # TODO expand to 6 legs

        self.control_board = ControlBoard(3)
    
    def move_leg_to_position(self, leg_index: int, desired_position) -> None:
        reachable, servo_positions = self.legs[leg_index].calculate_servo_positions(desired_position)
        if reachable:
            self.control_board.set_leg_servo_positions(leg_index, servo_positions)
        else:
            print("Not Reachable!")
    
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

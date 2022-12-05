from Leg import Leg
from ControlBoard import ControlBoard
import numpy as np

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
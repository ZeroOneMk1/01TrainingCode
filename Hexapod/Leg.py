import numpy as np

class Leg:
    def __init__(self, hipPos, zeroOrientation: float, tibia_length: float = 100.0, femur_length: float = 50.0, coxa_length: float = 20.0) -> None:
        self.hipPos = np.array(hipPos)

        self.TIBIA_LENGTH = tibia_length
        self.FEMUR_LENGTH = femur_length
        self.COXA_LENGTH = coxa_length
        self.BCSQ = self.FEMUR_LENGTH * self.FEMUR_LENGTH + self.TIBIA_LENGTH * self.TIBIA_LENGTH
        self.D2BC = 1/(self.FEMUR_LENGTH * self.TIBIA_LENGTH)* 0.5
        self.BCSQD2BC = self.BCSQ * self.D2BC

        theta = np.radians(-zeroOrientation)
        c, s = np.cos(theta), np.sin(theta)
        R = np.matrix([[c, -s, 0], [s, c,0], [0,0,1]])

        self.ROT_Z_MATRIX = R

    def absolute_to_relative_destination(self, abs_destination) -> np.array:
        temp_destination = abs_destination - self.hipPos
        rel_destination = self.ROT_Z_MATRIX*temp_destination.reshape(3,1)
        return rel_destination

    def relative_to_perpendicular_destination(self, rel_destination) -> np.array and float:
        try:
            theta  = -np.arctan(rel_destination[1]/rel_destination[0])
        except:
            theta  = rel_destination[1]/abs(rel_destination[1]) * np.pi / 2

        c, s = np.cos(theta), np.sin(theta)
        R = np.matrix([[c, -s, 0], [s, c,0], [0,0,1]])

        perp_destination = R*rel_destination.reshape(3,1) - np.array(self.COXA_LENGTH, 0, 0)
        return perp_destination, -theta


    def is_within_envelope(self, perp_destination) -> bool:
        """Assumes that the destination is WITHIN WORKABLE XY-ANGLE"""

        Y = perp_destination[2]
        X = perp_destination[0]
        
        if np.sqrt((self.TIBIA_LENGTH + self.FEMUR_LENGTH)**2 - Y**2) >= X >= np.sqrt(self.TIBIA_LENGTH**2 - (Y-self.FEMUR_LENGTH)**2):
            return True

        if 0 <= X <= np.sqrt((self.TIBIA_LENGTH + self.FEMUR_LENGTH)**2 - Y**2) and Y < self.FEMUR_LENGTH - self.TIBIA_LENGTH:
            return True

        if -np.sqrt((self.FEMUR_LENGTH - self.TIBIA_LENGTH)**2 - Y**2) >= X >= -np.sqrt(self.TIBIA_LENGTH**2 - (Y - self.FEMUR_LENGTH)**2):
            return True

        if 0 >= X >= -np.sqrt(self.TIBIA_LENGTH**2 - (Y + self.FEMUR_LENGTH)**2) and Y < self.FEMUR_LENGTH - self.TIBIA_LENGTH:
            return True

        return False
    
    def calculate_second_third_servo_positions(self, perp_destination) -> float:
        """Assumes it's in envelope"""
        L = np.linalg.norm(perp_destination)
        angle_three = np.arccos(self.BCSQD2BC - L**2 * self.D2BC)

        try:
            vector_angle = -np.arctan(perp_destination[2]/perp_destination[0])
        except:
            vector_angle = np.pi/2

        ambiguous = 0

        if L < 5*np.sqrt(3):
            ambiguous = 1
        
        alpha = ambiguous * np.arcsin(self.TIBIA_LENGTH/L*np.sin(angle_three)) + (1-ambiguous)(np.pi-np.arcsin(self.TIBIA_LENGTH/L*np.sin(angle_three)))

        angle_two = np.pi/2 + vector_angle - alpha

        return angle_two, angle_three


        
    def calculate_all_servo_positions(self, abs_destination):
        rel_destination = self.absolute_to_relative_destination(abs_destination)

        perp_destination, theta = self.relative_to_perpendicular_destination(rel_destination)

        if theta > np.pi / 2 or theta < -np.pi/2:
            return False, np.zeros(1, 3)
        
        if self.is_within_envelope(perp_destination):

            servo_two_angle, servo_three_angle = self.calculate_second_third_servo_positions(perp_destination)
            angles = np.array([theta, servo_two_angle, servo_three_angle]) * 180 / np.pi
            return True, angles
        else:
            return False, np.zeros(1, 3)


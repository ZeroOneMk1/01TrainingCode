import numpy as np
import math

DEG = 180 / math.pi
RAD = math.pi / 180

class Leg:
    def __init__(self, index:int, hipPos, zeroOrientation: float, tibia_length: float = 15.0, femur_length: float = 7.5, coxa_length: float = 5) -> None:
        self.hipPos = np.array(hipPos)
        self.index = index

        self.TIBIA_LENGTH = tibia_length
        self.FEMUR_LENGTH = femur_length
        self.COXA_LENGTH = coxa_length
        self.BCSQ = self.FEMUR_LENGTH * self.FEMUR_LENGTH + self.TIBIA_LENGTH * self.TIBIA_LENGTH
        self.D2BC = 1/(self.FEMUR_LENGTH * self.TIBIA_LENGTH)* 0.5
        self.BCSQD2BC = self.BCSQ * self.D2BC

        self.MAX_THETA: float = math.pi / 3

        self.position = (0, 0, 0)

        self.rest_angle = np.radians(-zeroOrientation)

        theta = np.radians(-zeroOrientation)
        c, s = np.cos(theta), np.sin(theta)
        R = np.matrix([[c, -s, 0], [s, c,0], [0,0,1]])

        self.ROT_Z_MATRIX = R
        self.ROT_Z_C = c
        self.ROT_Z_S = s

        self.min_dist = self.COXA_LENGTH + (self.hipPos[0]**2 + self.hipPos[1]**2)**.5

    def absolute_to_relative_destination(self, abs_destination) -> np.array:
        temp_destination = abs_destination - self.hipPos

        rel_destination = [self.ROT_Z_C*temp_destination[0] - self.ROT_Z_S*temp_destination[1], self.ROT_Z_S*temp_destination[0] + self.ROT_Z_C*temp_destination[1], temp_destination[2]]

        # rel_destination = self.ROT_Z_MATRIX*temp_destination.reshape(3,1)
        # rel_dest_return = [float(rel_destination[0][0]), float(rel_destination[1][0]), float(rel_destination[2][0])]
        # print(f"TEMP:\n{temp_destination}\nREL:\n{rel_dest_return}\n\n")
        return rel_destination

    def relative_to_perpendicular_destination(self, rel_destination) -> np.array and float:
        
        if rel_destination[0] == 0:
            if rel_destination[1] == 0:
                theta = 0
            else:
                theta  = rel_destination[1]/abs(rel_destination[1]) * math.pi / 2
        else:
            theta  = -math.atan(rel_destination[1]/rel_destination[0])

        perp_destination = [(rel_destination[0]**2 + rel_destination[1]**2)**.5 - self.COXA_LENGTH, 0, rel_destination[2]]
        return perp_destination, -theta


    def is_within_envelope(self, perp_destination) -> bool:
        """Assumes that the destination is WITHIN WORKABLE XY-ANGLE"""

        Y = float(perp_destination[2])
        X = float(perp_destination[0])
        
        try:
            A = ((self.TIBIA_LENGTH + self.FEMUR_LENGTH)**2 - Y**2)**.5
            B = (self.TIBIA_LENGTH**2 - (Y-self.FEMUR_LENGTH)**2)**.5
            C = self.FEMUR_LENGTH - self.TIBIA_LENGTH
            D = -((C)**2 - Y**2)**.5
            E = -(self.TIBIA_LENGTH**2 - (Y - self.FEMUR_LENGTH)**2)**.5
            F = -(self.TIBIA_LENGTH**2 - (Y + self.FEMUR_LENGTH)**2)**.5
        except Exception as e:
            print(f"EXCEPTION: {e}")
            return False, None
        
        if isinstance(A, complex) or isinstance(B, complex) or isinstance(C, complex) or isinstance(D, complex) or isinstance(E, complex) or isinstance(F, complex):
            print(f"COMPLEX NUMBERS, VARIABLE DUMP:\n{A}\n{B}\n{C}\n{D}\n{E}\n{F}\n")
            return False, None

        if A >= X >= B:
            return True, perp_destination

        if 0 <= X <= A and Y <= C:
            return True, perp_destination

        if D >= X >= E:
            return True, perp_destination

        if 0 >= X >= F and Y <= C:
            return True, perp_destination

        if 0 < B and Y >= C:
            # Snaps input to within the envelope while maintaining desired height
            return True, [B, perp_destination[1], perp_destination[2]]

        return False, None
    
    def calculate_second_third_servo_positions(self, snapped_destination) -> float:
        """Assumes it's in envelope"""
        L = (snapped_destination[0]**2 + snapped_destination[2]**2)**.5
        angle_three = math.acos(self.BCSQD2BC - L**2 * self.D2BC)

        Y = float(snapped_destination[2])
        X = float(snapped_destination[0])

        try:
            vector_angle = -math.atan(Y/X)
        except:
            vector_angle = math.pi/2

        ambiguous = 1

        if L < self.TIBIA_LENGTH*math.cos(math.asin(self.FEMUR_LENGTH/self.TIBIA_LENGTH)):
            ambiguous = 0
        
        alpha = ambiguous * math.asin(self.TIBIA_LENGTH/L*math.sin(angle_three)) + (1-ambiguous)*(math.pi-math.asin(self.TIBIA_LENGTH/L*math.sin(angle_three)))

        angle_two = math.pi/2 + vector_angle - alpha

        return angle_two, angle_three

        
    def calculate_all_servo_positions(self, abs_destination):
        rel_destination = self.absolute_to_relative_destination(abs_destination)
        perp_destination, theta = self.relative_to_perpendicular_destination(rel_destination)
        if theta > self.MAX_THETA or theta < -self.MAX_THETA:
            return False, None
        in_envelope, snapped_destination = self.is_within_envelope(perp_destination)
        # if self.index == 4:
            # print(f"LEG {self.index}\n")
            # print(f"ABS_DES:{abs_destination}\n")
            # print(f"REL_DES:{rel_destination}\n")
            # # print(f"PERP_DES:{perp_destination}\n")
            # print(f"SNAP_DES:{snapped_destination}\n")
        
        if in_envelope:

            servo_two_angle, servo_three_angle = self.calculate_second_third_servo_positions(snapped_destination)
            angles = [theta * DEG + 90, 180 - servo_two_angle * DEG, servo_three_angle * DEG]
            # print(f"ANGLES:{angles}\n\n")
            return True, angles
        else:
            return False, None


import numpy as np

class Leg:
    def __init__(self, index:int, hipPos, zeroOrientation: float, tibia_length: float = 25.0, femur_length: float = 13.5, coxa_length: float = 2.5) -> None:
        self.hipPos = np.array(hipPos)
        self.index = index

        self.TIBIA_LENGTH = tibia_length
        self.FEMUR_LENGTH = femur_length
        self.COXA_LENGTH = coxa_length
        self.BCSQ = self.FEMUR_LENGTH * self.FEMUR_LENGTH + self.TIBIA_LENGTH * self.TIBIA_LENGTH
        self.D2BC = 1/(self.FEMUR_LENGTH * self.TIBIA_LENGTH)* 0.5
        self.BCSQD2BC = self.BCSQ * self.D2BC

        self.MAX_THETA: float = np.pi / 3

        self.position = (0, 0, 0)

        theta = np.radians(-zeroOrientation)
        c, s = np.cos(theta), np.sin(theta)
        R = np.matrix([[c, -s, 0], [s, c,0], [0,0,1]])

        self.ROT_Z_MATRIX = R

    def absolute_to_relative_destination(self, abs_destination) -> np.array:
        temp_destination = abs_destination - self.hipPos
        rel_destination = self.ROT_Z_MATRIX*temp_destination.reshape(3,1)
        rel_dest_return = [float(rel_destination[0][0]), float(rel_destination[1][0]), float(rel_destination[2][0])]
        return rel_dest_return

    def relative_to_perpendicular_destination(self, rel_destination) -> np.array and float:
        
        if rel_destination[0] == 0:
            if rel_destination[1] == 0:
                theta = 0
            else:
                theta  = rel_destination[1]/abs(rel_destination[1]) * np.pi / 2
        else:
            theta  = -np.arctan(rel_destination[1]/rel_destination[0])

        perp_destination = [np.sqrt(rel_destination[0]**2 + rel_destination[1]**2) - self.COXA_LENGTH, 0, rel_destination[2]]
        return perp_destination, -theta


    def is_within_envelope(self, perp_destination) -> bool:
        """Assumes that the destination is WITHIN WORKABLE XY-ANGLE"""

        Y = float(perp_destination[2])
        X = float(perp_destination[0]) # TODO FIGURE OUT WHY MATRICES STACK
        
        try:

            if np.sqrt((self.TIBIA_LENGTH + self.FEMUR_LENGTH)**2 - Y**2) >= X >= np.sqrt(self.TIBIA_LENGTH**2 - (Y-self.FEMUR_LENGTH)**2):
                return True, perp_destination

            if 0 <= X <= np.sqrt((self.TIBIA_LENGTH + self.FEMUR_LENGTH)**2 - Y**2) and Y <= self.FEMUR_LENGTH - self.TIBIA_LENGTH:
                return True, perp_destination

            if -np.sqrt((self.FEMUR_LENGTH - self.TIBIA_LENGTH)**2 - Y**2) >= X >= -np.sqrt(self.TIBIA_LENGTH**2 - (Y - self.FEMUR_LENGTH)**2):
                return True, perp_destination

            if 0 >= X >= -np.sqrt(self.TIBIA_LENGTH**2 - (Y + self.FEMUR_LENGTH)**2) and Y <= self.FEMUR_LENGTH - self.TIBIA_LENGTH:
                return True, perp_destination

            if 0 < np.sqrt(self.TIBIA_LENGTH**2 - (Y-self.FEMUR_LENGTH)**2) and Y >= self.FEMUR_LENGTH - self.TIBIA_LENGTH:
                # Snaps input to within the envelope while maintaining desired height
                return True, [np.sqrt(self.TIBIA_LENGTH**2-(Y-self.FEMUR_LENGTH)**2), perp_destination[1], perp_destination[2]]
        except Exception as e:
            print(f"EXCEPTION: {e}")
            return False, None
        return False, None
    
    def calculate_second_third_servo_positions(self, perp_destination) -> float:
        """Assumes it's in envelope"""
        L = np.sqrt(perp_destination[0]**2 + perp_destination[2]**2)
        angle_three = np.arccos(self.BCSQD2BC - L**2 * self.D2BC)

        Y = float(perp_destination[2])
        X = float(perp_destination[0]) # TODO FIGURE OUT WHY MATRICES STACK

        try:
            vector_angle = -np.arctan(Y/X)
        except:
            vector_angle = np.pi/2

        ambiguous = 1

        if L < self.TIBIA_LENGTH*np.cos(np.arcsin(self.FEMUR_LENGTH/self.TIBIA_LENGTH)):
            ambiguous = 0
        
        alpha = ambiguous * np.arcsin(self.TIBIA_LENGTH/L*np.sin(angle_three)) + (1-ambiguous)*(np.pi-np.arcsin(self.TIBIA_LENGTH/L*np.sin(angle_three)))

        angle_two = np.pi/2 + vector_angle - alpha

        return angle_two, angle_three


        
    def calculate_all_servo_positions(self, abs_destination):
        rel_destination = self.absolute_to_relative_destination(abs_destination)
        perp_destination, theta = self.relative_to_perpendicular_destination(rel_destination)
        if theta > self.MAX_THETA or theta < -self.MAX_THETA:
            return False, None
        in_envelope, snapped_destination = self.is_within_envelope(perp_destination)
        if self.index == 4:
            print(f"LEG {self.index}\n")
            print(f"ABS_DES:{abs_destination}\n")
            # print(f"REL_DES:{rel_destination}\n")
            # # print(f"PERP_DES:{perp_destination}\n")
            # print(f"SNAP_DES:{snapped_destination}\n")
        
        if in_envelope:

            servo_two_angle, servo_three_angle = self.calculate_second_third_servo_positions(snapped_destination)
            angles = np.array([theta + np.pi/2, np.pi-servo_two_angle, servo_three_angle]) * 180 / np.pi
            # print(f"ANGLES:{angles}\n\n")
            return True, angles
        else:
            return False, None


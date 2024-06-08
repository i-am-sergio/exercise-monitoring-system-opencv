import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class EstocadaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/estocada.mp4')
        self.rep_count = 0
        self.initiated = False
    
    def __del__(self):
        super().__del__()

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle
    
    def check_exercise(self, keypoints):
        left_shoulder = keypoints[5][:2]
        right_shoulder = keypoints[6][:2]
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]
        left_ankle = keypoints[15][:2]
        right_ankle = keypoints[16][:2]
        
        # Calculate angles
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
        left_hip_angle = self.calculate_angle(left_knee, left_hip, left_shoulder)
        right_hip_angle = self.calculate_angle(right_knee, right_hip, right_shoulder)
        
        # Tolerancia para la alineación vertical en vista diagonal
        vertical_tolerance = 50  # Ajuste este valor según sea necesario para la diagonalidad

        # Check if the body is upright considering a diagonal view
        upright_check = lambda p1, p2: abs(p1[1] - p2[1]) > abs(p1[0] - p2[0]) - vertical_tolerance

        if not (upright_check(left_shoulder, left_hip) and upright_check(right_shoulder, right_hip)):
            return False  # Not sufficiently upright

        # Determine if a lunge is starting or in progress
        if not self.initiated:
            # Check if the lunge is starting with either leg
            if (130 <= left_knee_angle <= 180 and 120 <= left_hip_angle <= 180) or \
            (130 <= right_knee_angle <= 180 and 120 <= right_hip_angle <= 180):
                self.initiated = True
                return True  # Lunge started or in progress
        else:
            # Check if the lunge is still in progress with either leg
            if (60 <= left_knee_angle <= 120) or (60 <= right_knee_angle <= 120):
                return True  # Lunge in progress
            
            # Check if the lunge is complete with either leg
            if (75 <= left_knee_angle <= 115) or (75 <= right_knee_angle <= 115):
                self.initiated = False
                self.rep_count += 1
                return True  # Lunge complete
        
        return False
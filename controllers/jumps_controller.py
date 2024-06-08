import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class JumpsController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/jumping_jack.mp4')
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

    # las piernas deben abrirse y cerrarse    
    def check_exercise(self, keypoints):
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]
        left_ankle = keypoints[15][:2]
        right_ankle = keypoints[16][:2]

        # Calculate angles
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)

        # Correcto: Ha logrado el ángulo esperado
        if (75 <= left_knee_angle <= 115) and (75 <= right_knee_angle <= 115):
            return 3
        

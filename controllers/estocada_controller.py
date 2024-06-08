import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class EstocadaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/flexion.mp4')
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

        vertical_tolerance = 50
        upright_check = lambda p1, p2: abs(p1[1] - p2[1]) > abs(p1[0] - p2[0]) - vertical_tolerance

        # Correcto: Ha logrado el ángulo esperado
        if (75 <= left_knee_angle <= 115) or (75 <= right_knee_angle <= 115):
            return 3  # Correcto

        # Incorrecto: No ha logrado el ángulo esperado
        if (60 <= left_knee_angle <= 120) or (60 <= right_knee_angle <= 120):
            return 2  # Incorrecto

        # Intento: Está en proceso de agacharse y doblar las piernas
        if self.initiated and ((60 <= left_knee_angle <= 120) or (60 <= right_knee_angle <= 120)):
            return 1  # Intento

        # Reposo: No está suficientemente erguido o está con las piernas rectas
        if not (upright_check(left_shoulder, left_hip) and upright_check(right_shoulder, right_hip)) or \
        (130 <= left_knee_angle <= 180 and 120 <= left_hip_angle <= 180) or \
        (130 <= right_knee_angle <= 180 and 120 <= right_hip_angle <= 180):
            return 0  # Reposo

        return 2  # Por defecto, se considera Incorrecto

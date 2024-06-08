import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class ElevacionesController(ShowWindow):
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
        return False
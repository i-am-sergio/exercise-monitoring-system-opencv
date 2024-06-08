
import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np

class AbdominalController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/cortado1.mp4')
        self.rep_count = 0
        self.is_crunch_correct = False
        self.angle_init=180
        self.angle_end=40
        self.angle_attempt=100
    
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
        # Left hip (11), left shoulder (5), and left knee (13)
        hip = keypoints[11][:2]
        shoulder = keypoints[5][:2]
        knee = keypoints[13][:2]
        
        crunch_angle = self.calculate_angle(knee, hip, shoulder)
        return crunch_angle < 30  # Reduced threshold angle for crunch detection

    def check_attempt(self, keypoints):
        # Left hip (11), left shoulder (5), and left knee (13)
        hip = keypoints[11][:2]
        shoulder = keypoints[5][:2]
        knee = keypoints[13][:2]

        crunch_angle = self.calculate_angle(knee, hip, shoulder)
        return crunch_angle < self.angle_attempt

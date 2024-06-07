
import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np

class AbdominalController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/thunder.tflite', 'detection/video_completo.mp4')
        self.rep_count = 0
        self.is_crunch_correct = False  # Boolean to track the state of crunch correctness
    
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
        
        return crunch_angle < 60  # Reduced threshold angle for crunch detection


import cv2
import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',   
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

class EstocadaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/thunder.tflite', 'detection/video_completo.mp4')
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
        left_hip = keypoints[11][:2]
        left_knee = keypoints[13][:2]
        left_ankle = keypoints[15][:2]
        
        # Use left shoulder (index 5) for hip angle calculation
        left_shoulder = keypoints[5][:2]
        
        # Calculate angles
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        left_hip_angle = self.calculate_angle(left_knee, left_hip, left_shoulder)
        
        if not self.initiated:
            # Check if the lunge is starting
            if 150 <= left_knee_angle <= 180 and 140 <= left_hip_angle <= 180:
                self.initiated = True
                return False  # Lunge started, so return False
        else:
            # Check if the lunge is complete
            if 70 <= left_knee_angle <= 110:
                self.initiated = False
                self.rep_count += 1
                return True  # Lunge complete, so return True
        
        return False  # Not a lunge, so return False
import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class SentadillaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/sentadilla.mp4')
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
    
    # Check if the person is squatting
    # Check if angle between hips, knees and ankles is correct
    def check_exercise(self, keypoints):
        # Extract relevant keypoints
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]
        left_ankle = keypoints[15][:2]
        right_ankle = keypoints[16][:2]
        
        # Calculate angles
        angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
        angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)
        
        # # Check if angles are within the correct range
        # if angle_left < correct_threshold and angle_right < correct_threshold:
        #     return 3  # Correct
        # else:
        #     return 2  # Incorrect
        # I want check in range of 80 to 100,
        if self.range_of_angle(angle_left) and self.range_of_angle(angle_right):
            return 3 # Correct
        else:
            return 2 # Incorrect
    
    def range_of_angle(self, angle): # return true if angle is in range of 80 to 100 or false if not
        if angle >= 70 and angle <= 110: # arround of 90
            return True
        else:
            return False

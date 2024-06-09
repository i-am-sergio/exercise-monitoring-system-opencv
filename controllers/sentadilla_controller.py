import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class SentadillaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/sentadilla.mp4')
        self.rep_count = 0
        self.initiated = False
        self.angle_knee_attempt = 130
    
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

    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))
    
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
        left_shoulder = keypoints[5][:2]
        right_shoulder = keypoints[6][:2]

        # Calculate distances
        distance_left = self.calculate_distance(left_shoulder, left_knee)
        distance_right = self.calculate_distance(right_shoulder, right_knee)
        
        # Calculate angles
        angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
        angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)
        
        # if distances < 0.3 is attempting
        if distance_left < 0.3 and distance_right < 0.3:
            return angle_left < 95 and angle_right < 95
        else:
            return False
    
    # Check if the person is attempting to squat
    # Check if the angle between hips, knees and ankles is correct
    def check_attempt(self, keypoints):
        # Extract relevant keypoints
        left_hip = keypoints[11][:2]
        right_hip = keypoints[12][:2]
        left_knee = keypoints[13][:2]
        right_knee = keypoints[14][:2]
        left_ankle = keypoints[15][:2]
        right_ankle = keypoints[16][:2]
        left_shoulder = keypoints[5][:2]
        right_shoulder = keypoints[6][:2]
        
        # Calculate angles
        angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
        angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)

        # distance between shoulders and knees
        distance_left = self.calculate_distance(left_shoulder, left_knee)
        distance_right = self.calculate_distance(right_shoulder, right_knee)

        # if distances < 0.3 is attempting
        if distance_left < 0.3 and distance_right < 0.3:
            return angle_left < self.angle_knee_attempt and angle_right < self.angle_knee_attempt
        else:
            return False

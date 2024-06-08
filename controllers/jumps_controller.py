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

    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))

    # 'left_ankle': 15, 'right_ankle': 16, 'left_wrist': 9, 'right_wrist': 10
    def check_exercise(self, keypoints):
        # Define threshold distances for the exercise
        ankle_distance_threshold = 0.1  
        wrist_vertical_threshold = 0.1

        # Get the coordinates of the ankles
        left_ankle = keypoints[15][:2]
        right_ankle = keypoints[16][:2]

        # Get the coordinates of the wrists
        left_wrist = keypoints[9][:2]
        right_wrist = keypoints[10][:2]

        # Calculate the distance between the ankles
        ankle_distance = self.calculate_distance(left_ankle, right_ankle)

        # Calculate the vertical movement of the wrists
        left_wrist_vertical_movement = abs(left_wrist[0] - 0)
        right_wrist_vertical_movement = abs(right_wrist[0] - 0)

        # Check the state of the exercise
        # If the distance between the ankles is greater than the threshold and the vertical movement of the wrists is greater than the threshold, the state is 3
        if (ankle_distance > ankle_distance_threshold) and (left_wrist_vertical_movement < wrist_vertical_threshold or right_wrist_vertical_movement < wrist_vertical_threshold):
            state = 3
        else:
            state = 2

        return state


import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class JumpsController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/jumping_jack.mp4')
        self.rep_count = 0
        self.initiated = False
        self.ankle_distance_attempt = 0.1
        self.wrist_vertical_attempt = 0.1
    
    def __del__(self):
        super().__del__()

    def calculate_distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))

    # check the state of the exercise
    def check_exercise(self, keypoints):
        # Define threshold distances for the exercise
        ankle_distance_threshold = 0.05
        wrist_vertical_threshold = 0.05
        ankle_distance_tolerance = 0.07
        wrist_vertical_tolerance = 0.07

        # Get the coordinates of the ankles and wrists
        left_ankle, right_ankle = keypoints[15][:2], keypoints[16][:2]
        left_wrist, right_wrist = keypoints[9][:2], keypoints[10][:2]

        # Calculate the distance between the ankles and the vertical movement of the wrists
        ankle_distance = self.calculate_distance(left_ankle, right_ankle)
        left_wrist_vertical_movement = abs(left_wrist[0] - 0)
        right_wrist_vertical_movement = abs(right_wrist[0] - 0)

        # Check the state of the exercise with original and tolerant thresholds
        is_correct = self.is_exercise_correct(ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_distance_threshold, wrist_vertical_threshold)
        is_correct_tolerant = self.is_exercise_correct(ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_distance_tolerance, wrist_vertical_tolerance)

        # Calculate scores based on original and tolerant thresholds
        score = self.calculate_score(ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_distance_threshold, wrist_vertical_threshold)
        score_tolerant = self.calculate_score(ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_distance_tolerance, wrist_vertical_tolerance)

        # Calculate the final score percent
        score_percent = max(score, score_tolerant) if max(score, score_tolerant) >= 0 else 0
        color = self.determine_color(score_percent)

        # Create the indications with descriptive messages
        indications = [
            {"name": "Precisión: " + str(round(score_percent, 2)) + "%", "color": color},
            {"name": "Piernas estiradas" if is_correct or is_correct_tolerant else "Corrige piernas", "color": "green" if is_correct or is_correct_tolerant else "red"},
            {"name": "Brazos estirados" if left_wrist_vertical_movement < wrist_vertical_threshold or right_wrist_vertical_movement < wrist_vertical_threshold else "Corrige brazos", "color": "green" if left_wrist_vertical_movement < wrist_vertical_threshold or right_wrist_vertical_movement < wrist_vertical_threshold else "red"}
        ]

        self.show_indications(indications)
        return is_correct

    def is_exercise_correct(self, ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_threshold, wrist_threshold):
        return (ankle_distance > ankle_threshold) and (left_wrist_vertical_movement < wrist_threshold or right_wrist_vertical_movement < wrist_threshold)

    def calculate_score(self, ankle_distance, left_wrist_vertical_movement, right_wrist_vertical_movement, ankle_threshold, wrist_threshold):
        score_ankle_distance = min((ankle_distance / ankle_threshold) * 100, 100)
        score_wrist_vertical_movement = min((wrist_threshold - min(left_wrist_vertical_movement, right_wrist_vertical_movement)) / wrist_threshold * 100, 100)
        return np.mean([score_ankle_distance, score_wrist_vertical_movement])

    def determine_color(self, score_percent):
        if score_percent > 80:
            return "blue"
        elif 1 <= score_percent <= 80:
            return "green"
        else:
            return "red"

    # check the state of the attempt
    def check_attempt(self, keypoints):
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

        # Check the state of the attempt
        # If the distance between the ankles is greater than the threshold and the vertical movement of the wrists is greater than the threshold, the state is 3
        return (ankle_distance > self.ankle_distance_attempt) and (left_wrist_vertical_movement < self.wrist_vertical_attempt or right_wrist_vertical_movement < self.wrist_vertical_attempt)
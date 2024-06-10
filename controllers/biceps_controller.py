import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np
import random

class CurlBicepController(ShowWindow):
    def __init__(self):
        super().__init__(model_path="resources/models/model.tflite", video_path="detection/bicep.mp4")
        self.rep_count = 0
        self.error_feedback = []
        self.in_exercise = False
        self.last_keypoints = None
        self.exercise_angle_threshold = 45  # Ángulo más estricto para considerar el ejercicio correcto
        self.attempt_angle_threshold = 90  # Ángulo menos estricto para considerar un intento válido
    
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

    def check_curl_angles(self, keypoints):
        shoulder_left = keypoints[5][:2]
        elbow_left = keypoints[7][:2]
        wrist_left = keypoints[9][:2]
        shoulder_right = keypoints[6][:2]
        elbow_right = keypoints[8][:2]
        wrist_right = keypoints[10][:2]
        
        curl_angle_left = self.calculate_angle(shoulder_left, elbow_left, wrist_left)
        curl_angle_right = self.calculate_angle(shoulder_right, elbow_right, wrist_right)
        
        return curl_angle_left, curl_angle_right

    def check_back_alignment(self, keypoints):
        shoulder_left = keypoints[5][:2]
        hip_left = keypoints[11][:2]
        ankle_left = keypoints[15][:2]
        shoulder_right = keypoints[6][:2]
        hip_right = keypoints[12][:2]
        ankle_right = keypoints[16][:2]

        back_angle_left = self.calculate_angle(shoulder_left, hip_left, ankle_left)
        back_angle_right = self.calculate_angle(shoulder_right, hip_right, ankle_right)

        return back_angle_left, back_angle_right
    
    def check_body_aligment(self, keypoints):

        shoulder_right = keypoints[6][0]
        ankle_right = keypoints[16][0]

        is_correct = np.abs(np.abs(shoulder_right) - np.abs(ankle_right))

        print(is_correct)
        return is_correct > 0.45

    def evaluate_angles(self, curl_angle_left, curl_angle_right, back_angle_left, back_angle_right):
        back_straight_left = 150 <= back_angle_left <= 180
        back_straight_right = 150 <= back_angle_right <= 180

        is_correct = (curl_angle_left <= self.exercise_angle_threshold and 
                      curl_angle_right <= self.exercise_angle_threshold and 
                      back_straight_left and back_straight_right)

        score_left = (1 - abs(self.exercise_angle_threshold - curl_angle_left) / self.exercise_angle_threshold) * 100
        score_right = (1 - abs(self.exercise_angle_threshold - curl_angle_right) / self.exercise_angle_threshold) * 100
        score = np.mean([score_left, score_right])
        score_percent = score if score >= 0 else 0

        return is_correct, score_percent, back_straight_left, back_straight_right

    def determine_color(self, score):
        if score > 80:
            return "blue"
        elif 1 <= score <= 80:
            return "green"
        else:
            return "red"

    def generate_indications(self, score_percent, back_straight_left, back_straight_right, curl_angle_left, curl_angle_right):
        indications = [
            {"name": "Precision: " + str(round(score_percent, 2)) + "%", "color": self.determine_color(score_percent)},
            {"name": "Espalda recta" if back_straight_left and back_straight_right else "Corrige espalda", "color": "green" if back_straight_left and back_straight_right else "red"},
            {"name": "Curl brazo izquierdo" if curl_angle_left <= self.exercise_angle_threshold else "Corrige brazo izquierdo", "color": "green" if curl_angle_left <= self.exercise_angle_threshold else "red"},
            {"name": "Curl brazo derecho" if curl_angle_right <= self.exercise_angle_threshold else "Corrige brazo derecho", "color": "green" if curl_angle_right <= self.exercise_angle_threshold else "red"}
        ]
        return indications

    def check_exercise(self, keypoints):
        if self.last_keypoints is None:
            self.last_keypoints = keypoints
            return False

        curl_angle_left, curl_angle_right = self.check_curl_angles(keypoints)
        back_angle_left, back_angle_right = self.check_back_alignment(keypoints)
        is_correct, score_percent, back_straight_left, back_straight_right = self.evaluate_angles(curl_angle_left, curl_angle_right, back_angle_left, back_angle_right)
        indications = self.generate_indications(score_percent, back_straight_left, back_straight_right, curl_angle_left, curl_angle_right)

        is_correct = is_correct and self.check_body_aligment(keypoints)
        self.show_indications(indications)
        return is_correct 

    def check_attempt(self, keypoints):

        curl_angle_left, curl_angle_right = self.check_curl_angles(keypoints)

        is_attempt_left = curl_angle_left <= self.attempt_angle_threshold
        is_attempt_right = curl_angle_right <= self.attempt_angle_threshold

        return is_attempt_left or is_attempt_right

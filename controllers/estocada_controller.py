import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class EstocadaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/estocada.mp4')
        self.rep_count = 0
        self.initiated = False
        self.tolerance_frames = 10
        self.history_left = []
        self.history_right = []
    
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
    
    def check_attempt(self, keypoints):
        # Coordenadas relevantes
        left_hip = keypoints[11][:2]
        left_shoulder = keypoints[5][:2]
        left_knee = keypoints[13][:2]
        left_ankle = keypoints[15][:2]
        right_hip = keypoints[12][:2]
        right_knee = keypoints[14][:2]
        right_ankle = keypoints[16][:2]

        # Altura de los hombros y los hombros
        shoulder_height = (left_shoulder[1] + keypoints[6][1]) / 2  # Promedio de ambos hombros
        hip_height = (left_hip[1] + right_hip[1]) / 2  # Promedio de ambas caderas

        # Ángulo de la pierna izquierda y derecha
        knee_angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
        knee_angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)

        # Posición del cuerpo y alineación
        body_angle = self.calculate_angle(left_shoulder, left_hip, right_hip)

        # Flexión del cuerpo para determinar intento
        body_flexing = (shoulder_height - hip_height) < 150  # Valor ajustable según necesidades específicas

        # Verifica que el cuerpo empieza a inclinarse y que ambas piernas empiezan a flexionarse
        return body_flexing and body_angle < 150 and knee_angle_left < 140 and knee_angle_right < 140

    def check_exercise(self, keypoints):
        left_hip, left_knee, left_ankle = keypoints[11][:2], keypoints[13][:2], keypoints[15][:2]
        right_hip, right_knee, right_ankle = keypoints[12][:2], keypoints[14][:2], keypoints[16][:2]

        front_leg_knee_angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
        front_leg_knee_angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)

        back_leg_angle_left = self.calculate_angle(right_knee, left_knee, left_ankle)
        back_leg_angle_right = self.calculate_angle(left_knee, right_knee, right_ankle)

        horizontal_displacement = abs(left_knee[1] - right_knee[1])
        sufficient_displacement = self.check_sufficient_displacement(horizontal_displacement)

        correct_front_leg_angle_left = self.check_front_leg_angle(front_leg_knee_angle_left)
        correct_front_leg_angle_right = self.check_front_leg_angle(front_leg_knee_angle_right)
        
        correct_back_leg_angle_right = self.check_back_leg_angle(back_leg_angle_right)
        correct_back_leg_angle_left = self.check_back_leg_angle(back_leg_angle_left)

        correct_position_left = correct_front_leg_angle_left and correct_back_leg_angle_right
        correct_position_right = correct_front_leg_angle_right and correct_back_leg_angle_left

        score_left = self.calculate_score(front_leg_knee_angle_left)
        score_right = self.calculate_score(front_leg_knee_angle_right)
        
        score_percent, color = self.calculate_score_and_color(score_left, score_right)
        
        indications = self.create_indications(score_percent, color, correct_position_left, correct_position_right, 
                                            correct_front_leg_angle_left, correct_front_leg_angle_right,
                                            correct_back_leg_angle_right, correct_back_leg_angle_left)
        
        self.show_indications(indications)
        
        return (correct_position_left or correct_position_right) and sufficient_displacement

    def check_sufficient_displacement(self, displacement):
        return displacement > 0.05

    def check_front_leg_angle(self, angle):
        return 70 <= angle <= 120

    def check_back_leg_angle(self, angle):
        return angle > 130

    def calculate_score(self, angle):
        return (1 - abs(90 - angle) / 90) * 100

    def calculate_score_and_color(self, score_left, score_right):
        score = np.mean([score_left, score_right])
        score_percent = score if score >= 0 else 0
        
        if score >= 80:
            color = "blue"
        elif 1 <= score <= 80:
            color = "green"
        else:
            color = "red"
        
        return score_percent, color

    def create_indications(self, score_percent, color, correct_position_left, correct_position_right,
                        correct_front_leg_angle_left, correct_front_leg_angle_right,
                        correct_back_leg_angle_right, correct_back_leg_angle_left):
        return [
            {"name": "Precisión: " + str(round(score_percent, 2)) + "%", "color": color},
            {"name": "Piernas dobladas" if correct_position_left or correct_position_right else "Corrige piernas", "color": "green" if correct_position_left or correct_position_right else "red"},
            {"name": "Pierna delantera" if correct_front_leg_angle_left or correct_front_leg_angle_right else "Corrige pierna delantera", "color": "green" if correct_front_leg_angle_left or correct_front_leg_angle_right else "red"},
            {"name": "Pierna trasera" if correct_back_leg_angle_right or correct_back_leg_angle_left else "Corrige pierna trasera", "color": "green" if correct_back_leg_angle_right or correct_back_leg_angle_left else "red"}
        ]

    def update_history(self, correct_position_left, correct_position_right):
        self.history_left.append(correct_position_left)
        self.history_right.append(correct_position_right)

        if len(self.history_left) > self.tolerance_frames:
            self.history_left.pop(0)
        if len(self.history_right) > self.tolerance_frames:
            self.history_right.pop(0)

    def check_consistency(self, history):
        return sum(history) > len(history) // 2
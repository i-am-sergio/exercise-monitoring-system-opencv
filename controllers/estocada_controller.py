import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class EstocadaController(ShowWindow):
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
        # Verificar la ejecución con la pierna izquierda adelante
        left_hip = keypoints[11][:2]
        left_knee = keypoints[13][:2]
        left_ankle = keypoints[15][:2]
        right_hip = keypoints[12][:2]
        right_knee = keypoints[14][:2]
        right_ankle = keypoints[16][:2]

        # Determinar el ángulo en la rodilla y la cadera de la pierna adelantada (izquierda o derecha)
        front_leg_knee_angle_left = self.calculate_angle(left_hip, left_knee, left_ankle)
        front_leg_knee_angle_right = self.calculate_angle(right_hip, right_knee, right_ankle)

        # Determinar el ángulo en la rodilla de la pierna trasera (izquierda o derecha)
        back_leg_angle_left = self.calculate_angle(right_knee, left_knee, left_ankle)
        back_leg_angle_right = self.calculate_angle(left_knee, right_knee, right_ankle)

        # Chequear desplazamiento horizontal entre las rodillas para confirmar que una pierna está claramente adelantada
        horizontal_displacement = abs(left_knee[0] - right_knee[0])
        
        # Asegurar que la distancia horizontal es suficiente para considerar una pierna adelantada
        sufficient_displacement = horizontal_displacement > 0.10  # Valor ajustable según la escala de los keypoints

        # Aumentamos la tolerancia en los ángulos y aseguramos que las piernas no están paralelas
        correct_position_left = (70 <= front_leg_knee_angle_left <= 120) and (back_leg_angle_right > 150)
        correct_position_right = (70 <= front_leg_knee_angle_right <= 120) and (back_leg_angle_left > 150)

        return (correct_position_left or correct_position_right) and sufficient_displacement

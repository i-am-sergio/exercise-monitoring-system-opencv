import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np
import random

class CurlBicepController(ShowWindow):
    def __init__(self):
        super().__init__(model_path="resources/models/model.tflite", video_path="detection/bicep_curl2.mp4")
        self.rep_count = 0
        self.error_feedback = []
        self.in_exercise = False
    
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

    def valid_keypoints(self, points):
        return all([point[2] > 0.5 for point in points])  # Verificando el puntaje de confianza

    def check_exercise(self, keypoints):
        # Puntos clave del brazo izquierdo
        shoulder_left = keypoints[5][:2]
        elbow_left = keypoints[7][:2]
        wrist_left = keypoints[9][:2]

        # Puntos clave del brazo derecho
        shoulder_right = keypoints[6][:2]
        elbow_right = keypoints[8][:2]
        wrist_right = keypoints[10][:2]

        # Puntos clave de la espalda
        left_ankle = keypoints[15][:2]
        right_ankle = keypoints[16][:2]
        
        # Puntos clave del pie
        hip_left = keypoints[11][:2]
        hip_right = keypoints[12][:2]

        print(f"los puntos retornados: \n{keypoints}")

        # Calcular ángulo del curl de bíceps para el brazo izquierdo
        curl_angle_left = self.calculate_angle(shoulder_left, elbow_left, wrist_left)

        # Calcular ángulo del curl de bíceps para el brazo derecho
        curl_angle_right = self.calculate_angle(shoulder_right, elbow_right, wrist_right)

        # Calcular ángulo de la espalda usando los puntos clave del hombro y la cadera
        back_angle_left = self.calculate_angle(shoulder_left, hip_left, left_ankle)
        back_angle_right = self.calculate_angle(shoulder_right, hip_right, right_ankle)

        # Verificar si la espalda está recta (el ángulo debe ser cercano a 90 grados)
        back_straight_left = 150 <= back_angle_left <= 180
        back_straight_right = 150 <= back_angle_right <= 180

        with open("back_angle_left.txt", "a") as file:
                file.write(f"back_angle_left - back_angle_right: {back_angle_left} : {back_angle_right}\n")
        

        is_correct = False
        # if 10 <= curl_angle_left <= 60 and 10 <= curl_angle_right <= 60 and back_straight_left and back_straight_right:
        #     is_correct = True

        indications = [
            {"name": "Indicación 1", "color": "blue"},
            {"name": "Indicación 2", "color": "yellow"},
            {"name": "Indicación 3", "color": "purple"}
        ]

        # Llamamos a la función show_indications para mostrar las indicaciones
        self.show_indications(indications)
        return is_correct

    def check_attempt(self, keypoints):
        # Puntos clave del brazo izquierdo
        shoulder_left = keypoints[5][:2]
        elbow_left = keypoints[7][:2]
        wrist_left = keypoints[9][:2]

        # Puntos clave del brazo derecho
        shoulder_right = keypoints[6][:2]
        elbow_right = keypoints[8][:2]
        wrist_right = keypoints[10][:2]

        # Calcular ángulo del curl de bíceps para el brazo izquierdo
        curl_angle_left = self.calculate_angle(shoulder_left, elbow_left, wrist_left)

        # Calcular ángulo del curl de bíceps para el brazo derecho
        curl_angle_right = self.calculate_angle(shoulder_right, elbow_right, wrist_right)

        
        # with open("curl_angle_right.txt", "a") as file:
        #         file.write(f"curl_angle_left - curl_angle_right: {curl_angle_left} : {curl_angle_right}\n")

        # Verificar si el ángulo está en el rango correcto para considerar como intento
        if curl_angle_left < 90 or curl_angle_right < 90:
            return True
        else:
            return False

    
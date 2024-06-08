import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from detection.movenet_thunder import ShowWindow
import numpy as np
import tensorflow as tf

class PlanchaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/flexion.mp4')
        self.in_initial_position = False  # Nuevo estado para rastrear la posición inicial
        self.in_final_position = False  # Nuevo estado para rastrear la posición final

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def check_initial_position(self, keypoints, threshold=0.5):
        """Verifica si la posición inicial de la plancha es correcta."""
        keypoints_positions = keypoints[:, :2]
        keypoints_scores = keypoints[:, 2]

        # Extraer los puntos clave relevantes
        left_shoulder = keypoints_positions[5]
        left_elbow = keypoints_positions[7]
        left_wrist = keypoints_positions[9]
        right_shoulder = keypoints_positions[6]
        right_elbow = keypoints_positions[8]
        right_wrist = keypoints_positions[10]
        left_hip = keypoints_positions[11]
        right_hip = keypoints_positions[12]
        left_knee = keypoints_positions[13]
        right_knee = keypoints_positions[14]
        left_ankle = keypoints_positions[15]
        right_ankle = keypoints_positions[16]

        # Calcular los ángulos del codo
        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Calcular los ángulos de la cadera para asegurarse de que el cuerpo esté recto
        left_hip_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
        right_hip_angle = self.calculate_angle(right_shoulder, right_hip, right_knee)

        # Calcular los ángulos de la rodilla para asegurarse de que las piernas estén rectas
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)

        # Verificar que los ángulos de los codos estén en el rango correcto
        elbows_correct = 160 <= left_elbow_angle <= 180 and 160 <= right_elbow_angle <= 180

        # Verificar que los ángulos de la cadera estén en el rango correcto (cuerpo recto)
        hips_correct = 160 <= left_hip_angle <= 180 and 160 <= right_hip_angle <= 180

        # Verificar que los ángulos de las rodillas estén en el rango correcto (piernas rectas)
        knees_correct = 160 <= left_knee_angle <= 180 and 160 <= right_knee_angle <= 180

        return elbows_correct and hips_correct and knees_correct

    def check_final_position(self, keypoints, threshold=0.5):
        """Verifica si la posición final de la flexión es correcta."""
        keypoints_positions = keypoints[:, :2]
        # Extraer los puntos clave relevantes
        left_shoulder = keypoints_positions[5]
        left_elbow = keypoints_positions[7]
        left_wrist = keypoints_positions[9]
        right_shoulder = keypoints_positions[6]
        right_elbow = keypoints_positions[8]
        right_wrist = keypoints_positions[10]
        left_hip = keypoints_positions[11]
        right_hip = keypoints_positions[12]
        left_knee = keypoints_positions[13]
        right_knee = keypoints_positions[14]
        left_ankle = keypoints_positions[15]
        right_ankle = keypoints_positions[16]


        # Calcular los ángulos del codo
        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Calcular los ángulos de la cadera para asegurarse de que el cuerpo esté recto
        left_hip_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
        right_hip_angle = self.calculate_angle(right_shoulder, right_hip, right_knee)

        # Calcular los ángulos de la rodilla para asegurarse de que las piernas estén rectas
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)

        # Verificar que los ángulos de los codos estén en el rango correcto para la posición final
        elbows_correct = 70 <= left_elbow_angle <= 110 and 70 <= right_elbow_angle <= 110

        # Verificar que los ángulos de la cadera estén en el rango correcto (cuerpo recto)
        hips_correct = 160 <= left_hip_angle <= 180 and 160 <= right_hip_angle <= 180

        # Verificar que los ángulos de las rodillas estén en el rango correcto (piernas rectas)
        knees_correct = 160 <= left_knee_angle <= 180 and 160 <= right_knee_angle <= 180

        return elbows_correct and hips_correct and knees_correct

    def check_exercise(self, keypoints):
        if self.in_initial_position:
            # Si está en la posición inicial, verificar si ha llegado a la posición final
            if self.check_final_position(keypoints):
                self.in_initial_position = False
                self.in_final_position = True
            return False  # Aún no ha completado un ciclo
        elif self.in_final_position:
            # Si está en la posición final, verificar si ha regresado a la posición inicial
            if self.check_initial_position(keypoints):
                self.in_final_position = False
                self.in_initial_position = True
                return True  # Ha completado un ciclo
            return False  # Aún no ha regresado a la posición inicial
        else:
            # Si aún no ha comenzado, verificar si está en la posición inicial
            if self.check_initial_position(keypoints):
                self.in_initial_position = True
            return False

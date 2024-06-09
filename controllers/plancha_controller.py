import sys
import cv2
from detection.movenet_thunder import ShowWindow
import numpy as np

class PlanchaController(ShowWindow):
    def __init__(self):
        super().__init__('resources/models/model.tflite', 'detection/flexion.mp4')
        self.rep_count = 0
        self.is_plank_correct = False
        self.exercise_angle_threshold = 41  # Ángulo más estricto para considerar el ejercicio correcto
        self.attempt_angle_threshold = 150  # Ángulo menos estricto para considerar un intento válido
    
    def __del__(self):
        super().__del__()
        
    def calculate_angle(self, a, b, c):
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle
    
    def check_exercise(self, keypoints):
        # Definimos los índices de los puntos de referencia relevantes para la flexión (push-up)
        left_shoulder = keypoints[5]  # Índice 5 para el hombro izquierdo
        left_elbow = keypoints[7]     # Índice 7 para el codo izquierdo
        left_wrist = keypoints[9]     # Índice 9 para la muñeca izquierda
        
        right_shoulder = keypoints[6]  # Índice 6 para el hombro derecho
        right_elbow = keypoints[8]     # Índice 8 para el codo derecho
        right_wrist = keypoints[10]    # Índice 10 para la muñeca derecha
        
        # Calculamos los ángulos relevantes para verificar la flexión en ambos lados
        angle_left = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        angle_right = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        # Verificamos si el ángulo en ambos lados es menor que el umbral dado
        is_correct_left = angle_left < self.exercise_angle_threshold
        is_correct_right = angle_right < self.exercise_angle_threshold
        
        # Ejemplo de indicaciones aleatorias con precisión
        score_left = (1 - abs(self.exercise_angle_threshold - angle_left) / self.exercise_angle_threshold ) * 100 
        score_right = (1 - abs(self.exercise_angle_threshold - angle_right) / self.exercise_angle_threshold ) * 100 
        
        # Calcular el promedio de precisión entre los lados
        score = np.mean([score_left, score_right])
        score_porcent = score if score >= 0 else 0

        # Determinar el color basado en la precisión
        if score > 80:
            color = "blue"
        elif 1 <= score <= 80:
            color = "green"
        else:
            color = "red"
        # Verificar si las rodillas, caderas y pies están alineados correctamente
        is_body_straight = self.check_body_alignment(keypoints, 120, 170)
        
        # Verificar si la cabeza está alineada con los hombros
        is_head_straight = self.check_head_alignment(keypoints, 0 , 90)

        # Verificar si las piernas están juntas
        are_legs_together = self.check_legs_together(keypoints, 80, 180)
        
        
        # Crear las indicaciones con el mensaje descriptivo
        indications = [
            {"name": "Precision: " + str(round(score_porcent, 2)) + "%", "color": color},
            {"name": "Cabeza recta" if is_head_straight else "Cabeza inclinada", "color": "green" if is_head_straight else "orange"},
            {"name": "Cuerpo recto" if is_body_straight else "Cuerpo inclinado", "color": "green" if is_body_straight else "red"},
            {"name": "Piernas juntas" if are_legs_together else "Piernas separadas", "color": "green" if are_legs_together else "orange"}
        ]
        
        # Llamamos a la función show_indications para mostrar las indicaciones
        self.show_indications(indications)
        
        # Devolvemos True si el ejercicio se realiza correctamente en ambos lados
        return is_correct_left and is_correct_right


    def check_attempt(self, keypoints):
        # Definimos los índices de los puntos de referencia relevantes para la flexión (push-up)
        left_shoulder = keypoints[5]  # Índice 5 para el hombro izquierdo
        left_elbow = keypoints[7]     # Índice 7 para el codo izquierdo
        left_wrist = keypoints[9]     # Índice 9 para la muñeca izquierda
        
        right_shoulder = keypoints[6]  # Índice 6 para el hombro derecho
        right_elbow = keypoints[8]     # Índice 8 para el codo derecho
        right_wrist = keypoints[10]    # Índice 10 para la muñeca derecha
        
        # Calculamos los ángulos relevantes para verificar la flexión en ambos lados
        angle_left = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        angle_right = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        # Verificamos si el ángulo en ambos lados es menor que el umbral dado
        is_attempt_left = angle_left < self.attempt_angle_threshold
        is_attempt_right = angle_right < self.attempt_angle_threshold
        
        # Devolvemos True si el intento es válido en al menos un lado
        return is_attempt_left and is_attempt_right
    
    def check_body_alignment(self, keypoints, min_angle, max_angle):
        # Definir los índices para los puntos de referencia del cuerpo
        left_knee = keypoints[13]  # Índice 11 para la rodilla izquierda
        left_hip = keypoints[11]  # Índice 15 para el cadera izquierdo
        left_shoulder = keypoints[5]  # Índice 13 para la hombro izquierda

        right_knee = keypoints[14]  # Índice 12 para la rodilla derecha
        right_hip = keypoints[12]  # Índice 14 para la cadera derecha
        right_shoulder = keypoints[6]  # Índice 16 para el hombro derecho
        
        # Calcular los ángulos de las caderas, rodillas y tobillos
        angle_hip_left = self.calculate_angle(left_knee, left_hip, left_shoulder)
        angle_hip_right = self.calculate_angle(right_knee, right_hip, right_shoulder)
        # Verificar si los ángulos están dentro del rango especificado
        return min_angle <= angle_hip_left <= max_angle and min_angle <= angle_hip_right <= max_angle
    
    def check_head_alignment(self, keypoints, min_angle, max_angle):
        # Definir los índices para los puntos de referencia de la cabeza y los hombros
        left_shoulder = keypoints[5]
        right_shoulder = keypoints[6]
        nose = keypoints[0]

        # Calcular el ángulo entre la cabeza y los hombros
        angle_head_shoulder_left = self.calculate_angle(left_shoulder, nose, right_shoulder)
        
        # Verificar si el ángulo es menor que el umbral especificado
        return angle_head_shoulder_left >= min_angle and angle_head_shoulder_left <= max_angle
    
    def check_legs_together(self, keypoints, angle_min, angle_max):
        # Definir los índices para los puntos de referencia de las caderas, rodillas y tobillos
        hip_right = keypoints[12]
        knee_left = keypoints[13]
        knee_right = keypoints[14]

        # Calcular los ángulos entre las caderas y las rodillas
        angle_hip_right_knee = self.calculate_angle(hip_right, knee_right, knee_left)
        
        # Verificar si los ángulos están dentro del rango especificado
        return  angle_min <= angle_hip_right_knee <= angle_max 
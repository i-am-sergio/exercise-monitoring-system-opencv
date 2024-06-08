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
        self.rep_count = 0
        self.is_plank_correct = False
        self.angle_attempt = 100  # Puedes ajustar este ángulo según sea necesario
    
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
    
    def check_exercise(self, keypoints):
        # Definimos los índices de los puntos de referencia relevantes para la flexión (push-up)
        left_shoulder = keypoints[5][:2]  # Índice 5 para el hombro izquierdo
        left_elbow = keypoints[7][:2]     # Índice 7 para el codo izquierdo
        left_wrist = keypoints[9][:2]     # Índice 9 para la muñeca izquierda
        
        # Calculamos los ángulos relevantes para verificar la flexión
        angle1 = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        
        # Si el ángulo entre el hombro, codo y muñeca es menor que un umbral dado, consideramos la flexión correcta
        return angle1 < 90  # Puedes ajustar este umbral según sea necesario

    def check_attempt(self, keypoints):
        # Definimos los índices de los puntos de referencia relevantes para la flexión (push-up)
        left_shoulder = keypoints[5][:2]  # Índice 5 para el hombro izquierdo
        left_elbow = keypoints[7][:2]     # Índice 7 para el codo izquierdo
        left_wrist = keypoints[9][:2]     # Índice 9 para la muñeca izquierda
        
        # Calculamos los ángulos relevantes para verificar la flexión
        angle1 = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        
        # Si el ángulo entre el hombro, codo y muñeca es menor que un umbral dado, consideramos el intento de flexión válido
        return angle1 < self.angle_attempt  # Puedes ajustar este umbral según sea necesario

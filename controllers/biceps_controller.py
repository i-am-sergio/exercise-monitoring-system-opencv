import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np
import random 


class CurlBicepController(ShowWindow):
    def __init__(self):
        super().__init__( model_path="resources/models/model.tflite", video_path="detection/bicep_curl.mp4",)
        self.rep_count = 0
    
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
        # Puntos clave del brazo izquierdo
        elbow_left = keypoints[13][:2]
        wrist_left = keypoints[15][:2]
        shoulder_left = keypoints[11][:2]
        
        # Puntos clave del brazo derecho
        elbow_right = keypoints[12][:2]
        wrist_right = keypoints[14][:2]
        shoulder_right = keypoints[12][:2]
        
        print(f"los puntos retornados: \n{keypoints}")
        # Calcular ángulo del curl de bíceps para el brazo izquierdo
        curl_angle_left = self.calculate_angle(elbow_left, wrist_left, shoulder_left)
        
        # Calcular ángulo del curl de bíceps para el brazo derecho
        curl_angle_right = self.calculate_angle(elbow_right, wrist_right, shoulder_right)
        
        return random.randint(0,1)

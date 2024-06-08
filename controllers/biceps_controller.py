import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np


class CurlBicepController(ShowWindow):
    def __init__(self):
        super().__init__( model_path="resources/models/thunder.tflite", video_path="detection/video_completo.mp4",)
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
        elbow = keypoints[12][:2]
        wrist = keypoints[14][:2]
        shoulder = keypoints[11][:2]
        
        curl_angle = self.calculate_angle(elbow, wrist, shoulder)
        
        return 80 <= curl_angle <= 160

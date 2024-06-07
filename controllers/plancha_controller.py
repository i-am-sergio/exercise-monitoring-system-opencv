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
        super().__init__('resources/models/thunder.tflite', 'detection/flexion_fragment.mp4')

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
        left_shoulder = keypoints[5][:2]
        left_elbow = keypoints[7][:2]
        left_wrist = keypoints[9][:2]
        right_shoulder = keypoints[6][:2]
        right_elbow = keypoints[8][:2]
        right_wrist = keypoints[10][:2]

        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)

        if 160 <= left_elbow_angle <= 180 and 160 <= right_elbow_angle <= 180:
            return True
        return False

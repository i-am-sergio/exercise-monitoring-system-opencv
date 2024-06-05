import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np


class CurlBicepController(ShowWindow):
    def __init__(self):
        super().__init__(video_source="detection/video_completo.mp4", model_path="resources/models/thunder.tflite")
        self.rep_count = 0
        # self.interpreter = tf.lite.Interpreter(model_path='resources/models/thunder.tflite')
        # self.interpreter.allocate_tensors()
    
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
    
    def check_curl(self, keypoints):
        elbow = keypoints[12][:2]
        wrist = keypoints[14][:2]
        shoulder = keypoints[11][:2]
        
        curl_angle = self.calculate_angle(elbow, wrist, shoulder)
        
        return 80 <= curl_angle <= 160
    
    def draw_feedback(self, frame, is_curl_correct):
        text = "Curl Correct" if is_curl_correct else "Curl Incorrect"
        color = (0, 255, 0) if is_curl_correct else (0, 0, 255)
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    
    def annotate_frame(self, frame, keypoints_with_scores):
        keypoints = keypoints_with_scores[0][0]
        is_curl_correct = self.check_curl(keypoints)

        self.draw_connections(frame, keypoints_with_scores, self.edges, 0.4)
        self.draw_keypoints(frame, keypoints_with_scores, 0.4)
        self.draw_feedback(frame, is_curl_correct)

    def show(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            keypoints_with_scores = self.process_frame(frame)

            self.annotate_frame(frame, keypoints_with_scores)

            cv2.imshow('Curl Detection', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            if cv2.getWindowProperty('Curl Detection', cv2.WND_PROP_VISIBLE) < 1:
                break

        self.cap.release()
        cv2.destroyAllWindows()

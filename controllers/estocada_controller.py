import cv2
import tensorflow as tf
import numpy as np
from detection.movenet_thunder import ShowWindow

class EstocadaController(ShowWindow):
    def __init__(self):
        super().__init__(video_source="detection/video_completo.mp4", model_path="resources/models/thunder.tflite")
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
    
    def check_lunge(self, keypoints):
        left_hip = keypoints[11][:2]
        left_knee = keypoints[13][:2]
        left_ankle = keypoints[15][:2]
        
        # Use left shoulder (index 5) for hip angle calculation
        left_shoulder = keypoints[5][:2]
        
        # Calculate angles
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        left_hip_angle = self.calculate_angle(left_knee, left_hip, left_shoulder)
        
        if not self.initiated:
            # Check if the lunge is starting
            if 150 <= left_knee_angle <= 180 and 140 <= left_hip_angle <= 180:
                self.initiated = True
                return "Starting Lunge"
        else:
            # Check if the lunge is complete
            if 70 <= left_knee_angle <= 110:
                self.initiated = False
                self.rep_count += 1
                return "Lunge Complete"
        
        return "Not a Lunge"
    
    def draw_feedback(self, frame, lunge_status):
        text = lunge_status
        color = (0, 255, 0) if lunge_status == "Lunge Complete" else (0, 0, 255)
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        cv2.putText(frame, f'Reps: {self.rep_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    def annotate_frame(self, frame, keypoints_with_scores):
        keypoints = keypoints_with_scores[0][0]
        lunge_status = self.check_lunge(keypoints)
        
        self.draw_connections(frame, keypoints_with_scores, self.edges, 0.4)
        self.draw_keypoints(frame, keypoints_with_scores, 0.4)
        self.draw_feedback(frame, lunge_status)

    def show(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            keypoints_with_scores = self.process_frame(frame)

            self.annotate_frame(frame, keypoints_with_scores)

            cv2.imshow('Estocada Detection', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            if cv2.getWindowProperty('Estocada Detection', cv2.WND_PROP_VISIBLE) < 1:
                break

        self.cap.release()
        cv2.destroyAllWindows()
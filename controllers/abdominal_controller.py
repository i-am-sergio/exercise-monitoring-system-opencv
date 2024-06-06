
import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np

class AbdominalController(ShowWindow):
    def __init__(self):
        super().__init__(video_source="detection/video_completo.mp4", model_path="resources/models/thunder.tflite")
        self.rep_count = 0
        self.is_crunch_correct = False  # Boolean to track the state of crunch correctness
    
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
    
    def check_crunch(self, keypoints):
        # Left hip (11), left shoulder (5), and left knee (13)
        hip = keypoints[11][:2]
        shoulder = keypoints[5][:2]
        knee = keypoints[13][:2]
        
        crunch_angle = self.calculate_angle(knee, hip, shoulder)
        
        return crunch_angle < 60  # Reduced threshold angle for crunch detection
    
    def draw_feedback(self, frame, is_crunch_correct):
        if is_crunch_correct and not self.is_crunch_correct:
            self.rep_count += 1
            self.is_crunch_correct = True
        elif not is_crunch_correct:
            self.is_crunch_correct = False

        text = f"Crunch {'Correct' if is_crunch_correct else 'Incorrect'} - Count: {self.rep_count}"
        color = (0, 255, 0) if is_crunch_correct else (0, 0, 255)
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    
    def annotate_frame(self, frame, keypoints_with_scores):
        keypoints = keypoints_with_scores[0][0]
        is_crunch_correct = self.check_crunch(keypoints)

        self.draw_connections(frame, keypoints_with_scores, self.edges, 0.4)
        self.draw_keypoints(frame, keypoints_with_scores, 0.4)
        self.draw_feedback(frame, is_crunch_correct)

    def show(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            keypoints_with_scores = self.process_frame(frame)

            self.annotate_frame(frame, keypoints_with_scores)

            cv2.imshow('Crunch Detection', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            if cv2.getWindowProperty('Crunch Detection', cv2.WND_PROP_VISIBLE) < 1:
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    controller = AbdominalController()
    controller.show()


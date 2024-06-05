import tensorflow as tf
from detection.movenet_thunder import ShowWindow
import cv2
import numpy as np

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

class CurlBicepController(ShowWindow):
    def __init__(self):
        super().__init__(video_source="detection/video_completo.mp4")
        self.rep_count = 0
        self.interpreter = tf.lite.Interpreter(model_path='resources/models/thunder.tflite')
        self.interpreter.allocate_tensors()
    
    def __del__(self):
        super().__del__()
        
    def calculate_angle(self, a, b, c):
        """Calculate the angle between three points."""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle
    
    def check_curl(self, keypoints):
        """Check if the curl position is correct based on keypoints."""
        # Get the keypoints for the elbow, wrist, and shoulder
        elbow = keypoints[12][:2]
        wrist = keypoints[14][:2]
        shoulder = keypoints[11][:2]
        
        # Calculate the angle between the arm segments
        curl_angle = self.calculate_angle(elbow, wrist, shoulder)
        
        # Check if the angle is within a reasonable range for a curl
        return 80 <= curl_angle <= 160
    
    def draw_feedback(self, frame, is_curl_correct):
        """Draw feedback on the frame."""
        text = "Curl Correct" if is_curl_correct else "Curl Incorrect"
        color = (0, 255, 0) if is_curl_correct else (0, 0, 255)
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    
    def show(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Reshape image
            img = frame.copy()
            img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256, 256)
            input_image = tf.cast(img, dtype=tf.float32)
            
            # Setup input and output
            input_details = self.interpreter.get_input_details()
            output_details = self.interpreter.get_output_details()
            
            # Make predictions
            self.interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
            self.interpreter.invoke()
            keypoints_with_scores = self.interpreter.get_tensor(output_details[0]['index'])
            keypoints = keypoints_with_scores[0][0]
            
            # Check curl position
            is_curl_correct = self.check_curl(keypoints)
            
            # Rendering
            self.draw_connections(frame, keypoints_with_scores, EDGES, 0.4)
            self.draw_keypoints(frame, keypoints_with_scores, 0.4)
            self.draw_feedback(frame, is_curl_correct)
            
            cv2.imshow('Curl Detection', frame)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
            if cv2.getWindowProperty('Curl Detection', cv2.WND_PROP_VISIBLE) < 1:
                break

        self.cap.release()
        cv2.destroyAllWindows()

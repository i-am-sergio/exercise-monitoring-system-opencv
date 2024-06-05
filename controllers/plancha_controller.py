from detection.movenet_thunder import ShowWindow
import cv2
import tensorflow as tf
import numpy as np

EDGES = {
    (0, 1): 'm', (0, 2): 'c', (1, 3): 'm', (2, 4): 'c', (0, 5): 'm', (0, 6): 'c',
    (5, 7): 'm', (7, 9): 'm', (6, 8): 'c', (8, 10): 'c', (5, 6): 'y', (5, 11): 'm',
    (6, 12): 'c', (11, 12): 'y', (11, 13): 'm', (13, 15): 'm', (12, 14): 'c',
    (14, 16): 'c'
}

# Hereda de la clase ShowWindow
class PlanchaController(ShowWindow):
    def __init__(self):
        super().__init__(video_source="detection/flexion_fragment.mp4")
        self.rep_count = 0
        self.in_lunge_position = False
        self.interpreter = tf.lite.Interpreter(model_path='resources/models/thunder.tflite')
        self.interpreter.allocate_tensors()
    
    def __del__(self):
        super().__del__()
    
    def show(self):
        super().show()
        self.cap.release()
        cv2.destroyAllWindows()
    
    def calculate_angle(self,  a, b, c):
        """Calculate the angle between three points."""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle
    def check_plancha(self, keypoints):
        left_shoulder = keypoints[5][:2]
        left_elbow = keypoints[7][:2]
        left_wrist = keypoints[9][:2]
        
        right_shoulder = keypoints[6][:2]
        right_elbow = keypoints[8][:2]
        right_wrist = keypoints[10][:2]
        
        # Calculate angles
        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        # Check if angles are within the correct range for a push-up
        if 160 <= left_elbow_angle <= 180 and 160 <= right_elbow_angle <= 180:
            return True
        return False
    
    def draw_feedback(self, frame, is_push_up_correct):
        """Draw feedback on the frame."""
        text = "Push-Up Correct" if is_push_up_correct else "Push-Up Incorrect"
        color = (0, 255, 0) if is_push_up_correct else (0, 0, 255)
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
            
            # Check push-up position
            is_push_up_correct = self.check_plancha(keypoints)
            
            # Rendering
            self.draw_connections(frame, keypoints_with_scores, EDGES, 0.4)
            self.draw_keypoints(frame, keypoints_with_scores, 0.4)
            self.draw_feedback(frame, is_push_up_correct)
            
            cv2.imshow('Push-Up Detection', frame)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            
            if cv2.getWindowProperty('Push-Up Detection', cv2.WND_PROP_VISIBLE) < 1:
                break

        self.cap.release()
        cv2.destroyAllWindows()
    
    def calculate_time(self):
        pass

    def calculate_speed(self):
        pass



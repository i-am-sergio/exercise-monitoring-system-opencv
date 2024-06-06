import cv2
import tensorflow as tf
import numpy as np
from abc import ABC, abstractmethod
# interpreter = tf.lite.Interpreter(model_path='resources/models/thunder.tflite')
# interpreter.allocate_tensors()

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

class ShowWindow(ABC):
    def __init__(self, video_source=0, model_path='resources/models/thunder.tflite'):
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError(f"Error opening video source: {video_source}")
        
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.edges = EDGES

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
    def draw_keypoints(self, frame, keypoints, confidence_threshold):
        y, x, _ = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

        for kp in shaped:
            ky, kx, kp_conf = kp
            if kp_conf > confidence_threshold:
                cv2.circle(frame, (int(kx), int(ky)), 4, (0, 255, 0), -1)
    
    def draw_connections(self, frame, keypoints, edges, confidence_threshold):
        y, x, _ = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))
        
        for edge, _ in edges.items():
            p1, p2 = edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]
            
            if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

    def process_frame(self, frame):
        img = frame.copy()
        img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256, 256)
        input_image = tf.cast(img, dtype=tf.float32)
        
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        self.interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
        self.interpreter.invoke()
        keypoints_with_scores = self.interpreter.get_tensor(output_details[0]['index'])

        return keypoints_with_scores

    @abstractmethod
    def annotate_frame(self, frame, keypoints_with_scores):
        """Abstract method to be implemented by subclasses to add custom annotations."""
        pass

    @abstractmethod
    def show(self):
        """Abstract method to be implemented by subclasses for the main loop."""
        pass

if __name__ == '__main__':
    sw = ShowWindow()
    sw.show()
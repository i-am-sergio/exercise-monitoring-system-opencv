import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import tensorflow as tf

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

class PlanchaController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.resize(800, 600)  # Establecer un tamaño más grande para la ventana
        self.label = QLabel(self.window)
        self.window.setCentralWidget(self.label)

        #cargar modelo
        self.interpreter = tf.lite.Interpreter(model_path='resources/models/thunder.tflite')
        self.interpreter.allocate_tensors()

        #mostrar el texto
        self.feedback_label = QLabel(self.window)
        self.feedback_label.setGeometry(10, 10, 300, 30)  # Posición y tamaño del QLabel
        self.feedback_label.setAlignment(Qt.AlignTop)  # Alinear el texto en la parte superior del QLabel

        self.correct_repetitions = 0
        self.incorrect_repetitions = 0

        #mostrar correctas
        self.correct_label = QLabel(self.window)
        self.correct_label.setGeometry(10, 50, 300, 30)
        self.correct_label.setAlignment(Qt.AlignTop)
        #mostrar incorrectas
        self.incorrect_label = QLabel(self.window)
        self.incorrect_label.setGeometry(10, 70, 300, 30)
        self.incorrect_label.setAlignment(Qt.AlignTop)

        self.previous_plancha_state = None

    def show(self):
        self.video_path = "detection/flexion_fragment.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir el video.")
            return

        # Configurar temporizador para actualizar la ventana
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_window)
        self.timer.start(16) # Actualizar cada 33 milisegundos (aproximadamente 30 fps)

    def draw_keypoints(self, frame, keypoints, confidence_threshold):
        y, x, _ = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))

        for kp in shaped:
            ky, kx, kp_conf = kp
            if kp_conf > confidence_threshold:
                cv2.circle(frame, (int(kx), int(ky)), 4, (0,255,0), -1)
    
    def draw_connections(self, frame, keypoints, edges, confidence_threshold):
        y, x, _ = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
        
        for edge, _ in edges.items():
            p1, p2 = edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]
            
            if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 2)


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

    def show_feedback(self, is_plancha_correct):
        if is_plancha_correct:
            text = "Plancha Correcta"
            color = "green"
        else:
            text = "Plancha Incorrecta"
            color = "red"
        
        self.feedback_label.setText(text)
        self.feedback_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold;")
        self.feedback_label.show()

        self.correct_label.setText(f"Planchas Correctas: {self.correct_repetitions}")
        self.incorrect_label.setText(f"Planchas Incorrectas: {self.incorrect_repetitions}")
        self.correct_label.show()
        self.incorrect_label.show()
        
    def update_window(self):
        ret, frame = self.cap.read()
        if not ret:
            # Detener el temporizador cuando el video termina
            self.timer.stop()
            self.cap.release()
            return

        # Mostrar la imagen en la ventana
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
        
        is_plancha_correct = self.check_plancha(keypoints)

        # Verificar si el estado actual es diferente al anterior
        if self.previous_plancha_state is None:
            self.previous_plancha_state = is_plancha_correct
        elif self.previous_plancha_state != is_plancha_correct:
            self.previous_plancha_state = is_plancha_correct

            # Incrementar el contador correspondiente
            if is_plancha_correct:
                self.correct_repetitions += 1
            else:
                self.incorrect_repetitions += 1

            # Actualizar las etiquetas en la ventana
            self.show_feedback(is_plancha_correct)

        self.draw_connections(frame, keypoints_with_scores, EDGES, 0.4)
        self.draw_keypoints(frame, keypoints_with_scores, 0.4)
        self.show_image(frame)
        
    def show_image(self, image):
        # Convertir la imagen de BGR a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convertir la imagen de OpenCV a formato QImage
        height, width, channel = image_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Escalar la imagen para que se ajuste al tamaño de la ventana
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(self.window.size(), Qt.KeepAspectRatio)
        
        # Mostrar la imagen en la ventana
        self.label.setPixmap(scaled_pixmap)
        self.window.show()
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
import cv2
import tensorflow as tf
import numpy as np

from PyQt5.QtCore import Qt, QTimer

interpreter = tf.lite.Interpreter(model_path='resources/models/thunder.tflite')
interpreter.allocate_tensors()

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


class BaseController:
    def __init__(self, model_path, video_path):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("Exercices Opencv + Qt")
        self.window.resize(1200, 700)
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)  # Utiliza setCentralWidget en lugar de crear otro widget central

        # Layout de cuadrícula
        grid_layout = QGridLayout(central_widget)
        grid_layout.setColumnStretch(0, 3)  # Columna 0 con tamaño 3
        grid_layout.setColumnStretch(1, 1)  # Columna 1 con tamaño 1
        grid_layout.setRowStretch(0, 1)  # Fila 0 con tamaño 1

        # Contenedor 1
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)
        self.video_label = QLabel("Video Label")
        self.video_label.setAlignment(Qt.AlignCenter) 
        self.layout.addWidget(self.video_label)
        self.main_widget.setStyleSheet('background-color: red')
        grid_layout.addWidget(self.main_widget, 0, 0, alignment=Qt.AlignCenter)


        # Contenedor 2 con QVBoxLayout
        second_widget = QWidget()
        second_layout = QVBoxLayout(second_widget)
        grid_layout.addWidget(second_widget, 0, 1)

        # Etiquetas en el segundo contenedor
        self.feedback_label = QLabel()
        self.correct_label = QLabel()
        self.incorrect_label = QLabel()
        second_layout.addWidget(self.feedback_label)
        second_layout.addWidget(self.correct_label)
        second_layout.addWidget(self.incorrect_label)

        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.correct_repetitions = 0
        self.incorrect_repetitions = 0
        self.previous_state = None
        self.video_path = video_path

        self.window.closeEvent = self.closeEvent

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        self.app.quit()


    def show(self):
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir el video.")
            return

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_window)
        self.timer.start(16)

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

    def show_feedback(self, is_correct):
        if is_correct:
            text = "Correcto"
            color = "green"
        else:
            text = "Incorrecto"
            color = "red"

        self.feedback_label.setText(text)
        self.feedback_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold;")
        self.feedback_label.show()

        self.correct_label.setText(f"Correctas: {self.correct_repetitions}")
        self.incorrect_label.setText(f"Incorrectas: {self.incorrect_repetitions}")
        self.correct_label.show()
        self.incorrect_label.show()

    def update_window(self):
        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            self.cap.release()
            return

        img = frame.copy()
        img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256, 256)
        input_image = tf.cast(img, dtype=tf.float32)

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        self.interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
        self.interpreter.invoke()
        keypoints_with_scores = self.interpreter.get_tensor(output_details[0]['index'])
        keypoints = keypoints_with_scores[0][0]

        is_correct = self.check_exercise(keypoints)

        if self.previous_state is None:
            self.previous_state = is_correct
        elif self.previous_state != is_correct:
            self.previous_state = is_correct

            if is_correct:
                self.correct_repetitions += 1
            else:
                self.incorrect_repetitions += 1

            self.show_feedback(is_correct)

        self.draw_connections(frame, keypoints_with_scores, EDGES, 0.4)
        self.draw_keypoints(frame, keypoints_with_scores, 0.4)
        self.show_image(frame)

    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap)
        self.window.show()

class ShowWindow(QMainWindow):
    def __init__(self, video_source=0):
        super().__init__()
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError(f"Error opening video source: {video_source}")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.label = QLabel()
        self.layout.addWidget(self.label)

    def __del__(self):
        self.cap.release()

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

    def show_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.label.setPixmap(pixmap)

    def show(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            # Reshape image
            img = frame.copy()
            img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256,256)
            input_image = tf.cast(img, dtype=tf.float32)

            # Setup input and output 
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            # Make predictions 
            interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
            interpreter.invoke()
            keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])

            self.draw_connections(frame, keypoints_with_scores, EDGES, 0.4)
            self.draw_keypoints(frame, keypoints_with_scores, 0.4)

            self.show_frame(frame)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = ShowWindow()
    sw.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout,  QPushButton, QGroupBox
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

import cv2
import tensorflow as tf
import numpy as np
import time
from PyQt5.QtCore import Qt, QTimer


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

COLOR_MAP = {
    'm': (255, 0, 255),  # Magenta
    'c': (0, 255, 255),  # Cyan
    'y': (255, 255, 0),  # Yellow
}
class ShowWindow:
    def __init__(self, model_path="resources/models/model.tflite", video_path=0):
        self.window = QMainWindow()
        self.window.setWindowTitle("Ejercicios Opencv + Qt")
        self.window.resize(1200, 700)
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)  

        grid_layout = QGridLayout(central_widget)
        grid_layout.setColumnStretch(0, 3)  
        grid_layout.setColumnStretch(1, 1)  
        grid_layout.setRowStretch(0, 1)  

        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)
        self.video_label = QLabel("Video Label")
        self.video_label.setAlignment(Qt.AlignCenter) 
        self.layout.addWidget(self.video_label)
        grid_layout.addWidget(self.main_widget, 0, 0, alignment=Qt.AlignCenter)

        second_widget = QWidget()
        self.second_layout = QVBoxLayout(second_widget)

        exit_button = QPushButton("Salir")
        exit_button.clicked.connect(self.exit_application)

        font = QFont()
        font.setFamily("URW Bookman [urw]")
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)

        # Grupo para los labels
        labels_groupbox = QGroupBox("Contadores")
        labels_groupbox.setStyleSheet("QGroupBox { font-size: 30px; }")
        labels_groupbox.setAlignment(Qt.AlignCenter)
        labels_groupbox.setFont(font)
        
        labels_layout = QVBoxLayout(labels_groupbox)

        # Crear los labels con estilos predefinidos
        self.correct_label = QLabel()
        self.correct_label.setStyleSheet("color: blue; font-size: 20px; font-weight: bold;")
        self.incorrect_label = QLabel()
        self.incorrect_label.setStyleSheet("color: red; font-size: 20px; font-weight: bold;")
        self.state_label = QLabel()

        font2 = QFont()
        font2.setFamily("URW Bookman [urw]")
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(35)

        self.correct_label.setFont(font2)
        self.incorrect_label.setFont(font2)
        self.state_label.setFont(font2)

        # Añade los labels al grupo

        labels_layout.addWidget(self.state_label)
        labels_layout.addWidget(self.correct_label)
        labels_layout.addWidget(self.incorrect_label)

        self.second_layout.addWidget(labels_groupbox)

        # Crea un QGroupBox para las indicaciones
        indications_groupbox = QGroupBox("Indicaciones")
        indications_groupbox.setStyleSheet("QGroupBox { font-size: 30px; }")
        indications_groupbox.setFont(font)
        self.indications_layout = QVBoxLayout(indications_groupbox)
        self.indications_layout.setAlignment(Qt.AlignCenter) 
        self.indications_label = QLabel()  
        self.indications_label.setAlignment(Qt.AlignCenter)
        self.indications_label.setFixedSize(200, 100) 
        self.indications_layout.addWidget(self.indications_label) 
        self.second_layout.addWidget(indications_groupbox)

        # Añade el botón "Salir" como último elemento del layout
        self.second_layout.addWidget(exit_button)

        # Añade el segundo contenedor al grid layout
        grid_layout.addWidget(second_widget, 0, 1)

        self.indications = []
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.edges = [
            (0, 1), (0, 2), (1, 3), (2, 4), (0, 5), (0, 6), (5, 7),
            (7, 9), (6, 8), (8, 10), (5, 6), (5, 11), (6, 12),
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16)
        ]
        self.edge_colors = [
            (255, 0, 0), (0, 255, 0), (255, 0, 0), (0, 255, 0), 
            (255, 0, 0), (0, 255, 0), (255, 0, 0), (255, 0, 0),
            (0, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0),
            (0, 255, 0), (0, 255, 255), (255, 0, 0), (255, 0, 0),
            (0, 255, 0), (0, 255, 0)
        ]
        input_details = self.interpreter.get_input_details()
        self.input_shape = input_details[0]['shape']

        self.correct_repetitions = 0
        self.incorrect_repetitions = 0
        self.previous_state = None
        self.correct_state = False
        self.correct_state = False
        self.initiated = False
        self.video_path = video_path
        self.response_final = 0
        
        self.response_final = 0
        

    def exit_application(self):
            self.cap.release()
            self.timer.stop()
            self.window.close()

    def __del__(self):
        try:
            self.cap.release()
        except AttributeError:
            pass
        try:
            self.timer.stop()
        except AttributeError:
            pass

    def show(self):
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir el video.")
            return
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_duration = 1.0 / self.fps
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_duration = 1.0 / self.fps
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_window)
        self.timer.start(16)

    
    def get_keypoints(self, image):
        input_image = tf.image.resize(image, (self.input_shape[1], self.input_shape[2]))
        input_image = tf.cast(input_image, dtype=tf.uint8)
        input_image = tf.expand_dims(input_image, axis=0)
        self.interpreter.set_tensor(self.interpreter.get_input_details()[0]['index'], input_image)
        self.interpreter.invoke()
        keypoints_with_scores = self.interpreter.get_tensor(self.interpreter.get_output_details()[0]['index'])
        return keypoints_with_scores
    

    def draw_predictions_on_image(self, image, keypoints_with_scores, keypoint_threshold=0.11):
        height, width, _ = image.shape
        keypoints = keypoints_with_scores[0, 0, :, :2]
        keypoints_scores = keypoints_with_scores[0, 0, :, 2]

        for idx, ((start, end), color) in enumerate(zip(self.edges, self.edge_colors)):
            if keypoints_scores[start] > keypoint_threshold and keypoints_scores[end] > keypoint_threshold:
                start_point = (int(keypoints[start, 1] * width), int(keypoints[start, 0] * height))
                end_point = (int(keypoints[end, 1] * width), int(keypoints[end, 0] * height))
                cv2.line(image, start_point, end_point, color, 2)
        for i in range(keypoints.shape[0]):
            if keypoints_scores[i] > keypoint_threshold:
                center = (int(keypoints[i, 1] * width), int(keypoints[i, 0] * height))
                cv2.circle(image, center, 3, (0, 0, 255), -1)
        return image

    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = image_rgb.shape
        container_height, container_width = self.video_label.height(), self.video_label.width()
        image_aspect_ratio = image_width / image_height
        container_aspect_ratio = container_width / container_height
        if image_aspect_ratio > container_aspect_ratio:
            new_height = container_height
            new_width = int(container_height * image_aspect_ratio)
        else:
            new_width = container_width
            new_height = int(container_width / image_aspect_ratio)
        resized_image = cv2.resize(image_rgb, (new_width, new_height))
        bytes_per_line = 3 * new_width
        q_image = QImage(resized_image.data, new_width, new_height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap)
        self.window.show()

    def calculate_incorrect_duration(self):
        incorrect_duration_frames = sum(1 for s in self.current_sequence if s == self.INCORRECT_STATE)
        return incorrect_duration_frames * self.frame_duration
    
    def handle_rest_state(self):
        if self.current_sequence:
            incorrect_duration_seconds = self.calculate_incorrect_duration()
            total_duration_seconds = len(self.current_sequence) * self.frame_duration

            if incorrect_duration_seconds == 0 or incorrect_duration_seconds / total_duration_seconds <= 2:
                self.correct_repetitions += 1
                self.response_final = 1
            else:
                self.incorrect_repetitions += 1
                self.response_final = 2

            self.current_sequence = []
            
    def handle_incorrect_state(self):
        incorrect_duration_seconds = self.calculate_incorrect_duration()
        if incorrect_duration_seconds > 2:
            self.incorrect_repetitions += 1
            self.response_final = 2
            self.current_sequence = []
            
    def update_window(self):
        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            self.cap.release()
            return


        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        keypoints_with_scores = self.get_keypoints(frame_rgb)
        keypoints = keypoints_with_scores[0][0]
        is_attempt = self.check_attempt(keypoints)
        is_correct = self.check_exercise(keypoints)

        if self.previous_state is None:
            self.previous_state = is_attempt

        if self.previous_state != is_attempt:
            if is_attempt:
                # El usuario ha comenzado un nuevo intento
                self.correct_state = False
            else:
                # El usuario ha terminado un intento
                if self.correct_state:
                    self.correct_repetitions += 1
                else:
                    self.incorrect_repetitions += 1
            self.previous_state = is_attempt

        elif is_attempt:
            # Estamos en un intento, determinar si es correcto o no
            if is_correct and not self.correct_state:
                self.correct_state = True

        self.show_feedback(is_attempt)

        output_overlay = self.draw_predictions_on_image(frame, keypoints_with_scores)
        self.show_image(output_overlay)

    
    def show_image(self, image, new_height=500):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, _ = image_rgb.shape
        aspect_ratio = width / height
        new_width = int(new_height * aspect_ratio)
        resized_image_rgb = cv2.resize(image_rgb, (new_width, new_height))
        q_image = QImage(resized_image_rgb.data, new_width, new_height, 3 * new_width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap)
        self.window.show()


    def show_feedback(self,is_attempt):
        if is_attempt:
            text = "Intento"
            color = "#D35400"
            if self.correct_state:
                text = "Correcto"
                color = "#2874A6"
        else:
            text = "Reposo"
            color = "black"

        self.state_label.setText(f"Estado: {text}")
        self.state_label.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold;")

        self.correct_label.setText(f"Correctas: {self.correct_repetitions}")
        self.incorrect_label.setText(f"Incorrectas: {self.incorrect_repetitions}")

        self.correct_label.show()
        self.incorrect_label.show()


    def show_indications(self, indications):
        # Borra cualquier indicación previa
        for indication in self.indications:
            indication.hide()

        self.indications = []

        # Muestra las nuevas indicaciones
        for obj in indications:
            label = QLabel(obj["name"])
            label.setStyleSheet(f"color: {obj['color']}; font-size: 20px; font-weight: bold; ")
            self.indications_layout.addWidget(label)
            self.indications.append(label)
            label.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = ShowWindow()
    sw.show_window()
    sys.exit(app.exec_())
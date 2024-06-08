import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

import cv2
import tensorflow as tf
import numpy as np

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
    def __init__(self, model_path, video_path):
    
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

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_window)
        self.timer.start(16)

    
    def get_keypoints(self, frame, input_size=256 ):

        img = frame.copy()
        img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), input_size, input_size)
        input_image = tf.cast(img, dtype=tf.uint8)

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        self.interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
        self.interpreter.invoke()
        keypoints_with_scores = self.interpreter.get_tensor(output_details[0]['index'])
        return keypoints_with_scores
    
    def _keypoints_and_edges_for_display(self, keypoints_with_scores, height, width, keypoint_threshold=0.11):
        keypoints_all = []
        keypoint_edges_all = []
        edge_colors = []
        num_instances, _, _, _ = keypoints_with_scores.shape    
        for idx in range(num_instances):
            kpts_x = keypoints_with_scores[0, idx, :, 1]
            kpts_y = keypoints_with_scores[0, idx, :, 0]
            kpts_scores = keypoints_with_scores[0, idx, :, 2]
            kpts_absolute_xy = np.stack([width * np.array(kpts_x), height * np.array(kpts_y)], axis=-1)
            kpts_above_thresh_absolute = kpts_absolute_xy[kpts_scores > keypoint_threshold, :]
            keypoints_all.append(kpts_above_thresh_absolute)

            for edge_pair, color in EDGES.items():
                if (kpts_scores[edge_pair[0]] > keypoint_threshold and
                    kpts_scores[edge_pair[1]] > keypoint_threshold):
                    x_start = kpts_absolute_xy[edge_pair[0], 0]
                    y_start = kpts_absolute_xy[edge_pair[0], 1]
                    x_end = kpts_absolute_xy[edge_pair[1], 0]
                    y_end = kpts_absolute_xy[edge_pair[1], 1]
                    line_seg = np.array([[x_start, y_start], [x_end, y_end]])
                    keypoint_edges_all.append(line_seg)
                    edge_colors.append(color)
        if keypoints_all:
            keypoints_xy = np.concatenate(keypoints_all, axis=0)
        else:
            keypoints_xy = np.zeros((0, 17, 2))

        if keypoint_edges_all:
            edges_xy = np.stack(keypoint_edges_all, axis=0)
        else:
            edges_xy = np.zeros((0, 2, 2))
        return keypoints_xy, edges_xy, edge_colors

    def draw_predictions_on_image(self, frame, keypoints_with_scores, crop_region=None):
        height, width, _ = frame.shape

        # Obtiene los keypoints, bordes y colores según la función _keypoints_and_edges_for_display
        (keypoint_locs, keypoint_edges, edge_colors) = self._keypoints_and_edges_for_display(keypoints_with_scores, height, width)

        # Itera sobre los bordes y colores para dibujarlos en el marco
        for edge, color in zip(keypoint_edges, edge_colors):
            start_point = (int(edge[0][0]), int(edge[0][1]))
            end_point = (int(edge[1][0]), int(edge[1][1]))
            cv2.line(frame, start_point, end_point, COLOR_MAP[color], 2)  # Usa el color del diccionario

        # Dibuja los puntos clave en el marco
        for kp_loc in keypoint_locs:
            center = (int(kp_loc[0]), int(kp_loc[1]))
            cv2.circle(frame, center, 4, (0, 255, 0), -1)  # Usa el color verde para los puntos clave

        # Dibuja el rectángulo de recorte si se proporciona la región de recorte
        if crop_region is not None:
            xmin = max(crop_region['x_min'] * width, 0.0)
            ymin = max(crop_region['y_min'] * height, 0.0)
            rec_width = min(crop_region['x_max'], 0.99) * width - xmin
            rec_height = min(crop_region['y_max'], 0.99) * height - ymin
            start_point = (int(xmin), int(ymin))
            end_point = (int(xmin + rec_width), int(ymin + rec_height))
            cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 1)  # Usa el color rojo para el rectángulo

        return frame 

    def update_window(self):
        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            self.cap.release()
            return

        keypoints_with_scores = self.get_keypoints(frame)
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

        output_overlay = self.draw_predictions_on_image(frame, keypoints_with_scores)
        self.show_image(output_overlay)
    
    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, _ = image_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.video_label.setPixmap(pixmap)
        self.window.show()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = ShowWindow()
    sw.show_window()
    sys.exit(app.exec_())
import sys
import cv2
import tensorflow as tf
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

# Configurar el modelo de TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path='thunder.tflite')
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

def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, _ = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, _ in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 2)

def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, _ = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 4, (0,255,0), -1)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 500)
        MainWindow.setMinimumSize(QtCore.QSize(700, 500))
        MainWindow.setMaximumSize(QtCore.QSize(700, 500))
        MainWindow.setStyleSheet("QWidget#centralwidget{background-color: rgb(85, 170, 127);}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 70, 320, 240))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 340, 231, 41))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(232, 58, 58);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(70, 340, 231, 41))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(85, 255, 127);\n"
"\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 420, 91, 20))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("border-radius:5px;\n"
"background-color: rgb(85, 170, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 20, 341, 31))
        self.label_2.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.cancel)
        self.pushButton_2.clicked.connect(self.start_video)
        self.pushButton_3.clicked.connect(self.salir)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start_video(self):
        self.Work = Work()
        self.Work.start()
        self.Work.Imageupd.connect(self.Imageupd_slot)

    def Imageupd_slot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def cancel(self):
        self.label.clear()
        self.Work.stop()

    def salir(self):
        sys.exit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Stop"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.pushButton_3.setText(_translate("MainWindow", "Exit"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Video stream con PyQt5 y Python</p></body></html>"))

class Work(QThread):
    Imageupd = pyqtSignal(QImage)
    def run(self):
        self.hilo_corriendo = True
        cap = cv2.VideoCapture(0)
        
        while self.hilo_corriendo:
            ret, frame = cap.read()
            if ret:
                # Procesar la imagen
                img = frame.copy()
                img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256,256)
                input_image = tf.cast(img, dtype=tf.float32)

                # Configurar la entrada y salida del modelo
                input_details = interpreter.get_input_details()
                output_details = interpreter.get_output_details()

                # Realizar predicciones
                interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
                interpreter.invoke()
                keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])

                # Renderizar resultados
                draw_connections(frame, keypoints_with_scores, EDGES, 0.4)
                draw_keypoints(frame, keypoints_with_scores, 0.4)

                # Convertir imagen para mostrar en el QLabel
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                flip = cv2.flip(Image, 1)
                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format_RGB888)
                pic = convertir_QT.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
                self.Imageupd.emit(pic)
        cap.release()

    def stop(self):
        self.hilo_corriendo = False
        self.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

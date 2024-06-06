import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurar la ventana principal
        self.setWindowTitle('Grid Layout')
        self.resize(600, 400)
        
        # Crear el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout de cuadrícula
        grid_layout = QGridLayout(central_widget)
        
        # Establecer el tamaño de filas y columnas
        grid_layout.setColumnStretch(0, 1)  # Columna 0 con tamaño 1
        grid_layout.setColumnStretch(1, 2)  # Columna 1 con tamaño 2
        grid_layout.setRowStretch(0, 1)  # Fila 0 con tamaño 1
        grid_layout.setRowStretch(1, 2)  # Fila 1 con tamaño 2
        
        # Crear widgets individualmente y agregarlos al layout
        self.create_widgets(grid_layout)
        
    def create_widgets(self, layout):
        widget1 = QWidget()
        widget1.setStyleSheet('background-color: red')
        label1 = QLabel()
        widget1.addWidget(label1)
        label1.setText("hola mascota jaa")
        layout.addWidget(widget1, 0, 0)  # Agregar widget en la fila 0, columna 0
        
        widget2 = QWidget()
        widget2.setStyleSheet('background-color: yellow')
        layout.addWidget(widget2, 0, 1)  # Agregar widget en la fila 0, columna 1
        
        widget3 = QWidget()
        widget3.setStyleSheet('background-color: blue')
        layout.addWidget(widget3, 1, 0)  # Agregar widget en la fila 1, columna 0
        
        widget4 = QWidget()
        widget4.setStyleSheet('background-color: green')
        layout.addWidget(widget4, 1, 1)  # Agregar widget en la fila 1, columna 1
        
        widget5 = QWidget()
        widget5.setStyleSheet('background-color: orange')
        layout.addWidget(widget5, 2, 0)  # Agregar widget en la fila 2, columna 0
        
        widget6 = QWidget()
        widget6.setStyleSheet('background-color: purple')
        layout.addWidget(widget6, 2, 1)  # Agregar widget en la fila 2, columna 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

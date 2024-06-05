from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from views.main_window import Ui_MainWindow
from controllers.sentadilla_controller import SentadillaController
from controllers.biceps_controller import CurlBicepController
import os


class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons to their respective exercises
        self.ui.sentadilla_btn.clicked.connect(self.open_sentadilla_exercise)
        self.ui.biceps_btn.clicked.connect(self.open_sentadilla_exercise)
        # self.ui.estocada_btn.clicked.connect(self.open_estocada_exercise)

        controller_dir = os.path.dirname(os.path.abspath(__file__))
        project_root_dir = os.path.abspath(os.path.join(controller_dir, ".."))
        # img_dir = os.path.join(project_root_dir, "resources/1_sentadilla_btn.png")
        img_dir = "./resources/1_sentadilla_btn.png"
        img_dir3 = "./resources/3_biceps_btn.png"

        sentadilla_btn_stylesheet = f"""
                                    QPushButton#sentadilla_btn {{
                                        background-image: url('{img_dir}');
                                        background-repeat: no-repeat;
                                        background-position: center;
                                        border-style: outset;
                                    }}
                                    QPushButton#sentadilla_btn:hover {{
                                        border-style: inset;
                                    }}
                                    """        
        biceps_btn_stylesheet = f"""
                                    QPushButton#biceps_btn {{
                                        background-image: url('{img_dir3}');
                                        background-repeat: no-repeat;
                                        background-position: center;
                                        border-style: outset;
                                    }}
                                    QPushButton#biceps_btn:hover {{
                                        border-style: inset;
                                    }}
                                    """        
        # Change properties of sentadilla_btn
        self.ui.sentadilla_btn.setStyleSheet(sentadilla_btn_stylesheet)
        self.ui.biceps_btn.setStyleSheet(biceps_btn_stylesheet)
        
    def open_sentadilla_exercise(self):
        self.sentadilla_window = SentadillaController()
        self.sentadilla_window.show()
    
    def open_biceps_exercise(self):
        self.biceps_window = CurlBicepController()
        self.biceps_window.show()
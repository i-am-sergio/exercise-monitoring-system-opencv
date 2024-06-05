from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from views.main_window import Ui_MainWindow
from controllers.sentadilla_controller import SentadillaController
from controllers.estocada_controller import EstocadaController
import os


class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons to their respective exercises
        self.ui.sentadilla_btn.clicked.connect(self.open_sentadilla_exercise)
        controller_dir = os.path.dirname(os.path.abspath(__file__))
        project_root_dir = os.path.abspath(os.path.join(controller_dir, ".."))
        sentadilla_img_dir = os.path.join(project_root_dir, "resources/1_sentadilla_btn.png")
        #sentadilla_img_dir = "./resources/1_sentadilla_btn.png"
        sentadilla_btn_stylesheet = f"""
                                    QPushButton#sentadilla_btn {{
                                        background-image: url('{sentadilla_img_dir}');
                                        background-repeat: no-repeat;
                                        background-position: center;
                                        border-style: outset;
                                    }}
                                    QPushButton#sentadilla_btn:hover {{
                                        border-style: inset;
                                    }}
                                    """
        # Change properties of sentadilla_btn
        self.ui.sentadilla_btn.setStyleSheet(sentadilla_btn_stylesheet)
        
        self.ui.estocada_btn.clicked.connect(self.open_estocada_exercise)
        estocada_img_dir = os.path.join(project_root_dir, "resources/2_lunge_btn.png")
        #estocada_img_dir = "./resources/2_lunge_btn.png"
        estocada_btn_stylesheet = f"""
                                    QPushButton#estocada_btn {{
                                        background-image: url('{estocada_img_dir}');
                                        background-repeat: no-repeat;
                                        background-position: center;
                                        border-style: outset;
                                    }}
                                    QPushButton#estocada_btn:hover {{
                                        border-style: inset;
                                    }}
                                    """
        # Change properties of estocada_btn
        self.ui.estocada_btn.setStyleSheet(estocada_btn_stylesheet)
        
    def open_sentadilla_exercise(self):
        self.sentadilla_window = SentadillaController()
        self.sentadilla_window.show()
        
    def open_estocada_exercise(self):
        self.estocada_window = EstocadaController()
        self.estocada_window.show()
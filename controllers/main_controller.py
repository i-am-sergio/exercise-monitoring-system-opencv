from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from views.main_window import Ui_MainWindow
from controllers.sentadilla_controller import SentadillaController
from controllers.estocada_controller import EstocadaController
from controllers.biceps_controller import CurlBicepController
from controllers.abdominal_controller import AbdominalController 
from controllers.plancha_controller import PlanchaController
import os

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Set stylesheets
        self.set_button_styles()

        # Connect buttons to their respective exercises
        self.ui.sentadilla_btn.clicked.connect(self.open_sentadilla_exercise)
        self.ui.biceps_btn.clicked.connect(self.open_biceps_exercise)
        self.ui.estocada_btn.clicked.connect(self.open_estocada_exercise)
        self.ui.abdominal_btn.clicked.connect(self.open_abdominal_exercise)
        self.ui.plancha_btn.clicked.connect(self.open_plancha_exercise)
        # self.ui.estocada_btn.clicked.connect(self.open_estocada_exercise)

    def set_button_styles(self):
        controller_dir = os.path.dirname(os.path.abspath(__file__))
        project_root_dir = os.path.abspath(os.path.join(controller_dir, ".."))
        
        # img_dir1 = os.path.join(project_root_dir, "resources/1_sentadilla_btn.png")
        # img_dir2 = os.path.join(project_root_dir, "resources/2_lunge_btn.png")
        # img_dir3 = os.path.join(project_root_dir, "resources/3_biceps_btn.png")
        img_dir2 = "./resources/2_lunge_btn.png"
        img_dir1 = "./resources/1_sentadilla_btn.png"
        img_dir3 = "./resources/3_biceps_btn.png"
        img_abs_dir = "./resources/6_abdominal_btn.png"
        img_flexion_dir = "./resources/5_flexion_btn.png"

        sentadilla_btn_stylesheet = f"""
        QPushButton#sentadilla_btn {{
            background-image: url('{img_dir1}');
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
        
        estocada_btn_stylesheet = f"""
        QPushButton#estocada_btn {{
            background-image: url('{img_dir2}');
            background-repeat: no-repeat;
            background-position: center;
            border-style: outset;
        }}
        QPushButton#estocada_btn:hover {{
            border-style: inset;
        }}
        """
        
        abdominal_btn_stylesheet = f"""
                            QPushButton#abdominal_btn {{
                                background-image: url('{img_abs_dir}');
                                background-repeat: no-repeat;
                                background-position: center;
                                border-style: outset;
                            }}
                            QPushButton#abdominal_btn:hover {{
                                border-style: inset;
                            }}
                            """  
    
        plancha_btn_stylesheet = f"""
                            QPushButton#plancha_btn {{
                                background-image: url('{img_flexion_dir}');
                                background-repeat: no-repeat;
                                background-position: center;
                                border-style: outset;
                            }}
                            QPushButton#abdominal_btn:hover {{
                                border-style: inset;
                            }}
                            """  

        self.ui.sentadilla_btn.setStyleSheet(sentadilla_btn_stylesheet)
        self.ui.biceps_btn.setStyleSheet(biceps_btn_stylesheet)
        self.ui.estocada_btn.setStyleSheet(estocada_btn_stylesheet)
        self.ui.abdominal_btn.setStyleSheet(abdominal_btn_stylesheet)
        self.ui.plancha_btn.setStyleSheet(plancha_btn_stylesheet)
    def open_sentadilla_exercise(self):
        self.sentadilla_window = SentadillaController()
        self.sentadilla_window.show()

    def open_estocada_exercise(self):
        self.estocada_window = EstocadaController()
        self.estocada_window.show()

    def open_biceps_exercise(self):
        self.biceps_window = CurlBicepController()
        self.biceps_window.show()
    
    def open_abdominal_exercise(self):
        self.abdominal_window = AbdominalController()
        self.abdominal_window.show()

    def open_plancha_exercise(self):
        self.plancha_window = PlanchaController()
        self.plancha_window.show()
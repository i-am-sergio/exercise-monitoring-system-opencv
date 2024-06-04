from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from views.main_window import Ui_MainWindow
from controllers.sentadilla_controller import SentadillaController
import os


class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.sentadilla_btn.clicked.connect(self.open_sentadilla_exercise)

        controller_dir = os.path.dirname(os.path.abspath(__file__))
        project_root_dir = os.path.abspath(os.path.join(controller_dir, ".."))
        img_dir = os.path.join(project_root_dir, "resources/1_sentadilla_btn.png")

        sentadilla_btn_stylesheet = f"""
                                    QPushButton#sentadilla_btn {{
                                        background-image: url('{img_dir}');
                                        background-repeat: no-repeat;
                                        background-position: center;
                                        border-style: outset;
                                    }}
                                    QPushButton#sentadilla_btn:hover {{
                                        cursor: pointer;
                                    }}
                                    """        
        # Change properties of sentadilla_btn
        self.ui.sentadilla_btn.setStyleSheet(sentadilla_btn_stylesheet)
        
    def open_sentadilla_exercise(self):
        self.sentadilla_window = SentadillaController()
        self.sentadilla_window.show()
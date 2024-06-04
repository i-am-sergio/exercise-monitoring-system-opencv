from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets
from views.sentadilla_window import Ui_SentadillaWindow

class SentadillaController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SentadillaWindow()
        self.ui.setupUi(self)
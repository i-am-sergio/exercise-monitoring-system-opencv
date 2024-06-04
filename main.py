import sys
from PyQt5 import QtWidgets

from controllers.main_controller import MainController

# from views.main_window import Ui_MainWindow
# from views.exercise_window import Ui_ExerciseWindow

# class MainApp(QtWidgets.QMainWindow):
    # def __init__(self):
    #     super().__init__()
    #     self.ui = Ui_MainWindow()
    #     self.ui.setupUi(self)
    #     # self.ui.start_button.clicked.connect(self.open_exercise_window)

    # def open_exercise_window(self):
    #     self.exercise_window = QtWidgets.QMainWindow()
    #     self.exercise_ui = Ui_ExerciseWindow()
    #     self.exercise_ui.setupUi(self.exercise_window)
    #     self.exercise_window.show()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainController()
    main_app.show()
    sys.exit(app.exec_())

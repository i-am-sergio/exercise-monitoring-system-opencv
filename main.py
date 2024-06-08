import sys
from PyQt5 import QtWidgets

from controllers.main_controller import MainController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainController()
    main_app.show()
    sys.exit(app.exec_())
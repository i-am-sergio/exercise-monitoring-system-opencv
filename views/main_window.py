from PyQt5 import QtCore, QtGui, QtWidgets

BUTTON_STYLE = (
    "QPushButton {"
    "    background-color: #787878;"
    "    border-style: outset;"
    "    border-width: 0;"
    "    border-radius: 10px;"
    "    border-color: beige;"
    "    font: bold 20px;"
    "    color: #A0F97A;"
    "    padding: 6px;"
    "}"
    ""
    "QPushButton:pressed {"
    "    border-style: inset;"
    "}"
    ""
)

class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.setWindowModality(QtCore.Qt.NonModal)
        main_window.resize(1200, 700)
        main_window.setMinimumSize(QtCore.QSize(1200, 700))
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setStyleSheet("background: #242424;")
        self.centralwidget.setObjectName("centralwidget")
        self.vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vertical_layout.setObjectName("vertical_layout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.widget_izq = QtWidgets.QWidget(self.widget)
        self.widget_izq.setMinimumSize(QtCore.QSize(800, 0))
        self.widget_izq.setObjectName("widget_izq")
        self.grid_layout = QtWidgets.QGridLayout(self.widget_izq)
        self.grid_layout.setObjectName("grid_layout")
        
        self.sentadilla_btn = QtWidgets.QPushButton(self.widget_izq)
        self.sentadilla_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.sentadilla_btn.setMaximumSize(QtCore.QSize(350, 210))
        font = QtGui.QFont()
        font.setFamily("URW Bookman [urw]")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.sentadilla_btn.setFont(font)
        self.sentadilla_btn.setStyleSheet(BUTTON_STYLE)
        self.sentadilla_btn.setText("")
        self.sentadilla_btn.setObjectName("sentadilla_btn")        
        self.grid_layout.addWidget(self.sentadilla_btn, 0, 0, 1, 1)
        
        self.estocada_btn = QtWidgets.QPushButton(self.widget_izq)
        self.estocada_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.estocada_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.estocada_btn.setStyleSheet(BUTTON_STYLE)
        self.estocada_btn.setText("")
        self.estocada_btn.setObjectName("estocada_btn")
        self.grid_layout.addWidget(self.estocada_btn, 0, 1, 1, 1)
        
        
        self.abdominal_btn = QtWidgets.QPushButton(self.widget_izq)
        self.abdominal_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.abdominal_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.abdominal_btn.setStyleSheet(BUTTON_STYLE)
        self.abdominal_btn.setText("")
        self.abdominal_btn.setObjectName("abdominal_btn")
        self.grid_layout.addWidget(self.abdominal_btn, 1, 1, 1, 1)
        
        self.jumps_btn = QtWidgets.QPushButton(self.widget_izq)
        self.jumps_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.jumps_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.jumps_btn.setStyleSheet(BUTTON_STYLE)
        self.jumps_btn.setText("")
        self.jumps_btn.setObjectName("jumps_btn")
        self.grid_layout.addWidget(self.jumps_btn, 3, 0, 1, 1)
        
        self.plancha_btn = QtWidgets.QPushButton(self.widget_izq)
        self.plancha_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.plancha_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.plancha_btn.setStyleSheet(BUTTON_STYLE)
        self.plancha_btn.setText("")
        self.plancha_btn.setObjectName("plancha_btn")
        self.grid_layout.addWidget(self.plancha_btn, 3, 1, 1, 1)
        
        self.biceps_btn = QtWidgets.QPushButton(self.widget_izq)
        self.biceps_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.biceps_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.biceps_btn.setStyleSheet(BUTTON_STYLE)
        self.biceps_btn.setText("")
        self.biceps_btn.setObjectName("biceps_btn")
        self.grid_layout.addWidget(self.biceps_btn, 1, 0, 1, 1)
        
        self.horizontal_layout.addWidget(self.widget_izq)
        self.widget_der = QtWidgets.QWidget(self.widget)
        self.widget_der.setMaximumSize(QtCore.QSize(8777217, 16777215))
        self.widget_der.setObjectName("widget_der")
        self.label = QtWidgets.QLabel(self.widget_der)
        self.label.setGeometry(QtCore.QRect(70, 240, 231, 191))
        font = QtGui.QFont()
        font.setFamily("URW Bookman [urw]")
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel {"
                "    background-color: transparent;"
                "    border: none;"
                "    border-radius: 10px;"
                "    font: bold 30px;"
                "    color: #90CDF4;"
                "    padding: 6px;"
                "    text-align: center;"
                "    qproperty-alignment: AlignCenter;"
                "}"
                "")
        self.label.setObjectName("label")
        self.horizontal_layout.addWidget(self.widget_der)
        self.vertical_layout.addWidget(self.widget)
        main_window.setCentralWidget(self.centralwidget)
        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "EXERCISE\n"
                "MONITORING\n"
                "SYSTEM"))
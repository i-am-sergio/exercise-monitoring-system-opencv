# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1200, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background: #242424;")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_izq = QtWidgets.QWidget(self.widget)
        self.widget_izq.setMinimumSize(QtCore.QSize(800, 0))
        self.widget_izq.setObjectName("widget_izq")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_izq)
        self.gridLayout.setObjectName("gridLayout")
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
        self.sentadilla_btn.setStyleSheet("QPushButton {\n"
"    background-image: url(:/images/1_sentadilla_btn.png);\n"
"    /*background-color: rgb(28,19,42);*/\n"
"    background-color: #787878;\n"
"    border-style: outset;\n"
"    border-width: 0;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 20px;\n"
"    color: #A0F97A;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /*background-color: rgb(30,23,46);*/\n"
"    border-style: inset;\n"
"}\n"
"QPushButton:hover {\n"
"    cursor: pointer;\n"
"    /*background-color: #3F325C;*/\n"
"}")
        self.sentadilla_btn.setText("")
        self.sentadilla_btn.setObjectName("sentadilla_btn")
        self.gridLayout.addWidget(self.sentadilla_btn, 0, 0, 1, 1)
        self.estocada_btn = QtWidgets.QPushButton(self.widget_izq)
        self.estocada_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.estocada_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.estocada_btn.setStyleSheet("QPushButton {\n"
"    /*background-color: rgb(28,19,42);*/\n"
"    background-color: #787878;\n"
"    border-style: outset;\n"
"    border-width: 0;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 20px;\n"
"    color: #A0F97A;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /*background-color: rgb(30,23,46);*/\n"
"    border-style: inset;\n"
"}\n"
"QPushButton:hover {\n"
"    /*background-color: #3F325C;*/\n"
"}")
        self.estocada_btn.setText("")
        self.estocada_btn.setObjectName("estocada_btn")
        self.gridLayout.addWidget(self.estocada_btn, 0, 1, 1, 1)
        self.puente_btn = QtWidgets.QPushButton(self.widget_izq)
        self.puente_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.puente_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.puente_btn.setStyleSheet("QPushButton {\n"
"    /*background-color: rgb(28,19,42);*/\n"
"    background-color: #787878;\n"
"    border-style: outset;\n"
"    border-width: 0;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 20px;\n"
"    color: #A0F97A;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /*background-color: rgb(30,23,46);*/\n"
"    border-style: inset;\n"
"}\n"
"QPushButton:hover {\n"
"    /*background-color: #3F325C;*/\n"
"}")
        self.puente_btn.setText("")
        self.puente_btn.setObjectName("puente_btn")
        self.gridLayout.addWidget(self.puente_btn, 1, 1, 1, 1)
        self.elevaciones_btn = QtWidgets.QPushButton(self.widget_izq)
        self.elevaciones_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.elevaciones_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.elevaciones_btn.setStyleSheet("QPushButton {\n"
"    /*background-color: rgb(28,19,42);*/\n"
"    background-color: #787878;\n"
"    border-style: outset;\n"
"    border-width: 0;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 20px;\n"
"    color: #A0F97A;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /*background-color: rgb(30,23,46);*/\n"
"    border-style: inset;\n"
"}\n"
"QPushButton:hover {\n"
"    /*background-color: #3F325C;*/\n"
"}")
        self.elevaciones_btn.setText("")
        self.elevaciones_btn.setObjectName("elevaciones_btn")
        self.gridLayout.addWidget(self.elevaciones_btn, 3, 0, 1, 1)
        self.plancha_btn = QtWidgets.QPushButton(self.widget_izq)
        self.plancha_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.plancha_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.plancha_btn.setStyleSheet("QPushButton {\n"
"    /*background-color: rgb(28,19,42);*/\n"
"    background-color: #787878;\n"
"    border-style: outset;\n"
"    border-width: 0;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 20px;\n"
"    color: #A0F97A;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /*background-color: rgb(30,23,46);*/\n"
"    border-style: inset;\n"
"}\n"
"QPushButton:hover {\n"
"    /*background-color: #3F325C;*/\n"
"}")
        self.plancha_btn.setText("")
        self.plancha_btn.setObjectName("plancha_btn")
        self.gridLayout.addWidget(self.plancha_btn, 3, 1, 1, 1)
        self.biceps_btn = QtWidgets.QPushButton(self.widget_izq)
        self.biceps_btn.setMinimumSize(QtCore.QSize(350, 210))
        self.biceps_btn.setMaximumSize(QtCore.QSize(350, 210))
        self.biceps_btn.setStyleSheet("QPushButton {\n"
"    /*background-color: rgb(28,19,42);*/\n"
"    background-color: #787878;\n"
"    border-style: outset;\n"
"    border-width: 0;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 20px;\n"
"    color: #A0F97A;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /*background-color: rgb(30,23,46);*/\n"
"    border-style: inset;\n"
"}\n"
"QPushButton:hover {\n"
"    /*background-color: #3F325C;*/\n"
"}")
        self.biceps_btn.setText("")
        self.biceps_btn.setObjectName("biceps_btn")
        self.gridLayout.addWidget(self.biceps_btn, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget_izq)
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
        self.label.setStyleSheet("QLabel {\n"
"    background-color: transparent;\n"
"    border: 0;  /* Puedes usar border: none; también */\n"
"    border-radius: 10px;\n"
"    /*font-family: \"Courier New\";\n"
"    font-size: 30px;\n"
"    font-weight: bold;*/\n"
"    font: bold 30px;\n"
"    color: #90CDF4;\n"
"    padding: 6px;\n"
"    text-align: center;  /* Centra el texto horizontalmente */\n"
"    qproperty-alignment: AlignCenter; \n"
"}\n"
"")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.widget_der)
        self.verticalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "EXERCISE\n"
"MONITORING\n"
"SYSTEM"))

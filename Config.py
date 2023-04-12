# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Config.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_config(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 550)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(40, 70, 370, 480))
        self.widget.setStyleSheet("QPushButton#Login_button:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"QPushButton#Login_button:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgb(9, 121, 226), stop:1 rgb(105, 118, 132));\n"
"}\n"
"QPushButton#Login_button{\n"
"\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:15px;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"QPushButton#Close_button{\n"
"\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:8px;\n"
"}\n"
"QPushButton#Close_button:pressed{\n"
"padding-left:1px;\n"
"padding-top:1px;\n"
"background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 30, 300, 420))
        self.label.setStyleSheet("background-image: url(images/images/BG-9.jpg);\n"
"border-radius:20px")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(80, 90, 231, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily(u"Segoe UI Semibold")
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 165, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily(u"Segoe UI Semibold")
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:None;\n"
"border-bottom:2px solid rgb(0,0,0);\n"
"\n"
"padding-bottom:7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 230, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:None;\n"
"border-bottom:2px solid rgb(0,0,0);;\n"
"\n"
"padding-bottom:7px;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 300, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:None;\n"
"border-bottom:2px solid rgb(0,0,0);;\n"
"\n"
"padding-bottom:7px;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.Login_button = QtWidgets.QPushButton(self.widget)
        self.Login_button.setGeometry(QtCore.QRect(80, 390, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily(u"Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.Login_button.setFont(font)
        self.Login_button.setStyleSheet("")
        self.Login_button.setObjectName("Login_button")
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setGeometry(QtCore.QRect(80, 350, 181, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.Close_button = QtWidgets.QPushButton(self.widget)
        self.Close_button.setGeometry(QtCore.QRect(290, 50, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Close_button.setFont(font)
        self.Close_button.setStyleSheet("")
        self.Close_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/cerca.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close_button.setIcon(icon)
        self.Close_button.setObjectName("Close_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Registro usuario"))
        self.lineEdit.setPlaceholderText(_translate("Form", "User Name"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Password"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "Confirme Password"))
        self.Login_button.setText(_translate("Form", "Guardar"))
        self.checkBox.setText(_translate("Form", "Ver Password"))
if __name__ == "__main__":    
    app=QtWidgets.QApplication(sys.argv)
    Form=QtWidgets.QWidget()
    ui=Ui_config()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

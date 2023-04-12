# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login_Final.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 550)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        Form.setStyleSheet("QPushButton#pushButton{qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));\n"
"color:rgba:(255,255,255,210);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"\n"
"QPushButton#pushButton:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(105, 118, 132, 200);\n"
"}")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 30, 370, 480))
        self.widget.setStyleSheet("QPushButton#Login_button:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"QPushButton#Login_button:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#Login_button{\n"
"\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:15px;\n"
"}\n"
"\n"
"QPushButton#Config_button:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"QPushButton#Config_button:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton#Config_button{\n"
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
"\n"
"\n"
"")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 30, 300, 420))
        self.label.setStyleSheet("border-image: url(images/images/fondo.jpg);\n"
"border-radius: 20px;\n"
"")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 300, 420))
        self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:0.715909, stop:0 rgba(0, 0, 0, 9), stop:0.375 rgba(0, 0, 0, 50),stop:0.835227 rgba(0,0,0,75));\n"
"border-radius: 20px;\n"
"")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(135, 95, 90, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setFamily(u"Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 165, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:None;\n"
"border-bottom:2px solid rgba(105,118,132,255);\n"
"\n"
"padding-bottom:7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 230, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:None;\n"
"border-bottom:2px solid rgba(105,118,132,255);\n"
"\n"
"padding-bottom:7px;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.Login_button = QtWidgets.QPushButton(self.widget)
        self.Login_button.setGeometry(QtCore.QRect(80, 310, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily(u"Segoe UI Semibold")
        self.Login_button.setFont(font)
        self.Login_button.setStyleSheet("")
        self.Login_button.setObjectName("Login_button")
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setGeometry(QtCore.QRect(90, 280, 181, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.Config_button = QtWidgets.QPushButton(self.widget)
        self.Config_button.setGeometry(QtCore.QRect(80, 360, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily(u"Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.Config_button.setFont(font)
        self.Config_button.setStyleSheet("QPushButton2#pushButton:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"QPushButton2#pushButton:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));\n"
"}\n"
"QPushButton2#pushButton{\n"
"\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:15px;\n"
"}")
        self.Config_button.setObjectName("Config_button")
        self.Close_button = QtWidgets.QPushButton(self.widget)
        self.Close_button.setGeometry(QtCore.QRect(290, 50, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily(u"Segoe UI Semibold")
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
        self.label_4.setText(_translate("Form", "Log In"))
        self.lineEdit.setPlaceholderText(_translate("Form", "User Name"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Password"))
        self.Login_button.setText(_translate("Form", "Log  In"))
        self.checkBox.setText(_translate("Form", "Ver Password"))
        self.Config_button.setText(_translate("Form", "Registrarse"))
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    Form=QtWidgets.QWidget()
    ui=Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
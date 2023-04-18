# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Advertencia.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
import Upload_Files
import threading
from dotenv import set_key,dotenv_values
env=dotenv_values(".env")
ROOT_DIR="C:\\Users\IC0167A\Desktop\Proyecto_final\prueba_s"#!CONFIGURAR PATH DEL PC DE DONDE SE VAN A SUBIR LOS ARCHIVOS, UNA VEZ TERMINADO LOS DISEÑOS
SHAREPOINT_FOLDER__NAME=env["sharepoint_name_folder"]
FILE_NAME_PATTERN='PRUEBA_4'#!CONFIGURAR ARCHIVO QUE SE VA A SUBIR, UNA VEZ TERMINADO LOS DISEÑOS
#FILE_NAME_PATTERN=None
class Ui_ADVERTENCIA(QDialog):

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.window()

    def window(self):
        self.setObjectName("ADVERTENCIA")
        self.setWindowTitle("ADVERTENCIA")
        self.resize(374, 138)
        self.setStyleSheet("background-color:#cbcbcb;")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText("SI")
        self.pushButton.setGeometry(QtCore.QRect(80, 90, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.upload_file)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setText("NO")
        self.pushButton_2.setGeometry(QtCore.QRect(220, 90, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.no)
        self.label = QtWidgets.QLabel(self)
        self.label.setText( "¿ Esta seguro que quiere subir este diseño ?")
        self.label.setGeometry(QtCore.QRect(80, 50, 261, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 41, 41))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("images/advertencia.png"))
        self.label_2.setObjectName("label_2")

        QtCore.QMetaObject.connectSlotsByName(self)

    def upload_file(self):
        upload_Thread=threading.Thread(target=Upload_Files.upload_files(ROOT_DIR,FILE_NAME_PATTERN))
        upload_Thread.start()
        self.close()
    def no(self):
        print(FILE_NAME_PATTERN)  
        self.close()
         
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_ADVERTENCIA()
    ui.show()
    sys.exit(app.exec_())

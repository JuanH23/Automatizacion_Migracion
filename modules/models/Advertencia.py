
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
import modules.models.Upload_Files
import threading
from dotenv import set_key,dotenv_values
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
env=dotenv_values(".env")
SHAREPOINT_FOLDER__NAME=env["sharepoint_name_folder"]
#FILE_NAME_PATTERN='PRUEBA_4'
FILE_NAME_PATTERN=None

class SignalHandler(QObject):
    upload_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

class Ui_ADVERTENCIA(QDialog):

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.window()

    def window(self):
        """
        Esta función crea una ventana con un mensaje de advertencia y dos botones para que el usuario elija
        si desea cargar un archivo o no.
        """
        self.setObjectName("ADVERTENCIA")
        self.setWindowTitle("ADVERTENCIA")
        self.resize(380, 140)
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
        self.label.setText( "¿ Esta seguro que quiere subir estos diseños ?")
        self.label.setGeometry(QtCore.QRect(80, 50, 265, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(30, 40, 41, 41))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("modules/images/advertencia.png"))
        self.label_2.setObjectName("label_2")

        QtCore.QMetaObject.connectSlotsByName(self)
        self.signal_handler = SignalHandler()
        self.signal_handler.upload_finished.connect(self.finish)

    def show_finish(self):
        QTimer.singleShot(0, self.finish) 
    def finish(self):
        QMessageBox.information(self, "Proceso finalizado", "Se han subido los archivos, por favor revise que se hayan subido todos correctamente.")

    def upload_file(self):

        ROOT_DIR=env["path_list_download"]+ "/Diseños_NODOS"
        upload_Thread=threading.Thread(target=modules.models.Upload_Files.upload_files(ROOT_DIR,FILE_NAME_PATTERN))
        upload_Thread.start()
        upload_Thread.join()
        self.signal_handler.upload_finished.emit()
        self.close()

    def no(self):
        print(FILE_NAME_PATTERN)  
        print(env["path_list_download"]+ "/Diseños_NODOS")
        self.close()
         
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_ADVERTENCIA()
    ui.show()
    sys.exit(app.exec_())

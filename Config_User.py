
from PyQt5.QtWidgets import (QDialog,QLabel,QPushButton,QLineEdit,QMessageBox,)
from PyQt5.QtGui import QFont
from dotenv import set_key,dotenv_values
from Config import*
class ConfigUsuarioView(QDialog):
    

    def __init__(self):
        super().__init__()
        self.ui=Ui_config()
        self.ui.setupUi(self)
        self.setModal(False)
        self.generar_formulario()

    def generar_formulario(self):

        self.ui.lineEdit_2.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.ui.lineEdit_3.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.ui.checkBox.toggled.connect(self.mostrar_pass)

        self.ui.Login_button.clicked.connect(self.configurar_usuario)
        self.ui.Close_button.clicked.connect(self.cancelar)

    def mostrar_pass(self,clicked):
                  if clicked:
                    self.ui.lineEdit_2.setEchoMode(
                        QLineEdit.EchoMode.Normal
                    )
                    self.ui.lineEdit_3.setEchoMode(
                        QLineEdit.EchoMode.Normal
                    )                    
                  else:
                        self.ui.lineEdit_2.setEchoMode(
                        QLineEdit.EchoMode.Password
                    )
                        self.ui.lineEdit_3.setEchoMode(
                        QLineEdit.EchoMode.Password
                    )                             
    def cancelar(self):
        self.close()
    
    def configurar_usuario(self):
        user_path='usuarios.txt'
        usuario=self.ui.lineEdit.text()
        password1=self.ui.lineEdit_2.text()
        password2=self.ui.lineEdit_3.text()
    

        if password1 == '' or password2 == '' or usuario=='':
            QMessageBox.warning(self,'Error','Por favor ingrese datos validos',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)
        elif password1 != password2:
            QMessageBox.warning(self,'Error','Passwords diferentes',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)   
        else:
             try:
                with open (user_path,"a+") as f:
                    f.write(f"{usuario},{password1}\n")
                    QMessageBox.information(self,'Configuración exitosa','El usuario se configuro correctamente',
                                            QMessageBox.StandardButton.Ok,
                                            QMessageBox.StandardButton.Ok)
             except FileNotFoundError as e:
                                QMessageBox.warning(self,'Error',f'La base de datos no existe {e}',
                                QMessageBox.StandardButton.Close,
                                QMessageBox.StandardButton.Close)   



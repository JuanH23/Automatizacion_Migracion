
from PyQt5.QtWidgets import (QDialog,QLabel,QPushButton,QLineEdit,QMessageBox,)
from PyQt5.QtGui import QFont
from dotenv import set_key,dotenv_values
import Barra_descaga_list
class ConfigUsuarioView(QDialog):
    

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.generar_formulario()

    def generar_formulario(self):
        self.setGeometry(100,100,350,280)
        self.setWindowTitle("Configuración Usuario")

        self.user_label=QLabel(self)
        self.user_label.setText("Usuario:")
        self.user_label.setFont(QFont('Arial',10))
        self.user_label.move(20,44)

        self.user_input=QLineEdit(self)
        self.user_input.resize(250,24)
        self.user_input.move(90,40)

        password_1_label=QLabel(self)
        password_1_label.setText("Password:")
        password_1_label.setFont(QFont('Arial',10))
        password_1_label.move(20,74)

        self.password_1_input=QLineEdit(self)
        self.password_1_input.resize(250,24)
        self.password_1_input.move(90,70)
        self.password_1_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        password_2_label=QLabel(self)
        password_2_label.setText("Password:")
        password_2_label.setFont(QFont('Arial',10))
        password_2_label.move(20,104)

        self.password_2_input=QLineEdit(self)
        self.password_2_input.resize(250,24)
        self.password_2_input.move(90,100)
        self.password_2_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.url_site=QLabel(self)
        self.url_site.setText("Url:")
        self.url_site.setFont(QFont('Arial',10))
        self.url_site.move(20,134)

        self.site_exam=QLabel(self)
        self.site_exam.setText("URL:https://claromovilco.sharepoint.com/sites/sitename/")
        self.site_exam.setFont(QFont('Arial',10))
        self.site_exam.move(20,170)

        self.url_site=QLineEdit(self)
        self.url_site.resize(250,24)
        self.url_site.move(90,130)

        self.name_site=QLabel(self)
        self.name_site.setText("Name site:")
        self.name_site.setFont(QFont('Arial',10))
        self.name_site.move(20,204)

        self.name_site=QLineEdit(self)
        self.name_site.resize(250,24)
        self.name_site.move(90,200)

        


        create_button=QPushButton(self)
        create_button.setText("Guardar Parametros")
        create_button.resize(150,25)
        create_button.move(20,240)
        create_button.clicked.connect(self.configurar_usuario)

        cancel_button=QPushButton(self)
        cancel_button.setText("Cancelar")
        cancel_button.resize(150,25)
        cancel_button.move(185,240)
        create_button.clicked.connect(self.cancelar)


    def cancelar(self):
        self.close()
    
    def configurar_usuario(self):#!Guardar estos parametros en el archivo.env
        user_path='usuarios.txt'
        usuario=self.user_input.text()
        password1=self.password_1_input.text()
        password2=self.password_2_input.text()
        url=self.url_site.text()
        site=self.name_site.text()
        env=dotenv_values(".env")
        set_key(".env","sharepoint_url_site",url)#input("Digite correo==>") cambiar por la variable del qt            USERNAME=env["sharepoint_email"]
        set_key(".env","sharepoint_site_name",site)#
        

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



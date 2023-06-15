from PyQt5.QtWidgets import (QApplication,QWidget,QLineEdit,QMessageBox)
from modules.models.main import MiApp
from modules.statics.Login_Final import*
from modules.models.search_files import*
from modules.models.Config_User import ConfigUsuarioView
from dotenv import set_key,dotenv_values
from dotenv import load_dotenv
import sys
load_dotenv()
class Login(QWidget):
        def __init__(self):
            super().__init__()
            self.ui=Ui_Form()
            self.ui.setupUi(self)
            self.ui.Login_button.clicked.connect(self.login) 
            self.ui.Config_button.clicked.connect(self.config_usuario)#*Button Config
            self.ui.Close_button.clicked.connect(self.control_close)          
            self.is_loged=False     
            self.ui.lineEdit_2.setEchoMode(     #Label de usuario
                  QLineEdit.EchoMode.Password
             )
            
            self.ui.checkBox.toggled.connect(self.mostrar_pass)     #Checkbox para poder visualizar o no, la contraseña

        def control_close(self):#*Función para cerrar el programa
            self.close()

        def mostrar_pass(self,clicked):
                  if clicked :
                    self.ui.lineEdit_2.setEchoMode(
                        QLineEdit.EchoMode.Normal
                    )           
                  else:
                        self.ui.lineEdit_2.setEchoMode(
                        QLineEdit.EchoMode.Password
                    )          
                  
        def login(self):
                  #users: es una lista en la cual se va a aplicar la funcion .append para 
                  # agregar los registros que se hagan
                  #username:guarda los valores del LineEdit para guardarlos en el .env 
                  # y ademas de revisar si el texto digitado esta en el archivo de texto
                  #password:guarda los valores del LineEdit para guardarlos en el .env 
                  # y ademas de revisar si el texto digitado esta en el archivo de texto
                  users=[]
                  user_path='config/.env.users'

                  try:
                    with open(user_path,'r') as f:
                          for linea in f:
                            users.append(linea.strip("\n"))
                    login_information=f"{self.ui.lineEdit.text()},{self.ui.lineEdit_2.text()}"
                    Username=self.ui.lineEdit.text()
                    Password=self.ui.lineEdit_2.text()
                    print(f'Correo==>{Username}')
                    print(f'Pass==>{Password}')
                    env=dotenv_values(".env")
                    set_key(".env","sharepoint_email",Username)#input("Digite correo==>") cambiar por la variable del qt
                    USERNAME=env["sharepoint_email"]
                    set_key(".env","sharepoint_password",Password)#
                    PASSWORD=env["sharepoint_password"]
                    if login_information in users:
                         QMessageBox.information(self,"Inicio sesion",
                         "Inicio sesion exitoso",
                         QMessageBox.StandardButton.Ok,
                         QMessageBox.StandardButton.Ok)
                         self.is_loged=True
                         self.close()
                         self.open_main()
                    else:
                         QMessageBox.warning(self,"Error Message",
                         "Credenciales incorrectas",
                         QMessageBox.StandardButton.Close,
                         QMessageBox.StandardButton.Close)
                  except FileNotFoundError as e: 
                         QMessageBox.warning(self,"Error Message",
                         f"Base de datos de usuario no encontrada: {e}",
                         QMessageBox.StandardButton.Close,
                         QMessageBox.StandardButton.Close)
                  except Exception as u:
                          QMessageBox.warning(self, "Error Message",
                         f'Error en el servidor: {u}',
                         QMessageBox.StandardButton.Close,
                         QMessageBox.StandardButton.Close)
        def open_main(self):
              self.main= MiApp()
              self.main.show()
        def config_usuario(self):
            self.configu_user=ConfigUsuarioView()
            self.configu_user.show()
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Log= Login()
    Log.show()
    sys.exit(app.exec_())

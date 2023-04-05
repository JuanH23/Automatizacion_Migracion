import sys
from estructura_principal import*
from PyQt5.QtWidgets import QTableWidgetItem,QFileDialog,QMessageBox
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import download_lists
import threading
from office365_api import SharePoint
import download_lists
from Advertencia import*

##########################################################################################################
#*Librerias utilizadas en la función de subir lista a SharePoint
from office365.sharepoint.lists.template_type import ListTemplateType
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files import file
from office365.sharepoint.files.file import File
from office365.sharepoint.lists.creation_information import ListCreationInformation
from office365.runtime.auth.user_credential import UserCredential 
from office365.sharepoint.lists.list import List   
from office365.sharepoint.listitems.collection import ListItemCollection
from office365.runtime.client_request_exception import ClientRequestException 
import time
import ssl
import requests
import json
from dotenv import set_key,dotenv_values
###########################################################################################################
#*Variables de entorno para las funciones con SharePoint
env=dotenv_values(".env")
username = env["sharepoint_email"]
password = env["sharepoint_password"]
url = env['sharepoint_url_site']
ruth_list_download= env["path_list_download"]

EXPORT_TYPE='Excel'

##############################################################################################################




class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.gripSize=10
        self.grip=QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize,self.gripSize)
        self.ui.frame_Sup.mouseMoveEvent=self.mover_ventana
        self.ui.bt_restaurar.hide()
        #*Funciones con los botones para cada uno de los eventos
        #self.ui.pushButton.clicked.connect(self.abrir_archivo)
        self.ui.bt_filtrar.clicked.connect(self.mostrar_tabla)
        self.ui.download_LIST.clicked.connect(self.download_LISTS)
        self.ui.bt_inicio.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_tres))
        self.ui.bt_list.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_uno))	
        self.ui.bt_base_datos.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_dos))	
        self.ui.bt_congif.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_cuatro))		
        self.ui.bt_restaurar.clicked.connect(self.control_normal)
        self.ui.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.ui.bt_max.clicked.connect(self.control_max)
        self.ui.bt_close.clicked.connect(self.control_close)
        self.ui.bt_menu.clicked.connect(self.mover_menu)
        self.ui.bt_buscar_archivo.clicked.connect(self.abrir_archivo)
        self.ui.bt_filtrar_2.clicked.connect(self.upload_LIST)
        self.ui.bt_cancelar.clicked.connect(self.cancelar_stop)
        self.ui.bt_upload_file.clicked.connect(self.upload_file)
        self.ui.bt_save_path_list.clicked.connect(self.save_path_list)
        self.ui.comboBox.currentIndexChanged.connect(self.seleccion_archivo)
        self.index_stop=0
        self.count3=0
    #*Esta función abre desde el sistema solo archivos Excel  guarda la información en la variable direccion    
    def abrir_archivo(self):
        file=QFileDialog.getOpenFileName(self,"Abrir Archivo Excel", "","Excel Files (*.xlsx) ;; All Files (*)")
        self.direccion=file[0]
    #*Esta función llama a la función crear tabla lo unico que hace es correrlo en forma de hilos para que 
    #*corra en paralelo con la interfaz y cualquier proceso que se este ejecutando en el mismo instante    
    
    def mostrar_tabla(self):
        tabla_thread = threading.Thread(target=self.crear_tabla)
        tabla_thread.start()
        despues_thread=threading.Thread(target=self.crear_despues)
        despues_thread.start()

    def crear_tabla(self):#*Esta función filtra los datos del Dataframe requeridos y hace la tabla para mostrarla en la interfaz grafica
        variable =""
        try:
            file=pd.read_excel("Descargas/PRUEBA_4..xlsx")#*toma el archivo o la ruta y abre el archivo .xlsx
            df=pd.DataFrame(file)#*Lo convierte en Dataframe
            file_2=df.loc[:,['CMTS','Total','Description']].astype(str)#*Filtra las columnas en las que se requieren y transforma todos los datos en STR
            variable=self.ui.lineEdit_buscar.text()#*Toma lo que se ingrese en el LineEdit y lo pasa como texto almacenandolo en una variable
            variable=variable.upper()#*Debido a que todas las letras en la columna esta en mayuscula no importa lo que se digite en el LineEdit, lo transforma a mayuscula para facilitar el filtrado
            self.filtro=file_2[file_2['Description'].str.contains(variable,case=False,na=False,regex=True)]#*con el argumento contains revisa lo que se guarde en la varible,filtre y en la variable filtro guarde todo.
            if not (self.filtro['Description'].str.contains(variable,case=False,na=False,regex=True)!=variable).any() == (self.filtro['Description'].str.contains(variable,case=False,na=False,regex=True)==variable).any():#*Revisa con contains si lo ingresado en variable existe dentro del dataframe, si no existe continua sin realizar ningun proceso
                    print(self.filtro)
                    if  not variable=='':#*Con esta condicion revisa que que lo ingresado no este vacio y si lo esta no realiza ninguna operación
                        columnas=list(self.filtro.columns)#*Toma solo las columnas del Dataframe            
                        df_fila=self.filtro.to_numpy().tolist()#*lo transforma en una lista para revisar las filas del Dataframe                  
                        x=len(columnas)#*Toma el tamaño o longitud de la variable para luego recorrerlo en un for              
                        y=len(df_fila)#*Toma el tamaño o longitud de la variable para luego recorrerlo en un for                          
                        self.ui.tableWidget.setRowCount(y)#*inserta en el tableWidget la cantidad de filas que se van a mostrar                        
                        self.ui.tableWidget.setColumnCount(x)#*inserta en el tableWidget la cantidad de columnas que se van a mostrar                         
  
                        for j in range(x):#*Recorre las columnas 
                            encabezado=QtWidgets.QTableWidgetItem(columnas[j])#*Guarda los encabezados de cada columna
                            self.ui.tableWidget.setHorizontalHeaderItem(j,encabezado)#*Insterta en la tabla los encabezados guardados anteriormente
                            
                            for i in range (y):#*Recorre las filas
                                dato= str(df_fila[i][j])#*guarda en una lista posicion a posicion de los datos filtrados
                                if dato == 'nan':#*Revisa si hay algun dato vacio y si es asi colocarlo en blanco
                                    dato=''
                                self.ui.tableWidget.setItem(i,j,QTableWidgetItem(dato))#*Inserta posicion a posicion en el tableWidget
                                                          
                    else:
                        pass
            else:
                pass


        except ValueError:#*si hay un error de formato de archivo captura el archivo y lo muestra en un MessageBox
            QMessageBox.about (self,'Informacion', 'Formato incorrecto')
            return None
        except FileNotFoundError:#*si hay un error con el archivo, si esta dañado o no corresponde algo, captura el error y lo muestra en un MessageBox
            QMessageBox.about(self,'Informacion', 'El archivo esta \n malogrado')
            return None

    def crear_despues(self):
        try:
            path="data/Ocupacion.xlsx"
            file_despues=pd.read_excel(path,sheet_name='Hoja2',engine='openpyxl')
            df2=pd.DataFrame(file_despues)
            file_3=df2.loc[:,['IP','Dispositivo','Puerto','status','Unnamed: 5']].astype(str).fillna(value='No Data')
            
            variable2="PUERTOLIBRE"
            self.filtro2=file_3[file_3['Unnamed: 5'].str.contains(variable2,case=False,na=False,regex=True)].fillna(value='No Data')
            #print(self.filtro2)
            columnas2=list(self.filtro2.columns)#*Toma solo las columnas del Dataframe            
            df_fila2=self.filtro2.to_numpy().tolist()#*lo transforma en una lista para revisar las filas del Dataframe                  
            xx=len(columnas2)#*Toma el tamaño o longitud de la variable para luego recorrerlo en un for              
            yy=len(df_fila2)#*Toma el tamaño o longitud de la variable para luego recorrerlo en un for 
        except ValueError:#*si hay un error de formato de archivo captura el archivo y lo muestra en un MessageBox
            QMessageBox.about (self,'Informacion', 'Formato incorrecto')
            return None
        except FileNotFoundError:#*si hay un error con el archivo, si esta dañado o no corresponde algo, captura el error y lo muestra en un MessageBox
            QMessageBox.about(self,'Informacion', 'El archivo esta \n malogrado')
            return None                         
        self.ui.tabla.setRowCount(yy)#*inserta en el tableWidget la cantidad de filas que se van a mostrar                        
        self.ui.tabla.setColumnCount(xx)#*inserta en el tableWidget la cantidad de columnas que se van a mostrar                         
            
        for jj in range(xx):#*Recorre las columnas 
            encabezado2=QtWidgets.QTableWidgetItem(columnas2[jj])#*Guarda los encabezados de cada columna
            self.ui.tabla.setHorizontalHeaderItem(jj,encabezado2)#*Insterta en la tabla los encabezados guardados anteriormente
                                
            for ii in range (yy):#*Recorre las filas
                dato2= str(df_fila2[ii][jj])#*guarda en una lista posicion a posicion de los datos filtrados
                if dato2 == 'nan':#*Revisa si hay algun dato vacio y si es asi colocarlo en blanco
                    dato2=''
                self.ui.tabla.setItem(ii,jj,QTableWidgetItem(dato2))#*Inserta posicion a posicion en el tableWidget    
       

    def control_bt_minimizar(self):#*Función para minimizar el programa
        self.showMinimized()

    def control_normal(self):#*Función para restaurar los resize originales del programa
        self.showNormal()

        self.ui.bt_restaurar.hide()
        self.ui.bt_max.show()

    def control_max(self):#*Función para ampliar completamente la pantalla
        self.showMaximized()
        self.ui.bt_max.hide()
        self.ui.bt_restaurar.show()

    def control_close(self):#*Función para cerrar el programa
        self.close()
    def mover_menu(self):
        if True:
                width=self.ui.frame_lateral.width()
                normal=0
                if width==0:
                        extender=200
                else:
                        extender=normal

                self.animacion=QPropertyAnimation(self.ui.frame_lateral, b'minimumWidth' )
                self.animacion.setProperty("minimuWidth",200)
                self.animacion.setDuration(300)
                self.animacion.setStartValue(width)
                self.animacion.setEndValue(extender)
                self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animacion.start()

    def resizeEven(self,event):
        rect=self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self,event):
        self.clickPosition=event.globalPos()

    def mover_ventana(self,event):
         if self.isMaximized()==False:
              if event.buttons()==QtCore.Qt.LeftButton:
                   self.move(self.pos()+event.globalPos()-self.clickPosition)
                   self.clickPosition=event.globalPos()
                   event.accept()
         if event.globalPos().y()<=20:
              self.showMaximized()
         else:
              self.showNormal()    

   
    def upload_file(self):
        self.ad=Ui_ADVERTENCIA()
        self.ad.show()
        
        

    def update_progress_bar(self,value):
        self.ui.progressBar.setValue(value)
        if value==100:
            self.ui.progressBar.setValue(0)

    def cancelar_stop(self):
        self.index_stop=self.saved_index
        self.count3=self.count2
        self.index_saved=True
        url2="adfdsfdsfdsfdsgk"
        self.ctx=ClientContext(url2)
        self.ctx.execute_query()
        print(self.index_stop)
        self.update_progress_bar(100)
        
    def seleccion_archivo(self):
        seleccion=self.ui.comboBox.itemText(self.ui.comboBox.currentIndex())
        print(seleccion)   
        return seleccion
        


    def download_LISTS(self):
        
        LIST_NAME=self.ui.lineEdit_descargar_lista.text()
        FILE_NAME=self.seleccion_archivo()
        FOLDER_DEST=self.save_path_list()#!Revisar porque no se actualiza el path 
        print(FOLDER_DEST)
        file_name= download_lists.Type_file(FILE_NAME,EXPORT_TYPE)
        downloader_thread = threading.Thread(target=download_lists.download_list(LIST_NAME,EXPORT_TYPE,FOLDER_DEST,file_name))
        downloader_thread.start()
        


        

    def upload_LIST(self):
        
        self.upload_thread = threading.Thread(target=self.subir_list)
        
        self.upload_thread.start()
                
        
           
    def update_progress_bar(self,progress):
        self.ui.progressBar_2.setValue(progress)



    def subir_list(self):
        self.count2=0
        self.flag=1
        self.index_saved=False
        self.saved_index=0
        c=0
        count=0
        chunksize=1000#Cantidad de datos que va a recorrer del Dataframe, es decir va a coger x cantidad de datos y va a realizar todo el proceso con los datos y luego toam otra x cantidad de datos 
        last_index = 0 # índice del último elemento agregado
        commit_count=0
        commit_interval=50#cantidad de datos que manda por cada paquete
        # Manejar interrupciones y desconexiones, guardar el índice del último elemento agregado antes de la interrupción o desconexión
        #######################################################################################
        self.last_saved_index = 0
        max_attempts = 5 #Maxima cantidad de intentos que va a realizar el programa antes de acabarse
        attempt_count = 0
        total_items=0
        auth_context = AuthenticationContext(url)
        auth_context.acquire_token_for_user(username, password)
        #############################################################################
        ssl._create_default_https_context=ssl._create_unverified_context #*Quita la seguridad de número exedido de subida de datos
        self.ctx = ClientContext(url).with_credentials(UserCredential(username,password))
        self.ctx.clear
        #############################################################################
        list_title =self.ui.lineEdit_buscar_2.text()
        print(list_title)
        Sp_list = self.ctx.web.lists.get_by_title(list_title)#*Acceder a la lista
        
        print(Sp_list)
        self.ctx.load(Sp_list)
        self.ctx.execute_query()
        excel_file = self.direccion
        df = pd.read_excel(excel_file)
        file=pd.DataFrame(df)
        file_2=file.loc[:,['CMTS','Mac','Total','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
        file_2[['Mac','Total','Description']] = file_2[['Mac','Total','Description']].astype(str)#*Convierte los valores de estas columnas a tipo str
        data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario


        

        try:    
                print(self.flag==1)
                if  self.flag==1:
                    self.last_saved_index=self.index_stop
                    count=self.count3
                    print(f"count==>{count}")
                    print(f"L1==>{self.last_saved_index}")
                    self.flag=0
                    print(self.flag==1)
                while self.last_saved_index < len(data): 
                    
                    if  self.index_saved==False:
                         self.saved_index=self.last_saved_index
                         self.count2=count
                         


                    chunk=data[self.last_saved_index:self.last_saved_index+chunksize]
                    

                    for d in chunk:
                        c=c+1
                        item_properties = {'CMTS': d['CMTS'],'Mac':d['Mac'],'Total': d['Total'], 'Description': d['Description']}
                        
                        for i in range(max_attempts):
                            try:
                                item=Sp_list.add_item(item_properties)
                                
                                commit_count += 1
                                count+=1
                                progress=int((count/len(data))*100)
                                progress_bar_thread=threading.Thread(target=self.update_progress_bar,args=(progress,))
                                #progress_bar_thread.start()
                                #self.ui.progressBar_2.setValue(progress)
                                
                                if commit_count> commit_interval:
                                    print("Valor reestablecido :)")
                                    Sp_list.clear()
                                    commit_count=0
        
                                break  #* Si la inserción es exitosa, salir del ciclo for

                            except requests.exceptions.HTTPError as http_error:
                                
                                print(f"Error de HTTP al agregar el elemento #{c}: {http_error}")
                                time.sleep(5)  #* Esperar 5 segundos antes de intentar de nuevo
                                count=self.last_saved_index
                            except Exception as e:
                                
                                print(f"Error en el intento {i+1} de inserción para el elemento #{c}: {e}")
                                time.sleep(5)  #*Esperar 5 segundos antes de intentar de nuevo
                                if i == max_attempts - 1:
                                    # Si se alcanza el número máximo de intentos sin éxito, salir del programa
                                    print(f"No se pudo agregar el elemento #{c} después de {max_attempts} intentos. Saliendo del programa...")
                                    break
                        self.show()                
                        progress_bar_thread.start()
                        if commit_count==commit_interval:
                            self.ctx.execute_batch()       
                                
                            print("Se realizo Commit")
                            print(f"El último ID guardado en la lista es: {self.last_saved_index}")
                           
                            Sp_list.clear()
                            commit_count=0
                        self.show()
                    

                    if commit_count> commit_interval:
                        print("Valor reestablecido :)")
                        Sp_list.clear()
                        commit_count=0 
                    self.last_saved_index = self.last_saved_index+len(chunk)
                    
                    print(c)


                    if commit_count % commit_interval != 0:             
                        self.ctx.execute_batch()
                        print("Se realizo Commit2")
                        Sp_list.clear()
                        commit_count=0
                self.show()         
                self.last_saved_index2 = self.last_saved_index+len(chunk)
                progress_bar_thread.join()
                #self.ui.progressBar_2.deleteLater()    

                if commit_count> 0:
                    self.ctx.execute_batch()
                    print("commit final :)")
                    Sp_list.clear()
                    commit_count=0  
                self.show()
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):

                print("No hay conexión a internet. Esperando...")
                time.sleep(5)  # Esperar 5 segundos antes de volver a intentar
                
                pass  # Volver al inicio del bucle while
        except Exception as e:

                attempt_count += 1
               
                print(f"Error al Agregar el elemento a la lista #{c} error: {e}")
                print("Reintentando en 5 segundo...")
                time.sleep(5)
                if attempt_count >= max_attempts:
                    print("Se han excedido el número máximo de intentos. Saliendo del programa...")
                                 
    def save_path_list(self):
        path_list = self.ui.lineEdit_path_list.text()
        # Obtenemos el valor anterior de path_list_download del archivo .env
        old_path_list_download = env.get('path_list_download', '')
        print(f"path_list==>{path_list}")

        if self.ui.lineEdit_path_list.text()=='':
            new_path_list_download = old_path_list_download
            self.ui.lineEdit_path_list.setText('')
            #!PROBAR SI VACIANDO EL LINEEDIT PERMITE QUE VARIE Y NO SE QUEDE EN UN VALOR.
        else:
            new_path_list_download = path_list + "\\descarga"
            self.ui.lineEdit_path_list.setText('')

        print(f"new_path_list_download==>{new_path_list_download}")
        set_key(".env", "path_list_download", new_path_list_download)
        print(set_key(".env", "path_list_download", new_path_list_download))
        #FOLDER_DEST=env.get('path_list_download', '')
        FOLDER_DEST=new_path_list_download
        #FOLDER_DEST=FOLDER
        print(f"FOLDER_DEST==>{FOLDER_DEST}")
        return FOLDER_DEST
    
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    mi_app=MiApp()
    mi_app.show()
    sys.exit(app.exec_())

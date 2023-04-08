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
import urllib
import time
import ssl
import requests
import json
from dotenv import set_key,dotenv_values
import os
from pathlib import Path
from multiprocessing import Pool,cpu_count,freeze_support
import numpy as np
###########################################################################################################
#*Variables de entorno para las funciones con SharePoint
env=dotenv_values(".env")
username = env["sharepoint_email"]
password = env["sharepoint_password"]
url = env['sharepoint_url_site']

FOLDER_DEST="C:\\Users\\IC0167A\\Desktop\\Proyecto_final\\Descargas"
EXPORT_TYPE='Excel'

##############################################################################################################
name_files=["Arris_SCMSummary.xlsx","Casa_SCMSummary.xlsx","Ocupacion - Marcacion RPHY Harmonic.xlsx"]
ruta_de_busqueda=['C:\\Users\\IC0167A\\Desktop\\Documents','C\\Users']
sheet_names=[None,None,'Hoja2','Hoja5']
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
        self.ui.bt_search_files.clicked.connect(self.filtrado_COS_DAAS)
        self.index_stop=0
        self.count3=0




    #*Esta función abre desde el sistema solo archivos Excel  guarda la información en la variable direccion    
    def abrir_archivo(self):
        file=QFileDialog.getOpenFileName(self,"Abrir Archivo Excel", "","Excel Files (*.xlsx) ;; All Files (*)")
        self.direccion=file[0]
    #*Esta función llama a la función crear tabla lo unico que hace es correrlo en forma de hilos para que 
    #*corra en paralelo con la interfaz y cualquier proceso que se este ejecutando en el mismo instante    
    

    def complet_COS(self,df):
        todos_valores_num1=pd.Series(range(1,113))
        todos_valores_num1=pd.concat([pd.Series([1]),todos_valores_num1,pd.Series([112])])
        todos_valores_num2=pd.Series(range(0,1))
        todos_valores_num2=pd.concat([pd.Series([0]),todos_valores_num2,pd.Series([1])])
        print(todos_valores_num2)
        dispositivos=df['Dispositivo'].unique()
        dispositivos_con_puertos_faltantes=[]
        for dispositivo in dispositivos:
            puertos=df[df['Dispositivo']==dispositivo]['Puerto'].apply(lambda x:int(x.split(':')[-1]))
            puertos_faltantes=todos_valores_num1[~todos_valores_num1.isin(puertos)]
            if len(puertos_faltantes)>0:
                dispositivos_con_puertos_faltantes.append(dispositivo)


        nuevas_filas=[]
        for dispositivo in dispositivos_con_puertos_faltantes:
            puertos=df[df['Dispositivo']==dispositivo]['Puerto'].apply(lambda x: int(x.split(':')[-1]))
            valores_faltantes=todos_valores_num1[~todos_valores_num1.isin(puertos)]
            
            for puerto in valores_faltantes[valores_faltantes<=112]:

                puerto_str=str(puerto)+':0'
                puerto2_str=str(puerto)+':1'
                ip=df[df['Dispositivo']==dispositivo]['IP'].iloc[0]
                nuevas_filas.append((ip,dispositivo,puerto_str,"-","-","-","offline","unlocked"))
                nuevas_filas.append((ip,dispositivo,puerto2_str,"-","-","-","offline","unlocked"))
        nuevas_filas_df=pd.DataFrame(nuevas_filas,columns=df.columns)

        df=pd.concat([df,nuevas_filas_df]).sort_values(['Dispositivo','Puerto']).reset_index(drop=True)
        df=df.drop_duplicates()
        df=df.drop_duplicates(subset=['Dispositivo','Puerto'])
        return df


    def complete_DAAS(self,df):
        # Crear una serie con todos los valores posibles de puerto
        todos_los_valores = pd.Series(range(1, 49))
        todos_los_valores = pd.concat([pd.Series([0]), todos_los_valores, pd.Series([48])])

        # Identificar dispositivos con puertos faltantes
        dispositivos = df['Dispositivo'].unique()
        dispositivos_con_puertos_faltantes = []
        for dispositivo in dispositivos:
            puertos = df[df['Dispositivo'] == dispositivo]['Puerto'].apply(lambda x: int(x.split('/')[-1]))
            puertos_faltantes = todos_los_valores[~todos_los_valores.isin(puertos)]
            if len(puertos_faltantes) > 0:
                dispositivos_con_puertos_faltantes.append(dispositivo)

        # Crear DataFrame con nuevas filas para cada dispositivo
        nuevas_filas = []
        for dispositivo in dispositivos_con_puertos_faltantes:
            puertos = df[df['Dispositivo'] == dispositivo]['Puerto'].apply(lambda x: int(x.split('/')[-1]))
            valores_faltantes = todos_los_valores[~todos_los_valores.isin(puertos)]
            valores_faltantes_menores=valores_faltantes[valores_faltantes <= 48]
            if not valores_faltantes_menores.empty:
                for puerto in valores_faltantes_menores:
                    puerto_str = 'xe-0/0/' + str(puerto)
                    ip_series = df[df['Dispositivo'] == dispositivo]['IP']
                    if not ip_series.empty:
                        ip=ip_series.iloc[0]
                    else:
                        ip=np.nan
                    #ocupacion = df[df['Dispositivo'] == dispositivo]['Unnamed: 5'].iloc[0]
                    nuevas_filas.append((ip, dispositivo, puerto_str, np.nan, np.nan, "PUERTOLIBRE"))
        nuevas_filas_df = pd.DataFrame(nuevas_filas, columns=df.columns)

        # Concatenar DataFrame original con nuevas filas y ordenar por dispositivo y puerto
        df = pd.concat([df, nuevas_filas_df]).sort_values(['Dispositivo', 'Puerto']).reset_index(drop=True)
        df=df.drop_duplicates()
        return df

    def simpli_DAAS(self,df):
        Valor_Dispositivo=df['Dispositivo']
        Valor_Ip=df['IP']
        valor_dispositivo=Valor_Dispositivo.index
        valor_list_dispositivo=valor_dispositivo.to_list()
        valor_IP=Valor_Ip.index
        valor__list_IP=valor_IP.to_list()      
        indice_IP=valor__list_IP[0]
        indice_IP2=valor__list_IP[0]
        indice_Dispositivo=valor_list_dispositivo[0]
        Dispositivo= df.loc[indice_Dispositivo, "Dispositivo"]
        IP=df.loc[indice_IP,"IP"]
        IP2=df.loc[indice_IP2,"IP"]
        Sli_IP=IP.find(".")
        Slic_IP=IP.find(".",Sli_IP+1)
        SLICE_IP=IP.find(".",Slic_IP+1)
        Sli_IP2=IP2.find(".")
        Slic_IP2=IP2.find(".",Sli_IP2+1)
        SLICE_IP2=IP2.find(".",Slic_IP2+1)
        filter_IP=int(IP[SLICE_IP+1:])
        filter_IP2=int(IP2[SLICE_IP2+1:])

        return Dispositivo,filter_IP,filter_IP2

    def filtrado_COS_DAAS(self):
         try:
            path_arris="Documents/Arris_SCMSummary.xlsx"
            path_casa="Documents/Casa_SCMSummary.xlsx"
            file_arris=pd.read_excel(path_arris)
            file_casa=pd.read_excel(path_casa)
            df=pd.DataFrame(file_arris)
            df_casa=pd.DataFrame(file_casa)
            df_casa=df_casa.loc[:,['CMTS','Upstream','Total','Description']]
            df_casa=df_casa.rename(columns={'Upstream':'S'})
            file_2=df.loc[:,['CMTS','Mac','Total','Description']]
            file_2[['Mac','Total','Description']] = file_2[['Mac','Total','Description']].astype(str)
            #print(file_2)
            df_concat = pd.concat([file_2, df_casa])
            #print(df_concat)
            #variable="39g1"
            #variable="fas1"
            variable=self.ui.lineEdit_buscar.text()
            variable=variable.upper()#*Debido a que todas las letras en la columna esta en mayuscula no importa lo que se digite en el LineEdit, lo transforma a mayuscula para facilitar el filtrado
            self.filtro=df_concat[df_concat['Description'].str.contains(variable,case=False,na=False,regex=True)]#*con el argumento contains revisa lo que se guarde en la varible,filtre y en la variable filtro guarde todo.
            #print(self.filtro)
            
            ciudad=self.filtro['CMTS']
            #print(ciudad)
            valor=ciudad.index
            valor_list=valor.to_list()
            indice=valor_list[1]
            v = self.filtro.loc[indice, "CMTS"]

            print(v)
            sep=v.find("-")
            sep2=v.find("-",sep+1)
            variable3=v[:sep2]
            print(variable3)

            path_DAAS="Documents/Ocupacion - Marcacion RPHY Harmonic.xlsx"
            file_DAAS=pd.read_excel(path_DAAS,sheet_name='Hoja2',engine='openpyxl')
            df2=pd.DataFrame(file_DAAS)
            #print(df2)
            df_das=self.complete_DAAS(df2)
            #print(df2)
            file_3=df_das.loc[:,['IP','Dispositivo','Puerto','status','Unnamed: 4','Unnamed: 5']].astype(str).fillna(value='No Data')          
            variable2="PUERTOLIBRE"
            #variable3="BOGO-GARCE"
            filtro2=file_3[file_3['Unnamed: 5'].str.contains(variable2,case=False,na=False,regex=True)].fillna(value='No Data')
            
            filtro3=filtro2[filtro2['Dispositivo'].str.contains(variable3,case=False,na=False,regex=True)].fillna(value='No Data')
            filtro3_sin_duplicados = filtro3.drop_duplicates()
            #print(filtro3_sin_duplicados)
            variable_disp,variable_ip,variable_ip2=self.simpli_DAAS(filtro3)
            filtro4=filtro3_sin_duplicados[filtro3_sin_duplicados['Dispositivo'].str.contains(variable_disp,case=False,na=False,regex=True)]#!Opcion 1
            ############!Opcion2
            if filtro3_sin_duplicados['IP'].str.contains(str(variable_ip)).any():
                in_colum=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip),case=False,na=False,regex=True)
                temp_df=filtro3_sin_duplicados[in_colum]
                en_tempo=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip+1),case=False,na=False,regex=True)
                CON_DAAS_COS=filtro3_sin_duplicados[in_colum | en_tempo]
                CON_DAAS_COS.to_excel("out10.xlsx")
                #print(filtro3_sin_duplicados[in_colum | en_tempo])
            elif filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2)).any():
                in_colum=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2),case=False,na=False,regex=True)
                temp_df=filtro3_sin_duplicados[in_colum]
                en_tempo=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2+1),case=False,na=False,regex=True)
                CON_DAAS_COS=filtro3_sin_duplicados[in_colum | en_tempo]
                CON_DAAS_COS.to_excel("out10.xlsx")
            path_COS="Documents/Ocupacion - Marcacion RPHY Harmonic.xlsx"
            file_COS=pd.read_excel(path_COS,sheet_name='Hoja5',engine='openpyxl')
            df_cos=pd.DataFrame(file_COS)
            df_out=self.complet_COS(df_cos)
            #print(df_cos)
            df_out=df_out[df_out['Dispositivo'].str.contains(variable3,case=False,na=False,regex=True)]
            #print(df_out)
            ptp="unlocked"
            df_out2=df_out[df_out['ptp'].str.contains(ptp,case=False,na=False,regex=True)]#*Filtrado columna ptp
            #print(f"df_out2==>{df_out2}")
            df_out2=df_out2.loc[:,['Dispositivo','Puerto','ptp']]
            df_out2=df_out2.rename(columns={'Dispositivo':'Dispositivo COS'}) 
            CON_DAAS_COS=CON_DAAS_COS.loc[:,['Dispositivo','Puerto','Unnamed: 5']]
            CON_DAAS_COS=CON_DAAS_COS.rename(columns={'Dispositivo':'Dispositivo DAAS'}) 
            df_out2=pd.concat([df_out2, pd.Series([None] * len(df_out2.columns), index=df_out2.columns)], ignore_index=True)
            CON_DAAS_COS=pd.concat([CON_DAAS_COS, pd.Series([None] * len(CON_DAAS_COS.columns), index=CON_DAAS_COS.columns)], ignore_index=True)
            final=pd.concat([df_out2,CON_DAAS_COS],axis=1)
            #print(final)

            DIS_COS=final['Dispositivo COS']
            index_DIS_COS=DIS_COS.index
            index_DIS_COS_list=index_DIS_COS.to_list()
            indice_DIS_COS=index_DIS_COS_list[1]
            UNO = final.loc[indice_DIS_COS, "Dispositivo COS"]

            #print(UNO)
            first=UNO.find("-")
            second=UNO.find("-",first+1)
            three=UNO.find("-",second+1)
            four=UNO.find("-",three+1)
            UN_COS=UNO[three+1:four]
            #print(UN_COS)
            if final['Dispositivo COS'].str.contains(UN_COS,case=False,na=False,regex=True).any():
                NO_dos_COS=final['Dispositivo COS'].str.contains(UN_COS,case=False,na=False,regex=True)
                self.FINAL_FILTRADO=final[NO_dos_COS]
            else:
                self.FINAL_FILTRADO=final
            print(self.FINAL_FILTRADO )    
            final.to_excel("out8.xlsx")
            self.FINAL_FILTRADO.to_excel("out11.xlsx")##RETORNAR FINAL_FILTRADO PARA LA VISUALIZACION DE LA TABLA DEL DESPUES
            return self.filtro,self.FINAL_FILTRADO
         except KeyError as e:
              print(e)

    def mostrar_tabla(self):
        tabla_thread = threading.Thread(target=self.crear_tabla)
        tabla_thread.start()
        despues_thread=threading.Thread(target=self.crear_despues)
        despues_thread.start()

    def crear_tabla(self):#*Esta función filtra los datos del Dataframe requeridos y hace la tabla para mostrarla en la interfaz grafica
        self.variable =""
        try:

            self.variable=self.ui.lineEdit_buscar.text()#*Toma lo que se ingrese en el LineEdit y lo pasa como texto almacenandolo en una variable
            self.variable=self.variable.upper()#*Debido a que todas las letras en la columna esta en mayuscula no importa lo que se digite en el LineEdit, lo transforma a mayuscula para facilitar el filtrado
            filtro,x=self.filtrado_COS_DAAS()
            
            if not (filtro['Description'].str.contains(self.variable,case=False,na=False,regex=True)!=self.variable).any() == (self.filtro['Description'].str.contains(self.variable,case=False,na=False,regex=True)==self.variable).any():#*Revisa con contains si lo ingresado en variable existe dentro del dataframe, si no existe continua sin realizar ningun proceso
                    #print(self.filtro)
                    if  not self.variable=='':#*Con esta condicion revisa que que lo ingresado no este vacio y si lo esta no realiza ninguna operación
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
            x,FINAL_DESPUES=self.filtrado_COS_DAAS()
            print(FINAL_DESPUES)

            columnas2=list(FINAL_DESPUES.columns)#*Toma solo las columnas del Dataframe            
            df_fila2=FINAL_DESPUES.to_numpy().tolist()#*lo transforma en una lista para revisar las filas del Dataframe                  
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
        




    def download_LISTS(self):
        LIST_NAME=self.ui.lineEdit_descargar_lista.text()
        FILE_NAME=self.ui.lineEdit_nombre_lista.text()

        file_name= download_lists.Type_file(FILE_NAME,EXPORT_TYPE)
        downloader_thread = threading.Thread(target=download_lists.download_list(LIST_NAME,EXPORT_TYPE,FOLDER_DEST,file_name))
        downloader_thread.start()
        


        

    def upload_LIST(self):
        
        self.upload_thread = threading.Thread(target=self.subir_list(self))
        
        self.upload_thread.start()
                
        
           
    def update_progress_bar(self,progress):
        self.ui.progressBar_2.setValue(progress)


######################################################################################

    def buscar_archivo(self,name_file,ruta):
            for root,dirs, files in os.walk(ruta):
                for file in files:
                    if file.endswith('.xlsx') and file==name_file:
                        return Path(root)/file
    
    def obtener_dataframes(self,name_files,ruta_de_busqueda):            
            if __name__=='__main__':
                freeze_support()       
                with Pool(processes=os.cpu_count()) as pool:
                    rutas_files=pool.starmap(self.buscar_archivo,[(name_file,ruta) for ruta in ruta_de_busqueda for name_file in name_files])
                    rutas_files=[ruta_file for ruta_file in rutas_files if ruta_file is not None]
                dfs={}
                for ruta_file,sheet_name in zip(rutas_files,sheet_names):
                    print(ruta_file.name,sheet_name)
                    if sheet_name is not None:
                        for sheet_name in sheet_names:

                            df=pd.read_excel(ruta_file,sheet_name=sheet_name,engine='openpyxl')
                            dfs[f"{sheet_name }_{ruta_file.name}"]=df
                    else:
                        df=pd.read_excel(ruta_file)
                        dfs[ruta_file.name]=df
                                
                return dfs
    def read_data(self):
            arris_df=None
            ocupacion_Cos=None
            ocupacion_Daas=None
            Casa_df=None
            if __name__=='__main__':  
                dataframes=self.obtener_dataframes(name_files,ruta_de_busqueda)
                arris_df=dataframes['Arris_SCMSummary.xlsx']
                Casa_df=dataframes['Casa_SCMSummary.xlsx']
                for key in dataframes.keys():
                    print(key)  # Imprimir las claves del diccionario
                if 'Hoja5_Ocupacion - Marcacion RPHY Harmonic.xlsx' in dataframes.keys():
                    ocupacion_Cos = dataframes['Hoja5_Ocupacion - Marcacion RPHY Harmonic.xlsx']
                    print(ocupacion_Cos)
                if 'Hoja2_Ocupacion - Marcacion RPHY Harmonic.xlsx' in dataframes.keys():
                    ocupacion_Daas = dataframes['Hoja2_Ocupacion - Marcacion RPHY Harmonic.xlsx']
                    
            return arris_df,ocupacion_Daas,ocupacion_Cos,Casa_df    
    def search_file_filter(self):
    
            file_arris,file_despues_DAAS,file_despues_COS,file_casa=self.read_data()
        
##########################################################################################

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
        file=file.rename(columns={'S/CG/CH':'Sa'})
        file_2=file.loc[:,['CMTS','Sa','Total','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
        file_2[['Sa','Total','Description']] = file_2[['Sa','Total','Description']].astype(str)#*Convierte los valores de estas columnas a tipo str
        data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario
        #print(data)

        

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
                        item_properties = {'CMTS': d['CMTS'],'Sa':d['Sa'],'Total': d['Total'], 'Description': d['Description']}
                        
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
                                 
    
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    mi_app=MiApp()
    mi_app.show()
    sys.exit(app.exec_())

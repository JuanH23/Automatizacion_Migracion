import sys
from modules.statics.Estructura_principal_FINAL import*
from PyQt5.QtWidgets import QTableWidgetItem,QFileDialog,QMessageBox
from PyQt5 import QtCore, QtWidgets
import pandas as pd
import modules.models.download_lists
import threading
from modules.models.office365_api import SharePoint
import modules.models.download_lists
from PyQt5.QtCore import QTimer
from modules.models.Advertencia import*
from modules.models.search_files import Search
from modules.models.Prueba_formato import diseño
#*Librerias utilizadas en la función de subir lista a SharePoint
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files import file
from office365.sharepoint.files.file import File
from office365.sharepoint.lists.list import List   
import time
import ssl
import requests
from dotenv import set_key,dotenv_values
import os
from pathlib import Path
from multiprocessing import Pool,cpu_count,freeze_support
import numpy as np
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyQt5.QtCore import pyqtSignal, QObject
from dotenv import load_dotenv
#*Variables de entorno para las funciones con SharePoint
load_dotenv()
env=dotenv_values(".env")
username = env["sharepoint_email"]
password = env["sharepoint_password"]
url = env['sharepoint_url_site']
ruth_list_download= env["path_list_download"]
EXPORT_TYPE='Excel'
#Lista de los nombres de los archivos que se van a buscar en el PC
name_files=["Arris_SCMSummary.xlsx","Casa_SCMSummary.xlsx","Ocupacion- RPHY Harmonic_DAAS.xlsx","Ocupacion-Harmonic_COS.xlsx"]
sheet_names=[None,None,None,None]#Si hay algun archivo con mas de una hoja, colocar el nombre de la hoja 
#en orden de los archivos de la lista name_files
class SignalHandler(QObject):
    download_finished = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
 # Establece el evento de finalización
class MiApp(QtWidgets.QMainWindow):
    update_progressBar=QtCore.pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.gripSize=10
        self.grip=QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize,self.gripSize)
        self.signal_handler = SignalHandler()
        self.signal_handler.download_finished.connect(self.finish)
        #*Funciones con los botones para cada uno de los eventos
        self.ui.bt_filtrar.clicked.connect(self.mostrar_tabla)
        self.ui.download_LIST.clicked.connect(self.download_LISTS)
        self.ui.bt_inicio.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_tres))
        self.ui.bt_list.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_uno))	
        self.ui.bt_base_datos.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_dos))	
        self.ui.bt_config.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_cuatro))		
        self.ui.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.ui.bt_close.clicked.connect(self.control_close)
        self.ui.search_files.clicked.connect(self.abrir_archivo)
        self.ui.bt_filtrar_2.clicked.connect(self.upload_LIST)
        self.ui.bt_stop.clicked.connect(self.cancelar_stop)
        self.ui.bt_upload_file.clicked.connect(self.upload_file)
        self.ui.bt_search_files.clicked.connect(self.search_file_filter)
        self.ui.bt_save_con.clicked.connect(self.save_path_list)
        self.ui.bt_save_con.clicked.connect(self.save_parameters_url_sharepoint)
        self.ui.bt_save_con.clicked.connect(self.save_parameters_name_folder_Sharepoint)
        self.ui.comboBox.currentIndexChanged.connect(self.seleccion_archivo)
        self.ui.comboBox2.currentIndexChanged.connect(self.seleccion_archivo_2)
        self.index_stop=0
        self.count3=0
        self.search=Search()
        self.file_arris=0
        self.file_despues_DAAS=0
        self.file_despues_COS=0
        self.file_casa=0
        self.c_up=0
        self.continuar_subida=True
        self.update_progressBar.connect(self.ui.progressBar_2.setValue)
        self.FOLDER_DEST=""
        self.sch=0
        self.ruta_de_busqueda=[]
        self.seleccion_2=""
        self.flag=0
        self.process=True
        self.btc_stop=0
    
    def show_popup(self):
        #Hace con la función Qtimer.singleShot, que se ejecute una sola vez el mensaje
        QTimer.singleShot(0, self.popup) 
    def popup(self):
        QMessageBox.warning(self,"Advertencia",
        f"Programa finalizado, El último ID guardado en la lista es: {self.count3}") 
    def show_error(self):
        QTimer.singleShot(0, self.error) #Hace con la función Qtimer.singleShot, que se ejecute una sola vez el mensaje de error
    def error(self):
            QMessageBox.warning(self,"Advertencia",
            f"Por favor seleccione un documento a subir")
    def show_finish(self):
        QTimer.singleShot(0, self.finish) 
    def finish(self):
        QMessageBox.information(self, "Proceso finalizado", "La descarga se ha completado correctamente.")
    def show_not_find(self):
        QTimer.singleShot(0, self.not_find) 
    def not_find(self):
        QMessageBox.information(self, "Error de busqueda", "No se encuentra el nodo, busque nuevamente.")

    def update_progress_bar_Slot(self,value):
        self.ui.progressBar_2.setValue(value)
        
    def abrir_archivo(self):
        #*Esta función abre desde el sistema solo archivos Excel  guarda la información en la variable direccion
        #file: obtiene toda la informacion de el archivo, solo permitiendo abrir archivos Excel (xlsx)
        try:
            file=QFileDialog.getOpenFileName(self,"Abrir Archivo Excel", "","Excel Files (*.xlsx) ;; All Files (*)")
            self.direccion=file[0]
        except AttributeError:
            QMessageBox.warning(self,"Advertencia",
            f"Por favor seleccione un documento a subir")   
            
    #*Esta función llama a la función crear tabla lo unico que hace es correrlo en forma de hilos para que 
    #*corra en paralelo con la interfaz y cualquier proceso que se este ejecutando en el mismo instante    
    
    def complet_COS(self,df):

        #todos_valores_num1: Da un rango de valores el cual va a completar los puertos COS, del rango 1-112
        #dispositivos:dispositivos guarda como valores unicos a la columna del Dataframe 'Dispositivo'
        #puertos: guarda los valores resultantes de realizar una separacion de los datos de la columna 'Puerto' que contenga el simbolo ':'
        # y lo compara para guardar unicamente los que contengan esto 
        #puertos_faltantes: este va a mirar que valores faltan dentro del rango de valores de la variable todos_valores_num1
        #y va revisar si los valores de puertos estan dentro de el 
        #dispositivos_con_puertos_faltantes: esta variable que es una lista, va a ir añadiendo los valores faltantes
        #nuevas_filas: esta variable va a añadir todos los valores con sus numeros faltantes
        #puerto_str: va a ser la variable para añadir los puertos faltantes con su segundo numero :0
        #puerto2_str: va a ser la variable para añadir los puertos faltantes con su segundo numero :1
        #ip: toma los valores de la columna ip para añadirla en todos los valores de la nueva lista "nuevas_filas"
        #param df: Un DataFrame de pandas que contiene información sobre los dispositivos y sus puertos
        #return:una versión modificada del marco de datos de entrada `df`, con filas adicionales agregadas
        #para completar los números de puerto que faltan para cada dispositivo.
        todos_valores_num1=pd.Series(range(1,113))
        todos_valores_num1=pd.concat([pd.Series([1]),todos_valores_num1,pd.Series([112])])
        todos_valores_num2=pd.Series(range(0,1))
        todos_valores_num2=pd.concat([pd.Series([0]),todos_valores_num2,pd.Series([1])])      
        #print(todos_valores_num2)
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
                nuevas_filas.append((ip,dispositivo,puerto_str,"-","-","offline","unlocked"))
                nuevas_filas.append((ip,dispositivo,puerto2_str,"-","-","offline","unlocked"))
        nuevas_filas_df=pd.DataFrame(nuevas_filas,columns=df.columns)
        
        df=pd.concat([df,nuevas_filas_df]).sort_values(['Dispositivo','Puerto']).reset_index(drop=True)
        df=df.drop_duplicates()
        df=df.drop_duplicates(subset=['Dispositivo','Puerto'])
        return df

    def complete_DAAS(self,df):
        #:param df: un DataFrame de pandas que contiene información sobre los dispositivos de red y sus puertos
        #:return: un DataFrame modificado con nuevas filas agregadas para dispositivos a los que les faltan puertos
        #todos_valores_num1: Da un rango de valores el cual va a completar los puertos COS, del rango 1-112,Creando una serie con todos los valores posibles de puerto
        #dispositivos:dispositivos guarda como valores unicos a la columna del Dataframe 'Dispositivo'
        #puertos: guarda los valores resultantes de realizar una separacion de los datos de la columna 'Puerto' que contenga el simbolo ':'
        # y lo compara para guardar unicamente los que contengan esto 
        #puertos_faltantes: este va a mirar que valores faltan dentro del rango de valores de la variable todos_valores_num1
        #y va revisar si los valores de puertos estan dentro de el 
        #dispositivos_con_puertos_faltantes: esta variable que es una lista, va a ir añadiendo los valores faltantes
        #nuevas_filas: esta variable va a añadir todos los valores con sus numeros faltantes
        #puerto_str: va a ser la variable para añadir los puertos faltantes con su segundo numero :0
        #puerto2_str: va a ser la variable para añadir los puertos faltantes con su segundo numero :1
        #ip: toma los valores de la columna ip para añadirla en todos los valores de la nueva lista "nuevas_filas"
        #param df: Un DataFrame de pandas que contiene información sobre los dispositivos y sus puertos
        #return:una versión modificada del marco de datos de entrada `df`, con filas adicionales agregadas
        #para completar los números de puerto que faltan para cada dispositivo.        
        # Crear una serie con todos los valores posibles de puerto
        todos_los_valores = pd.Series(range(1, 49))
        todos_los_valores = pd.concat([pd.Series([0]), todos_los_valores, pd.Series([48])])
        dispositivos = df['Dispositivo'].unique()# Identificar dispositivos con puertos faltantes
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
                    nuevas_filas.append((ip, dispositivo, puerto_str, np.nan, np.nan, "PUERTOLIBRE"))
        nuevas_filas_df = pd.DataFrame(nuevas_filas, columns=df.columns)
        df = pd.concat([df, nuevas_filas_df]).sort_values(['Dispositivo', 'Puerto']).reset_index(drop=True)# Concatenar DataFrame original con nuevas filas y ordenar por dispositivo y puerto
        df=df.drop_duplicates()
        return df

    def simpli_DAAS(self,df):
        #Lo principal es que hace slicing en valores especificos en dos columnas 'Dispositivo' y 'IP'
        #Esto para retornar valores que ayudaran a filtrar y reducir los valores que se quieren obtenter
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
        se_daas=Dispositivo.find("-")
        sel_daas=Dispositivo.find("-",se_daas+1)
        sele_daas=Dispositivo.find("-",sel_daas+1)
        fin_sele_daas=Dispositivo.find("-",sele_daas+1)
        filter_Daas=Dispositivo[sele_daas+1:fin_sele_daas]     
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
        return Dispositivo,filter_IP,filter_IP2,int(filter_Daas)

# The code defines a method called "filtrado_COS_DAAS" that takes no arguments. Within the method, it
# performs various data manipulations and filtering on input data stored in instance variables of the
# class. The method then returns the filtered data as well as two dataframes called "COS" and "DAAS".
# Finally, it calls a function called "diseño" with some of the filtered data as arguments.

    def filtrado_COS_DAAS(self):

         try:           
            df=pd.DataFrame(self.file_arris)            #Lee el archivo encontrado de ARRIS
            df_casa=pd.DataFrame(self.file_casa)        #Lee el archivo encontrado de CASA
            df_casa=df_casa.loc[:,['CMTS','Upstream','Total','Description']].astype(str).fillna('No data')    #Filtra las columnas necesarias para realizar el filtrado      
            df_casa=df_casa.rename(columns={'Upstream':'Up'})       #Cambia el nombre de la columna
                                                        #Filtra las columnas necesarias para realizar el filtrado
            file_2=df.loc[:,['CMTS','Up','Total','Description']].astype(str).fillna('No data')
            df_concat = pd.concat([file_2, df_casa])    #Une el Dataframe de ARRIS con el de CASA                                                                                                      
            variable=self.ui.lineEdit_buscar.text()     #Toma el nombre del nodo que se dijite en el LineEdit
            variable=variable.upper()                   #*Debido a que todas las letras en la columna esta en mayuscula no importa lo que se digite en el LineEdit, lo transforma a mayuscula para facilitar el filtrado
            self.filtro=df_concat[df_concat['Description'].str.contains(variable,case=False,na=False,regex=True)]#*con el argumento contains revisa lo que se guarde en la varible,filtre y en la variable filtro guarde todo. 
            ciudad=self.filtro['CMTS']
            valor=ciudad.index
            valor_list=valor.to_list()
            indice=valor_list[0]
            v = self.filtro.loc[indice, "CMTS"]
            #print(v)
            sep=v.find("-")
            sep2=v.find("-",sep+1)
            variable3=v[:sep2]
            #print(variable3)
            df2=pd.DataFrame(self.file_despues_DAAS)    #Lee el archivo encontrado de DAAS
            df_das=self.complete_DAAS(df2)              #coloca la variable df2 en la funcion complete_DAAS, para completar los puertos faltantes
            #Filtra las columnas necesarias para realizar el filtrado
            file_3=df_das.loc[:,['IP','Dispositivo','Puerto','status','stat2','ptp']].astype(str).fillna(value='No Data')          
            variable2="PUERTOLIBRE"  #utiliza la palabra clave "PUERTO LIBRE" para reducir la cantidad de resultados
            #Realiza el filtro con la variable2
            filtro2=file_3[file_3['ptp'].str.contains(variable2,case=False,na=False,regex=True)].fillna(value='No Data')     
            #Realiza el filtro con la variable2
            filtro3=filtro2[filtro2['Dispositivo'].str.contains(variable3,case=False,na=False,regex=True)].fillna(value='No Data')
            filtro3_sin_duplicados = filtro3.drop_duplicates()      #Elimina filas duplicadas
            variable_disp,variable_ip,variable_ip2,filter_daas=self.simpli_DAAS(filtro3)
            #filtro4=filtro3_sin_duplicados[filtro3_sin_duplicados['Dispositivo'].str.contains(variable_disp,case=False,na=False,regex=True)]#!Opcion 1
            ############!Opcion2
            #Para reducir la cantidad de dispositivos DAAS toma la variable_ip y variable_ip+1 para que solo puedan haber dos
            if filtro3_sin_duplicados['IP'].str.contains(str(variable_ip)).any():
                in_colum=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip),case=False,na=False,regex=True)
                temp_df=filtro3_sin_duplicados[in_colum]
                en_tempo=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip+1),case=False,na=False,regex=True)
                CON_DAAS_COS=filtro3_sin_duplicados[in_colum | en_tempo]
                #CON_DAAS_COS.to_excel("out10.xlsx")
            elif filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2)).any():
                in_colum=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2),case=False,na=False,regex=True)
                temp_df=filtro3_sin_duplicados[in_colum]
                en_tempo=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2+1),case=False,na=False,regex=True)
                CON_DAAS_COS=filtro3_sin_duplicados[in_colum | en_tempo]
                #CON_DAAS_COS.to_excel("out10.xlsx")
            if CON_DAAS_COS['Dispositivo'].str.contains(str(filter_daas+1)).any():
                if CON_DAAS_COS['Dispositivo'].str.contains(str(filter_daas)).any():
                    column_daas=CON_DAAS_COS['Dispositivo'].str.contains(str(filter_daas),case=False,na=False,regex=True)
                    en_tempo_daas=CON_DAAS_COS['Dispositivo'].str.contains(str(filter_daas+1),case=False,na=False,regex=True)
                    DOS_DAAS=CON_DAAS_COS[column_daas | en_tempo_daas]
                    
            else:
                 DOS_DAAS=CON_DAAS_COS[CON_DAAS_COS['Dispositivo'].str.contains(str(filter_daas),case=False,na=False,regex=True)]    
            df_cos=pd.DataFrame(self.file_despues_COS)      #Lee el archivo encontrado de COS
            df_cos=df_cos.loc[:,['IP','Dispositivo','Puerto','ID','moka','status','ptp']]
            #print(df_cos)
            df_out=self.complet_COS(df_cos)           
            df_out=df_out[df_out['Dispositivo'].str.contains(variable3,case=False,na=False,regex=True)]
            ptp="unlocked"      #utiliza la palabra clave "unlocked" para reducir la cantidad de resultados
            df_out2=df_out[df_out['ptp'].str.contains(ptp,case=False,na=False,regex=True)]#*Filtrado columna ptp
            df_out2=df_out2.loc[:,['Dispositivo','Puerto','ptp']]
            df_out2=df_out2.rename(columns={'Dispositivo':'Dispositivo COS'})
            df_out2=df_out2.rename(columns={'Puerto':'Puerto COS'})  
            DOS_DAAS=DOS_DAAS.loc[:,['Dispositivo','Puerto','ptp']]
            DOS_DAAS=DOS_DAAS.rename(columns={'Dispositivo':'Dispositivo DAAS'})
            DOS_DAAS=DOS_DAAS.rename(columns={'Puerto':'Puerto DAAS'})
            df_out2=pd.concat([df_out2, pd.Series([None] * len(df_out2.columns), index=df_out2.columns)], ignore_index=True)
            DOS_DAAS=pd.concat([DOS_DAAS, pd.Series([None] * len(DOS_DAAS.columns), index=DOS_DAAS.columns)], ignore_index=True)
            final=pd.concat([df_out2,DOS_DAAS],axis=1)
            DIS_COS=final['Dispositivo COS']
            index_DIS_COS=DIS_COS.index
            index_DIS_COS_list=index_DIS_COS.to_list()
            indice_DIS_COS=index_DIS_COS_list[1]
            UNO = final.loc[indice_DIS_COS, "Dispositivo COS"]           
            first=UNO.find("-")
            second=UNO.find("-",first+1)
            three=UNO.find("-",second+1)
            four=UNO.find("-",three+1)
            UN_COS=UNO[three+1:four]
            #Con el slicing que se realiza toma la columna Dispositivo COS y mira el numero que tiene para que solo tome uno de esos dispositivos
                       
            if final['Dispositivo COS'].str.contains(UN_COS,case=False,na=False,regex=True).any():
                NO_dos_COS=final['Dispositivo COS'].str.contains(UN_COS,case=False,na=False,regex=True)
                self.FINAL_FILTRADO=final[NO_dos_COS]
                self.FINAL_FILTRADO=self.FINAL_FILTRADO.loc[:,['Dispositivo COS','Puerto COS','ptp','Dispositivo DAAS','Puerto DAAS','ptp']]
            else:
                self.FINAL_FILTRADO=final
                self.FINAL_FILTRADO=self.FINAL_FILTRADO.loc[:,['Dispositivo COS','Puerto COS','ptp','Dispositivo DAAS','Puerto DAAS','ptp']]
            #print(self.FINAL_FILTRADO )    
            #final.to_excel("out8.xlsx")
            #self.FINAL_FILTRADO.to_excel("out11.xlsx")##RETORNAR FINAL_FILTRADO PARA LA VISUALIZACION DE LA TABLA DEL DESPUES
            COS=self.FINAL_FILTRADO.loc[:,['Dispositivo COS','Puerto COS','ptp']]
            DAAS=self.FINAL_FILTRADO.loc[:,['Dispositivo DAAS','Puerto DAAS','ptp']]
            #print(COS)
            #print(DAAS)
            diseño(self.filtro,self.FINAL_FILTRADO,variable,filter_daas,self.seleccion_2)            #Da los parametros necesarios para que se realicen los diseños
            return self.filtro,COS,DAAS
            
         except KeyError as e:
              print(e)
              
         except IndexError:
              self.show_not_find()

    def mostrar_tabla(self):
        """
        Esta función crea e inicia tres hilos para ejecutar diferentes métodos.
        -La tabla del antes, llamando a la función crear_tabla 
        -La tabla del despues del COS, llamando a la función crear_despues_COS 
        -La tabla del DAAS, llamando a la función crear_despues_DAAS 
        """
        if self.sch==1:
            try:
                tabla_thread = threading.Thread(target=self.crear_tabla)
                tabla_thread.start()
                despues_DAAS_thread=threading.Thread(target=self.crear_despues_COS)
                despues_DAAS_thread.start()
                despues_COS_thread=threading.Thread(target=self.crear_despues_DAAS)
                despues_COS_thread.start()
            except NameError as e:
                print(e)  
            except ValueError as e:
                 print(e)
        else:
                QMessageBox.warning(self,"Advertencia",
                "Por favor presione primero el botón de buscar archivos",
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)               
    def crear_tabla(self):#*Esta función filtra los datos del Dataframe requeridos y hace la tabla para mostrarla en la interfaz grafica
        """
        Esta función filtra datos de un DataFrame y crea una tabla para mostrarlos en una interfaz gráfica.
        :return: La función no devuelve nada explícitamente, pero puede devolver Ninguno si hay un error.
        """
        #filtro revisa que exista la variable y que no sea ninguna busqueda inexistente
        #x: guarda las columnas del dataframe
        #y: guarda las filas del dataframe
        # Hace dos for concatenados de i, j para ir asignando las filas y columnas al Qtable
        self.variable =""
        try:
            self.variable=self.ui.lineEdit_buscar.text()#*Toma lo que se ingrese en el LineEdit y lo pasa como texto almacenandolo en una variable
            self.variable=self.variable.upper()#*Debido a que todas las letras en la columna esta en mayuscula no importa lo que se digite en el LineEdit, lo transforma a mayuscula para facilitar el filtrado
            filtro,COS,DAAS=self.filtrado_COS_DAAS()        
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

    def crear_despues_COS(self):
        try:
            x,FINAL_DESPUES,DAAS=self.filtrado_COS_DAAS()
            #print(FINAL_DESPUES)
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
    
    def crear_despues_DAAS(self):
        try:
            x,y,DAAS=self.filtrado_COS_DAAS()
            #print(DAAS)
            columnas2=list(DAAS.columns)#*Toma solo las columnas del Dataframe            
            df_fila2=DAAS.to_numpy().tolist()#*lo transforma en una lista para revisar las filas del Dataframe                  
            xx=len(columnas2)#*Toma el tamaño o longitud de la variable para luego recorrerlo en un for              
            yy=len(df_fila2)#*Toma el tamaño o longitud de la variable para luego recorrerlo en un for 
        except ValueError:#*si hay un error de formato de archivo captura el archivo y lo muestra en un MessageBox
            QMessageBox.about (self,'Informacion', 'Formato incorrecto')
            return None
        except FileNotFoundError:#*si hay un error con el archivo, si esta dañado o no corresponde algo, captura el error y lo muestra en un MessageBox
            QMessageBox.about(self,'Informacion', 'El archivo esta \n malogrado')
            return None                         
        self.ui.tabla2.setRowCount(yy)#*inserta en el tableWidget la cantidad de filas que se van a mostrar                        
        self.ui.tabla2.setColumnCount(xx)#*inserta en el tableWidget la cantidad de columnas que se van a mostrar                         
            
        for jj in range(xx):#*Recorre las columnas 
            encabezado2=QtWidgets.QTableWidgetItem(columnas2[jj])#*Guarda los encabezados de cada columna
            self.ui.tabla2.setHorizontalHeaderItem(jj,encabezado2)#*Insterta en la tabla los encabezados guardados anteriormente                               
            for ii in range (yy):#*Recorre las filas
                dato2= str(df_fila2[ii][jj])#*guarda en una lista posicion a posicion de los datos filtrados
                if dato2 == 'nan':#*Revisa si hay algun dato vacio y si es asi colocarlo en blanco
                    dato2=''
                self.ui.tabla2.setItem(ii,jj,QTableWidgetItem(dato2))#*Inserta posicion a posicion en el tableWidget          
    def control_bt_minimizar(self):
        self.showMinimized()#minimiza la ventana del programa.
      
    def control_close(self):
        self.close()#cierra el programa.

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
        self.ad=Ui_ADVERTENCIA()#ad: cuando se presione el botón, llamara a la Clase Ui_ADVERTENCIA.
        self.ad.show()#Muestra en pantalla esa ventana
        
    def cancelar_stop(self):
        #Esta función cancela una parada y restablece ciertas variables.
        # El código anterior es un fragmento de código de Python que establece el valor de algunas variables y
        # crea un nuevo objeto ClientContext. Luego ejecuta una consulta sobre el contexto e imprime el valor
        # de una variable. Finalmente, establece el valor de dos variables más en False y 0 respectivamente.
        # url2 manda una cadena sin sentido como url para que no pueda mandar ninguna petición y detener el envio de datos
        if self.btc_stop==1:#Si se presiona una vez el boton para detener la subida de datos, hasta que no se ejecute de nuevo la subida de datos. no permite presionarse este botón
            self.index_stop=self.saved_index
            self.count3=self.count2
            self.index_saved=True
            url2="adfdsfdsfdsfdsgk"
            self.ctx=ClientContext(url2)
            self.ctx.execute_query()
            #print(self.index_stop)
            self.continuar_subida=False
            self.process=False
            if self.process==False:
                try:              
                    #print(self.process)
                    self.show_popup()   
                except Exception as e:
                    print(e)    
            self.c_up=0
            self.flag=1
            self.btc_stop=2
        else:#Si ya fue presionado una vez el botón durante la ejecución, muestra este mensaje
            QMessageBox.warning(self,"Advertencia",
            f"Por favor intente subir primero los datos nuevamente")   
        
    def seleccion_archivo(self):
        seleccion=self.ui.comboBox.itemText(self.ui.comboBox.currentIndex())#seleccion: Almacena el valor que se seleccione del comboBox
        #print(seleccion)   
        return seleccion
    
    def seleccion_archivo_2(self):
        self.seleccion_2=self.ui.comboBox2.itemText(self.ui.comboBox2.currentIndex())#seleccion_2: Almacena el valor que se seleccione del comboBox
        #print(self.seleccion_2)   
        return self.seleccion_2    

    def download_LISTS(self,pbar):
        #Esta función descarga una lista específica y la guarda en una carpeta específica.
        #LIST_NAME: Extrae del LineEdit el nombre de la lista el cual se va a descargar
        #FILE_NAME: Del nombre que se seleccione del comboBox se guardara una lista con ese nombre
        #De la ruta guardada, se extraera del archivo .env, la ruta en la cual se va a guardar el archivo descargado
        #Crear un hilo para ejecutar los procesos en paralelo de la función de descarga de las listas y la interfaz grafica
        #hay un QMssageBox para saber en que momento finalizo la descarga
        try:
            LIST_NAME=self.ui.lineEdit_descargar_lista.text()
            FILE_NAME=self.seleccion_archivo()
            FOLDER_DEST=env["path_list_download"]
            #print(f"FOLDER_DEST==>{FOLDER_DEST}")
            if FILE_NAME =="Elija nombre del archivo":
                QMessageBox.warning(self,'Advertencia','Por favor escoja un nombre valido',
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
            else:
                ssl._create_default_https_context=ssl._create_unverified_context
                file_name= modules.models.download_lists.Type_file(FILE_NAME,EXPORT_TYPE)
                downloader_thread = threading.Thread(target=modules.models.download_lists.download_list,args=(LIST_NAME,EXPORT_TYPE,FOLDER_DEST,file_name,self.signal_handler))
                downloader_thread.start()
        except PermissionError as e:
                QMessageBox.warning(self,'Error','Ruta no valida',
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
        except requests.exceptions.SSLError as re:
                QMessageBox.warning(self,'Error','Error de servidor, intente la descarga nuevamente',
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)

    def upload_LIST(self):
        #La función crea un hilo para cargar una lista y establece una variable en 1.
        ssl._create_default_https_context=ssl._create_unverified_context
        self.upload_thread = threading.Thread(target=self.subir_list)
        
        self.upload_thread.start()
        self.c_up=1        
        self.process=True
           
    def update_progress_bar(self,progress):
        self.ui.progressBar_2.setValue(progress)

    def obtener_dataframes(self,name_files,ruta_de_busqueda):            
            """    
        :name_files: Una lista de nombres de archivos para buscar en los directorios dados
        :ruta_de_busqueda: Las rutas de directorio donde la función buscará los archivos
        :return: un diccionario de marcos de datos de pandas, donde las claves son una combinación del
        nombre de la hoja (si se proporciona) y el nombre del archivo donde se obtuvo el marco de datos.
            """          
            freeze_support()            
            with concurrent.futures.ThreadPoolExecutor() as executor:    
                rutas_files = list(executor.map(lambda x: self.search.buscar_archivo(*x), [(name_file, ruta) for ruta in ruta_de_busqueda for name_file in name_files]))
                rutas_files=[ruta_file for ruta_file in rutas_files if ruta_file is not None]
            dfs={}
            #print(rutas_files)
            #print(sheet_names)
            for ruta_file,sheet_name in zip(rutas_files,sheet_names):
                #print(ruta_file.name,sheet_name)
                if sheet_name is not None:
                    for sheet_name in sheet_names:
                        df=pd.read_excel(ruta_file,sheet_name=sheet_name,engine='openpyxl')
                        dfs[f"{sheet_name }_{ruta_file.name}"]=df
                else:
                    df=pd.read_excel(ruta_file)
                    dfs[ruta_file.name]=df           
            return dfs
    def read_data(self):
                """
                :return: four variables: arris_df, ocupacion_Daas, ocupacion_Cos, and Casa_df.
                """           
                arris_df=None
                Casa_df=None
                COS_df=None
                DAAS_df=None               
                dataframes=self.obtener_dataframes(name_files,self.ruta_de_busqueda)
                arris_df=dataframes['Arris_SCMSummary.xlsx']
                Casa_df=dataframes['Casa_SCMSummary.xlsx']               
                COS_df=dataframes['Ocupacion-Harmonic_COS.xlsx']
                DAAS_df=dataframes['Ocupacion- RPHY Harmonic_DAAS.xlsx']     
                return arris_df,DAAS_df,COS_df,Casa_df
  
    def search_file_filter(self):
         # Esta función busca archivos en función de un filtro y muestra los resultados en un cuadro de mensaje.
         # El código anterior es un bloque de código de Python que intenta ejecutar un conjunto de
         # instrucciones. Primero obtiene el valor de una variable llamada `old_path_list_download` del
         # entorno, la agrega a una lista llamada `ruta_de_busqueda` y luego imprime el contenido de la lista y
         # los valores de otras cuatro variables. Luego muestra un cuadro de mensaje que indica que la
         # operación se completó con éxito. Si se genera una excepción `KeyError` durante la ejecución del
         # bloque de código, imprime un mensaje de error que indica la causa de la excepción.
         try:
                old_path_list_download = env.get('path_list_download', '')
                self.ruta_de_busqueda.append(old_path_list_download)
                #print(self.ruta_de_busqueda)
                self.file_arris,self.file_despues_DAAS,self.file_despues_COS,self.file_casa=self.read_data()
                self.sch=1
                QMessageBox.information(self,"OPERACION",
                "La operación se ha completado correctamente",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok)
         except KeyError as e:
                print(f"Error:{e}")  

    def subir_list(self):
        self.btc_stop=1
        ssl._create_default_https_context=ssl._create_unverified_context
        self.continuar_subida=True
        self.count2=0
        flagg=1
        index_saved=False
        self.saved_index=0
        c=0
        count=0
        chunksize=1000#Cantidad de datos que va a recorrer del Dataframe, es decir va a coger x cantidad de datos y va a realizar todo el proceso con los datos y luego toam otra x cantidad de datos 
        self.last_index = 0 # índice del último elemento agregado
        commit_count=0
        commit_interval=50#cantidad de datos que manda por cada paquete
        last_saved_index = 0
        max_attempts = 5 #Maxima cantidad de intentos que va a realizar el programa antes de acabarse
        attempt_count = 0
        cout=0
        auth=True
        while auth==True:
            try:
                auth_context = AuthenticationContext(url)
                auth_context.acquire_token_for_user(username, password)
                ssl._create_default_https_context=ssl._create_unverified_context #*Quita la seguridad de número exedido de subida de datos
                self.ctx = ClientContext(url, auth_context)
                self.ctx.clear
                list_title =self.ui.lineEdit_buscar_2.text()##!NOMBRE LISTA
                print(list_title)
                Sp_list = self.ctx.web.lists.get_by_title(list_title)#*Acceder a la lista            
                print(Sp_list)
                self.ctx.load(Sp_list)
                self.ctx.execute_query()
                auth=False
            except:
                c+=1
                print(f"error MFA, reintentando conectar #{c}")
                time.sleep(2)
                continue   
        try:
            excel_file = self.direccion##!PATH
        except AttributeError:
                self.show_error()
        
        data={}
        chunk=0
        item_pro={}   
        print(self.process==True)
        while self.process==True:#Esta condicion solo cambiara cuando se ejecuta la funcion cancelar_stop o termine de enviar los datos
            print("BBBBBBBB")
        # El código verifica si el archivo de Excel de entrada contiene hojas específicas con ciertos
        # encabezados de columna. Si encuentra una hoja con los encabezados requeridos, filtra las columnas,
        # convierte los valores al tipo de cadena y convierte el marco de datos resultante en un diccionario.
        # La variable indicadora se establece en un valor específico según la hoja que se haya encontrado.
            print(("Ocupacion - Marcacion RPHY Harmonic" in excel_file) and ("DAAS" in list_title))      
            if "Arris_SCMSummary" in excel_file:
                        df = pd.read_excel(excel_file)
                        file=pd.DataFrame(df)
                        cont1=0
                        print("a")
                        cabeceras=list(file.columns)
                        headers=['CMTS','S/CG/CH','Mac','Conn','Total','Oper','Disable','Init','Offline','Description']
                        for header in headers:
                            if header in cabeceras:
                                cont1+=1
                                if cont1==9:
                                    file_2=file.loc[:,['CMTS','S/CG/CH','Mac','Conn','Total','Oper','Disable','Init','Offline','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
                                    file_2=file_2.rename(columns={"S/CG/CH":"Up"})
                                    file_2[['Up','Mac','Conn','Total','Oper','Disable','Init','Offline','Description']] = file_2[['Up','Mac','Conn','Total','Oper','Disable','Init','Offline','Description']].astype(str)#*Convierte los valores de estas columnas a tipo str
                                    data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario
                                    flagg=1
            # El código lee un archivo de Excel y verifica si contiene una hoja específica llamada
            # "Casa_SCMSummary". Si la hoja existe, filtra las columnas 'CMTS', 'Upstream', 'Total' y
            # 'Description' de la hoja y reemplaza los valores faltantes con 'Sin datos'. Luego convierte los
            # valores en las columnas 'Upstream', 'Total' y 'Description' en cadenas y convierte el marco de datos
            # filtrado en un diccionario. Finalmente, establece una variable de bandera en 2.
            elif "Casa_SCMSummary" in excel_file :
                        df = pd.read_excel(excel_file)
                        file=pd.DataFrame(df)
                        cont2=0
                        print("b")
                        cabeceras=list(file.columns)
                        headers=['CMTS','Upstream','Total','Active','Registered','Secondary','offline','Bonding','Non_Bonding','Description']
                        for header in headers:
                            if header in cabeceras:
                                cont2+=1
                                if cont2==9:
                                    file_2=file.loc[:,['CMTS','Upstream','Total','Active','Registered','Secondary','Offline','Bonding','Non_Bonding','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
                                    file_2[['Upstream','Total','Active','Registered','Secondary','Offline','Bonding','Non_Bonding','Description']] = file_2[['Upstream','Total','Active','Registered','Secondary','Offline','Bonding','Non_Bonding','Description']].astype(str)#*Convierte los valores de estas columnas a tipo str
                                    data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario 
                                    flagg=2
            elif ("Ocupacion - Marcacion RPHY Harmonic" in excel_file) and ("COS" in list_title)  :
                        df = pd.read_excel(excel_file,sheet_name='Hoja5',engine='openpyxl')
                        file=pd.DataFrame(df)
                        cont4=0
                        print("d")
                        cabeceras=list(file.columns)
                        headers=['IP','Dispositivo','Puerto','moka','status','ptp']
                        for header in headers:
                            if header in cabeceras:
                                cont4+=1
                        if cont4==6:
                            file_2=file.loc[:,['IP','Dispositivo','Puerto','moka','status','ptp']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
                            file_2[['IP','Dispositivo','Puerto','moka','status','ptp']] = file_2[['IP','Dispositivo','Puerto','moka','status','ptp']].astype(str)#*Convierte los valores de estas columnas a tipo str
                            data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario 
                            flagg=4 
            elif ("Ocupacion - Marcacion RPHY Harmonic" in excel_file) and ("DAAS" in list_title) :                       
                        df = pd.read_excel(excel_file,sheet_name='Hoja2',engine='openpyxl')
                        file=pd.DataFrame(df)
                        cont3=0
                        print("c")                    
                        cabeceras=list(file.columns)
                        headers=['IP','Dispositivo','Puerto','status','Unnamed: 4','Unnamed: 5']        
                        for header in headers:
                            if header in cabeceras:
                                cont3+=1
                                if cont3==6:                 
                                    file_2=file.loc[:,['IP','Dispositivo','Puerto','status','Unnamed: 4','Unnamed: 5']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
                                    file_2=file.rename(columns={"Unnamed: 4":"stat2","Unnamed: 5":"ptp"})
                                    file_2[['IP','Dispositivo','Puerto','status','stat2','ptp']] = file_2[['IP','Dispositivo','Puerto','status','stat2','ptp']].astype(str)#*Convierte los valores de estas columnas a tipo str
                                    print(file_2)
                                    data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario 
                                    flagg=3
            # El código anterior es un script de Python que inserta datos en una lista de SharePoint mediante la
            # API REST de SharePoint. Incluye manejo de errores para errores HTTP y otras excepciones que pueden
            # ocurrir durante el proceso de inserción. El código también incluye una barra de progreso para
            # realizar un seguimiento del progreso de la inserción y un intervalo de confirmación para borrar la
            # lista y comenzar un nuevo lote de inserciones después de que se haya agregado una cierta cantidad de
            # elementos. El código también verifica el valor de ciertas variables y realiza diferentes acciones en
            # función de sus valores.

            try:                     
                            print(self.flag==1)
            # El código anterior es un fragmento de código de Python que contiene una declaración if-else.
            # Comprueba el valor de la variable `self.flag` y realiza diferentes acciones en función de su valor.
            # Si `self.flag` es igual a 1, comprueba el valor de otra variable `self.c_up`. Si `self.c_up` es
            # mayor que 1, establece el valor de `self.last_saved_index` en 0 y establece el valor de `count` en
            # 0. Si `self.c_up` no es mayor que 1, establece el valor de `self.last_saved
                            if  self.flag==1:
                                if self.c_up>1:
                                    last_saved_index=0
                                    count=0
                                    print(f"count==>{count}")
                                    print(f"L1==>{last_saved_index}")
                                    self.flag=0
                                else:
                                    last_saved_index=self.index_stop
                                    count=self.count3
                                    print(f"count==>{count}")
                                    print(f"L1==>{last_saved_index}")
                                    self.flag=0
                                    print(self.flag==1)

                            while last_saved_index < len(data): 
                                if  index_saved==False:
                                    self.saved_index=last_saved_index
                                    self.count2=count
                                    
                                chunk=data[last_saved_index:last_saved_index+chunksize]
                                
                                for d in chunk:
            # El código define un diccionario `item_pro` basado en el valor de la variable `flag`. Dependiendo del
            # valor de `bandera`, se agregan diferentes pares clave-valor al diccionario. El valor de `c` se
            # incrementa en 1 y el diccionario `item_pro` resultante se asigna a la variable `item_properties`.
                                    if flagg==1:
                                        #item_pro = {'CMTS': d['CMTS'],'Up':d['Up'],'Mac':d['Mac'],'Conn':d['Conn'],'Total': d['Total'],'Oper':d['Oper'],'Disable':d['Disable'],'Init':d['Init'],'Offline':d['Offline'], 'Description': d['Description']}
                                        item_pro = {'CMTS': d['CMTS'],'Up':d['Up'],'Mac':d['Mac'],'Conn':d['Conn'],'Total': d['Total'],'Oper':d['Oper'],'Disable':d['Disable'],'Init':d['Init'],'Offline':d['Offline'], 'Description': d['Description']}      
                                    elif flagg==2:
                                        item_pro = {'CMTS': d['CMTS'],'Upstream':d['Upstream'],'Total': d['Total'],'Active':d['Active'],'Registered':d['Registered'],'Secondary':d['Secondary'],'offline':d['Offline'],'Bonding':d['Bonding'],'NonBonding':d['Non_Bonding'],'Description': d['Description']}                                
                                    elif flagg==3:
                                        item_pro = {'IP': d['IP'],'Dispositivo':d['Dispositivo'],'Puerto': d['Puerto'],'status':d['status'],'stat2':d['stat2'],'ptp':d['ptp']}  
                                    elif flagg==4:
                                        item_pro = {'IP': d['IP'],'Dispositivo':d['Dispositivo'],'Puerto': d['Puerto'],'moka':d['moka'],'status':d['status'], 'ptp': d['ptp']}      
                                    c=c+1
                                    item_properties=item_pro

                                    for i in range(max_attempts):
            # El código anterior es un bloque de código de Python que intenta agregar elementos a una lista de
            # SharePoint mediante la API REST de SharePoint. Incluye manejo de errores para errores HTTP y otras
            # excepciones que pueden ocurrir durante el proceso de inserción. También incluye un intervalo de
            # compromiso para borrar la lista y comenzar un nuevo lote de inserciones después de que se haya
            # agregado una cierta cantidad de elementos. El código actualiza una barra de progreso a medida que se
            # agregan elementos y muestra mensajes de error mediante un QMessageBox.
                                        try:
                                            ssl._create_default_https_context=ssl._create_unverified_context
                                            item=Sp_list.add_item(item_properties)                            
                                            commit_count += 1
                                            count+=1
                                            progress=int((count/len(data))*100)
                                            self.update_progressBar.emit(progress)
                                           
                                            if commit_count> commit_interval:
                                                print("Valor reestablecido :)")
                                                Sp_list.clear()
                                                commit_count=0
                                            
                                            break  #* Si la inserción es exitosa, salir del ciclo for                                               
                                        except requests.exceptions.HTTPError as http_error:
                                            cout+=1
                                            print(f"Error de HTTP al agregar el elemento #{c}: {http_error}")
                                            time.sleep(5)  #* Esperar 5 segundos antes de intentar de nuevo
                                            continue
                                        except Exception as e:                                        
                                            print(f"Error en el intento {i+1} de inserción para el elemento #{c}: {e}")  
                                            self.count2=count                            
                                            cout+=1
                                            time.sleep(5)  #*Esperar 5 segundos antes de intentar de nuevo
                                            if i == max_attempts - 1: # Si se alcanza el número máximo de intentos sin éxito, salir del programa
                                                print(f"No se pudo agregar el elemento #{c} después de {max_attempts} intentos. Saliendo del programa...")
                                                break
                                                                             
                                    if commit_count==commit_interval:
                                        print("h")
                                        self.ctx.execute_batch()                                                  
                                        print("Se realizo Commit")
                                        ssl._create_default_https_context=ssl._create_unverified_context
                                        print(f"El último ID guardado en la lista es: {last_saved_index}")                                   
                                        Sp_list.clear()
                                        commit_count=0
                                                                                       
                                if commit_count> commit_interval:
                                    print("Valor reestablecido :)")
                                    Sp_list.clear()
                                    commit_count=0 
                                last_saved_index = last_saved_index+len(chunk)                                
                                print(c)
                                if commit_count % commit_interval != 0:             
                                    self.ctx.execute_batch()
                                    print("Se realizo Commit2")
                                    count=0
                                    self.process=False
                                    print(last_saved_index)
                                    
                                    Sp_list.clear()
                                    commit_count=0

                            self.last_saved_index2 = last_saved_index+len(chunk)
                            
                            if commit_count> 0:
                                self.ctx.execute_batch()
                                print("commit final :)")
                                Sp_list.clear()
                                self.process=False
                                commit_count=0  
                            
            except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                            print("No hay conexión a internet. Esperando...")
                            cout+=1
                            time.sleep(5)  # Esperar 5 segundos antes de volver a intentar
                            self.count2=count
                            continue # Volver al inicio del bucle while
            except Exception as e:
                            attempt_count += 1                       
                            print(f"Error al Agregar el elemento a la lista #{c} error: {e}")
                            print("Reintentando en 5 segundo...")
                            cout+=1
                            self.count2=count
                            time.sleep(5)
                            if cout == 5:#Si la execepcion ocuure 5 veces va a a terminar la subida de archivos
                                print("Se han excedido el número máximo de intentos. Saliendo del programa...")
                                self.cancelar_stop()
                            else:
                                continue
                            continue
                            continue
                                       
    def save_path_list(self):
        #Revisa que el nombre del archivo en el LineEdit no este vacio y si es asi lo guarde como ya estaba guardado
        # y si tiene algo nuevo lo guarde en el archivo y lo tome como la nueva ruta
        path_list = self.ui.lineEdit_Path_lists.text()
        old_path_list_download = env.get('path_list_download', '')# Obtenemos el valor anterior de path_list_download del archivo .env
        print(f"path_list==>{path_list}")
        if path_list=='':
            print("a")
            new_path_list_download = old_path_list_download
            self.ui.lineEdit_Path_lists.setText('')
            self.ruta_de_busqueda.append(old_path_list_download)            
        else:
            print("b")
            new_path_list_download = path_list + "\\descarga"
            self.ui.lineEdit_Path_lists.setText('')
            self.ruta_de_busqueda.append(path_list)  
        print(f"new_path_list_download==>{new_path_list_download}")
        set_key(".env", "path_list_download", new_path_list_download)
        print(set_key(".env", "path_list_download", new_path_list_download))
        self.FOLDER_DEST=new_path_list_download
        ruta_nueva_carpeta = new_path_list_download + "/Diseños_NODOS" 
        set_key(".env", "path_files_upload", ruta_nueva_carpeta)
        print(f"s_files==>{self.ruta_de_busqueda}")
        print(f"FOLDER_DEST==>{self.FOLDER_DEST}")
        QMessageBox.information(self,"GUARDADO",
        "Se ha guardado correctamente, por favor reinicie la aplicación",
        QMessageBox.StandardButton.Ok,
        QMessageBox.StandardButton.Ok)        
    def save_parameters_url_sharepoint(self):
        #Revisa que el nombre del archivo en el LineEdit no este vacio y si es asi lo guarde como ya estaba guardado
        # y si tiene algo nuevo lo guarde en el archivo y lo tome como la nueva ruta
        path_Sharepoint=self.ui.lineEdit_site_Sharepoint.text()
        old_path_path_sharepoint = env.get('sharepoint_url_site', '')
        if path_Sharepoint=='':
            print("a")
            new_path_Sharepoint = old_path_path_sharepoint
            self.ui.lineEdit_site_Sharepoint.setText('')           
        else:
            print("b")
            new_path_Sharepoint = path_Sharepoint 
            self.ui.lineEdit_site_Sharepoint.setText('')
        print(f"path_SHAREPOINT==>{new_path_Sharepoint}")    
        set_key(".env","sharepoint_url_site",new_path_Sharepoint)
        S_path_share=new_path_Sharepoint.find("/")
        Sl_path_share=new_path_Sharepoint.find("/",S_path_share+1)
        SLI_path_share=new_path_Sharepoint.find("/",Sl_path_share+1)
        SLIC_path_share=new_path_Sharepoint.find("/",SLI_path_share+1)
        site_name=new_path_Sharepoint[SLIC_path_share+1:-1]
        print(site_name)
        set_key(".env","sharepoint_site_name",site_name)

    def save_parameters_name_folder_Sharepoint(self):
        #Revisa que el nombre del archivo en el LineEdit no este vacio y si es asi lo guarde como ya estaba guardado
        # y si tiene algo nuevo lo guarde en el archivo y lo tome como la nueva ruta
        folder_Sharepoint=self.ui.lineEdit_folder_subir_archivo.text()
        old_path_name_folder=env.get('sharepoint_name_folder', '')
        if folder_Sharepoint=='':
            print("a")
            new_path_folder_name = old_path_name_folder
            self.ui.lineEdit_folder_subir_archivo.setText('')      
        else:
            print("b")
            new_path_folder_name = folder_Sharepoint 
            self.ui.lineEdit_folder_subir_archivo.setText('')
        print(f"name_folder_Sharepoint==>{new_path_folder_name}")    
        set_key(".env","sharepoint_name_folder",new_path_folder_name)   
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    mi_app=MiApp()
    mi_app.show()
    sys.exit(app.exec_())
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
#from dotenv import set_key,dotenv_values
import os
from pathlib import Path
from multiprocessing import Pool,cpu_count,freeze_support
import numpy as np
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
#env=dotenv_values(".env")
'''username = "juan.hurtado02@usa.edu.co"
password = "Mono9100."
url = "https://universidadsergioarboleda.sharepoint.com/sites/devs/"'''
url = "https://claromovilco.sharepoint.com/sites/Prueba35/"
username = "juan.hurtado@claro.com.co"
password = "JUEhp$9_23"
"""
        Esta función carga datos de un archivo de Excel a una lista de SharePoint, maneja interrupciones y
        desconexiones y vuelve a intentar intentos fallidos.
"""
process=True
continuar_subida=True
count2=0
flag=1
index_saved=False
saved_index=0
c=0
count=0
chunksize=1000#Cantidad de datos que va a recorrer del Dataframe, es decir va a coger x cantidad de datos y va a realizar todo el proceso con los datos y luego toam otra x cantidad de datos 
last_index = 0 # índice del último elemento agregado
commit_count=0
commit_interval=50#cantidad de datos que manda por cada paquete
        # Manejar interrupciones y desconexiones, guardar el índice del último elemento agregado antes de la interrupción o desconexión
        #######################################################################################
last_saved_index = 0
max_attempts = 5 #Maxima cantidad de intentos que va a realizar el programa antes de acabarse
attempt_count = 0
total_items=0
#auth_context = AuthenticationContext(url)
#auth_context.acquire_token_for_user(username, password)
ssl._create_default_https_context=ssl._create_unverified_context
'''ctx=ClientContext(url).with_credentials(
            UserCredential(
                username,
                password
            )
        )'''
auth_context = AuthenticationContext(url)
auth_context.acquire_token_for_user(username, password)
ctx = ClientContext(url, auth_context)
        #############################################################################
#ssl._create_default_https_context=ssl._create_unverified_context #*Quita la seguridad de número exedido de subida de datos
#ctx = ClientContext(url).with_credentials(UserCredential(username,password))
ctx.clear
        #############################################################################
list_title ="Lista_COS2"##!NOMBRE LISTA
#!
##!Lista_arris
##!Lista_Casa
##!Lista_Cos
##!Lista_COS2
#*P_P
#*Lista_Daas
print(list_title)
Sp_list = ctx.web.lists.get_by_title(list_title)#*Acceder a la lista
      
print(Sp_list)
ctx.load(Sp_list)
ctx.execute_query()
excel_file = "descarga/Arris_SCMSummary.xlsx"##!PATH
data={}
chunk=0
while process==True:
# El código verifica si el archivo de Excel de entrada contiene hojas específicas con ciertos
# encabezados de columna. Si encuentra una hoja con los encabezados requeridos, filtra las columnas,
# convierte los valores al tipo de cadena y convierte el marco de datos resultante en un diccionario.
# La variable indicadora se establece en un valor específico según la hoja que se haya encontrado.
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
                            flag=1
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
                headers=['CMTS','Upstream','Total','Active','Registered','Secondary','Offline','Bonding','Non_Bonding','Description']
                for header in headers:
                    if header in cabeceras:
                        cont2+=1
                        if cont2==9:
                            file_2=file.loc[:,['CMTS','Upstream','Total','Active','Registered','Secondary','Offline','Bonding','Non_Bonding','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
                            #file_2=file.loc[:,['CMTS','Upstream','Total','Active','Registered','Secondary','offline','Bonding','NonBonding','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
                            file_2[['Upstream','Total','Active','Registered','Secondary','Offline','Bonding','Non_Bonding','Description']] = file_2[['Upstream','Total','Active','Registered','Secondary','Offline','Bonding','Non_Bonding','Description']].astype(str)#*Convierte los valores de estas columnas a tipo str
                            #file_2[['Upstream','Total','Description','Active','Registered','Secondary','offline','Bonding','NonBonding']] = file_2[['Upstream','Total','Description','Active','Registered','Secondary','offline','Bonding','NonBonding']].astype(str)#*Convierte los valores de estas columnas a tipo str
                            data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario 
                            flag=2
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
                    print(cont4)
                    file_2=file.loc[:,['IP','Dispositivo','Puerto','moka','status','ptp']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
                    file_2[['IP','Dispositivo','Puerto','moka','status','ptp']] = file_2[['IP','Dispositivo','Puerto','moka','status','ptp']].astype(str)#*Convierte los valores de estas columnas a tipo str
                    data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario 
                    flag=4 
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
                            flag=3


    # El código anterior es un script de Python que inserta datos en una lista de SharePoint mediante la
    # API REST de SharePoint. Incluye manejo de errores para errores HTTP y otras excepciones que pueden
    # ocurrir durante el proceso de inserción. El código también incluye una barra de progreso para
    # realizar un seguimiento del progreso de la inserción y un intervalo de confirmación para borrar la
    # lista y comenzar un nuevo lote de inserciones después de que se haya agregado una cierta cantidad de
    # elementos. El código también verifica el valor de ciertas variables y realiza diferentes acciones en
    # función de sus valores.

    try:    
                    print(flag==1)
    # El código anterior es un fragmento de código de Python que contiene una declaración if-else.
    # Comprueba el valor de la variable `self.flag` y realiza diferentes acciones en función de su valor.
    # Si `self.flag` es igual a 1, comprueba el valor de otra variable `self.c_up`. Si `self.c_up` es
    # mayor que 1, establece el valor de `self.last_saved_index` en 0 y establece el valor de `count` en
    # 0. Si `self.c_up` no es mayor que 1, establece el valor de `self.last_saved
                    '''if  flag==1:
                        if c_up>1:
                            last_saved_index=0
                            count=0
                            print(f"count==>{count}")
                            print(f"L1==>{last_saved_index}")
                            flag=0
                        else:
                            last_saved_index=index_stop
                            count=count3
                            print(f"count==>{count}")
                            print(f"L1==>{last_saved_index}")
                            flag=0
                            print(flag==1)'''

                    while last_saved_index < len(data): 
                        
                        if  index_saved==False:
                            saved_index=last_saved_index
                            count2=count
                            
                        chunk=data[last_saved_index:last_saved_index+chunksize]
                        
                        for d in chunk:
    # El código define un diccionario `item_pro` basado en el valor de la variable `flag`. Dependiendo del
    # valor de `bandera`, se agregan diferentes pares clave-valor al diccionario. El valor de `c` se
    # incrementa en 1 y el diccionario `item_pro` resultante se asigna a la variable `item_properties`.
                            if flag==1:
                                item_pro = {'CMTS': d['CMTS'],'Up':d['Up'],'Mac':d['Mac'],'Conn':d['Conn'],'Total': d['Total'],'Oper':d['Oper'],'Disable':d['Disable'],'Init':d['Init'],'Offline':d['Offline'], 'Description': d['Description']}     
                            elif flag==2:
                                item_pro = {'CMTS': d['CMTS'],'Upstream':d['Upstream'],'Total': d['Total'],'Active':d['Active'],'Registered':d['Registered'],'Secondary':d['Secondary'],'offline':d['Offline'],'Bonding':d['Bonding'],'NonBonding':d['Non_Bonding'],'Description': d['Description']}                              
                                #item_pro = {'CMTS': d['CMTS'],'Upstream':d['Upstream'],'Total': d['Total'],'Active':d['Active'],'Registered':d['Registered'],'Secondary':d['Secondary'],'offline':d['offline'],'Bonding':d['Bonding'],'NonBonding':d['Non_Bonding'], 'Description': d['Description']}  
                            elif flag==3:
                                item_pro = {'IP': d['IP'],'Dispositivo':d['Dispositivo'],'Puerto': d['Puerto'],'status':d['status'],'stat2':d['stat2'],'ptp':d['ptp']}  
                            elif flag==4:
                                item_pro = {'IP': d['IP'],'Dispositivo':d['Dispositivo'],'Puerto': d['Puerto'],'moka':d['moka'],'status':d['status'], 'ptp': d['ptp'],}      
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
                                    item=Sp_list.add_item(item_properties)
                                    
                                    commit_count += 1
                                    count+=1
                                    progress=int((count/len(data))*100)
                                    #update_progressBar.emit(progress)

                                    
                                    if commit_count> commit_interval:
                                        print("Valor reestablecido :)")
                                        Sp_list.clear()
                                        commit_count=0
                                    
                                    break  #* Si la inserción es exitosa, salir del ciclo for
                                        
                                except requests.exceptions.HTTPError as http_error:
                                    
                                    print(f"Error de HTTP al agregar el elemento #{c}: {http_error}")
                                    time.sleep(5)  #* Esperar 5 segundos antes de intentar de nuevo
                                    count=last_saved_index
                                except Exception as e:
                                    
                                    print(f"Error en el intento {i+1} de inserción para el elemento #{c}: {e}")                              
                                    time.sleep(5)  #*Esperar 5 segundos antes de intentar de nuevo
                                    if i == max_attempts - 1:
                                        # Si se alcanza el número máximo de intentos sin éxito, salir del programa
                                        print(f"No se pudo agregar el elemento #{c} después de {max_attempts} intentos. Saliendo del programa...")
                                        break
                                        
                            
                            if commit_count==commit_interval:
                                print("h")
                                ctx.execute_batch()       
                                    
                                print("Se realizo Commit")
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
                            ctx.execute_batch()
                            print("Se realizo Commit2")
                            count=0
                            process=False
                            print(last_saved_index)
                            
                            Sp_list.clear()
                            commit_count=0
                        
                    last_saved_index2 = last_saved_index+len(chunk)
                    
                    if commit_count> 0:
                        ctx.execute_batch()
                        print("commit final :)")
                        Sp_list.clear()
                        process=False
                        commit_count=0  
                    
    except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                    print("No hay conexión a internet. Esperando...")
                    time.sleep(5)  # Esperar 5 segundos antes de volver a intentar
                    
                    continue # Volver al inicio del bucle while
    except Exception as e:

                    attempt_count += 1
                
                    print(f"Error al Agregar el elemento a la lista #{c} error: {e}")
                    print("Reintentando en 5 segundo...")
                    time.sleep(5)
                    continue
                    if attempt_count >= max_attempts:
                        print("Se han excedido el número máximo de intentos. Saliendo del programa...")
                    
                    continue
                    
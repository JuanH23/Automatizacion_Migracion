#*Librerias utilizadas en el programa
from office365.sharepoint.lists.template_type import ListTemplateType
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files import file
from office365.sharepoint.lists.creation_information import ListCreationInformation
from office365.runtime.auth.user_credential import UserCredential 
from office365.sharepoint.lists.list import List   
from office365.sharepoint.listitems.collection import ListItemCollection

import pandas as pd
import time
import ssl
import requests
import json
from dotenv import set_key,dotenv_values
#*Autenticacion para poder acceder al Sharepoint
env=dotenv_values(".env")
username = "juan.hurtado@claro.com.co"
password ="JUEhp$9_23" 
url = 'https://claromovilco.sharepoint.com/sites/Prueba35'

auth_context = AuthenticationContext(url)
auth_context.acquire_token_for_user(username, password)
#ctx = ClientContext(url, auth_context)
#############################################################################
ssl._create_default_https_context=ssl._create_unverified_context #*Quita la seguridad de número exedido de subida de datos
ctx = ClientContext(url).with_credentials(UserCredential(username,password))
#############################################################################

list_title = "Lista_Casa"
Sp_list = ctx.web.lists.get_by_title(list_title)#*Acceder a la lista

print(Sp_list)
ctx.load(Sp_list)
ctx.execute_query()



################CREAR LISTA#####################
#list_title = "listas"
#list_description = "Descripción de la lista"
#list_template = ListTemplateType.GenericList
#list_creation_info = ListCreationInformation(list_title, list_description, list_template)
#ctx.web.lists.add(list_creation_info)
#ctx.execute_query()
#################################################

#######################################################################################

excel_file = "Descargas/Casa_SCMSummary.xlsx"
if "arris" in list_title :
    df = pd.read_excel(excel_file)
    file=pd.DataFrame(df)
    file_2=file.loc[:,['CMTS','Mac','Total','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
    file_2[['Mac','Total','Description']] = file_2[['Mac','Total','Description']].astype(str)#*Convierte los valores de estas columnas a tipo str
    data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario
    flag=1
elif "Casa" in list_title :
    df = pd.read_excel(excel_file)
    file=pd.DataFrame(df)
    file_2=file.loc[:,['CMTS','Upstream','Total','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
    file_2[['Upstream','Total','Description']] = file_2[['Upstream','Total','Description']].astype(str)#*Convierte los valores de estas columnas a tipo str
    data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario 
    flag=2
elif "Daas" in list_title :
    df = pd.read_excel(excel_file,sheet_name='Hoja2',engine='openpyxl')
    file=pd.DataFrame(df)
    file_2=file.loc[:,['IP','Dispositivo','Puerto','Unnamed: 5']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
    file_2[['IP','Dispositivo','Puerto','Unnamed: 5']] = file_2[['IP','Dispositivo','Puerto','Unnamed: 5']].astype(str)#*Convierte los valores de estas columnas a tipo str
    data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario 
    flag=3
elif "Cos" in list_title :
    df = pd.read_excel(excel_file,sheet_name='Hoja5',engine='openpyxl')
    file=pd.DataFrame(df)
    file_2=file.loc[:,['IP','Dispositivo','Puerto','ptp']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
    file_2[['IP','Dispositivo','Puerto','ptp']] = file_2[['IP','Dispositivo','Puerto','ptp']].astype(str)#*Convierte los valores de estas columnas a tipo str
    data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario 
    flag=4              
c=0
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

#######################################################################################




try:    
        
        while last_saved_index < len(data): 
            chunk=data[last_saved_index:last_saved_index+chunksize]
            

            for d in chunk:
                if flag==1:
                    item_pro = {'CMTS': d['CMTS'],'Mac':d['Mac'],'Total': d['Total'], 'Description': d['Description']}     
                elif flag==2:
                    item_pro = {'CMTS': d['CMTS'],'Upstream':d['Upstream'],'Total': d['Total'], 'Description': d['Description']}    
                elif flag==3:
                    item_pro = {'IP': d['IP'],'Dispositivo':d['Dispositivo'],'Puerto': d['Puerto'], 'Unnamed: 5': d['Unnamed: 5']}  
                elif flag==4:
                    item_pro = {'IP': d['IP'],'Dispositivo':d['Dispositivo'],'Puerto': d['Puerto'], 'ptp': d['ptp']}      
                c=c+1
                item_properties=item_pro
                
                for i in range(max_attempts):
                    try:
                        item=Sp_list.add_item(item_properties)
                        
                        commit_count += 1

                            
                        if commit_count> commit_interval:
                            print("Valor reestablecido :)")
                            Sp_list.clear()
                            commit_count=0
  
                        break  #* Si la inserción es exitosa, salir del ciclo for

                    except requests.exceptions.HTTPError as http_error:
                        
                        print(f"Error de HTTP al agregar el elemento #{c}: {http_error}")
                        time.sleep(5)  #* Esperar 5 segundos antes de intentar de nuevo
                    except Exception as e:
                        
                        print(f"Error en el intento {i+1} de inserción para el elemento #{c}: {e}")
                        time.sleep(5)  #*Esperar 5 segundos antes de intentar de nuevo
                        if i == max_attempts - 1:
                            # Si se alcanza el número máximo de intentos sin éxito, salir del programa
                            print(f"No se pudo agregar el elemento #{c} después de {max_attempts} intentos. Saliendo del programa...")
                            break

                
                if commit_count==commit_interval:
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
                Sp_list.clear()
                commit_count=0


        if commit_count> 0:
            ctx.execute_batch()
            print("commit final :)")
            Sp_list.clear()
            commit_count=0  

        


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
    


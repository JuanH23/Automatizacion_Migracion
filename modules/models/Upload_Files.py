from modules.models.office365_api import SharePoint
import re
import sys,os
from pathlib import PurePath
from dotenv import set_key,dotenv_values
from dotenv import load_dotenv
import time
load_dotenv()
#Ruta a donde se va a subir
#Path de computador de desde donde se va a subir el archivo
ROOT_DIR=""
#Nombre del archivo, incluye subfolders para subir
#Ruta de SharePoint a donde se va a subir 
env=dotenv_values(".env")
SHAREPOINT_FOLDER__NAME=env["sharepoint_name_folder"]
#archivo nombre pattern, si se quiere subir un archivo en especifico colocar en ese parametro el nombre sin extension
FILE_NAME_PATTERN='None'

def upload_files(folder,keyword=None):
    """  
    folder: La ruta de la carpeta donde se encuentran los archivos que se cargarán
    keyword: El parámetro de palabra clave es un argumento opcional que se puede usar para
    """
# Este código define una función llamada `upload_files` que toma dos parámetros: `carpeta` y `palabra
# clave`.
    c=0
    cfiles=0
    file_list=get_list_of_files(folder)
    while cfiles != len(file_list):
        for file in file_list:
            if keyword is None or keyword == 'None' or re.search(keyword,file[0]):
                file_content=get_file_content(file[1])
                
                print(f"count==>{cfiles}")
                print(f"len(file_list)==>{len(file_list)}")
                try:              
                        SharePoint().upload_file(file[0],SHAREPOINT_FOLDER__NAME,file_content)   
                        print("ARCHIVOS SUBIDOS")
                        cfiles+=1
                        if cfiles == len(file_list):
                             break
                except:
                        c+=1
                        print(f"error MFA, reintentando conectar #{c}")
                        time.sleep(2)
                        continue 
                        
def get_list_of_files(folder):
    """
    :folder: El parámetro "carpeta" es una cadena que representa la ruta a un directorio
    :return: La función `get_list_of_files` devuelve una lista de listas, donde cada lista interna
    contiene el nombre y la ruta completa de un archivo en la carpeta especificada.
    """
    file_list=[]
    folder_item_list=os.listdir(folder)
    for item in folder_item_list:
        item_full_path=PurePath(folder,item)
        if os.path.isfile(item_full_path):
            file_list.append([item,item_full_path])
    return file_list
        

def get_file_content(file_path):#Lectura de archivos y regresa el contenido de los archivos
    """   
    :file_path: El parámetro de la ruta del archivo es una cadena que representa la ubicación del
    archivo que debe leerse. Puede ser una ruta absoluta o relativa al archivo
    :return: el contenido del archivo ubicado en la ruta de archivo especificada como un objeto de
    bytes.
    """
    with open(file_path,'rb')as f:
        return f.read()
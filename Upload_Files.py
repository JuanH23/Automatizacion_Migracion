from office365_api import SharePoint
import re
import sys,os
from pathlib import PurePath
#Ruta a donde se va a subir
#ROOT_DIR=sys.argv[1]#Path de computador de desde donde se va a subir el archivo
ROOT_DIR=""
#Nombre del archivo, incluye subfolders para subir
#SHAREPOINT_FOLDER__NAME=sys.argv[2]#Ruta de SharePoint a donde se va a subir 
SHAREPOINT_FOLDER__NAME="PRUEBA_STORAGE"
#archivo nombre pattern, si se quiere subir un archivo en especifico colocar en ese parametro el nombre sin extension
#FILE_NAME_PATTERN=sys.argv[3]
FILE_NAME_PATTERN='None'

def upload_files(folder,keyword=None):
    file_list=get_list_of_files(folder)
    for file in file_list:
        if keyword is None or keyword == 'None' or re.search(keyword,file[0]):
            file_content=get_file_content(file[1])
            SharePoint().upload_file(file[0],SHAREPOINT_FOLDER__NAME,file_content)    


def get_list_of_files(folder):
    file_list=[]
    folder_item_list=os.listdir(folder)
    for item in folder_item_list:
        item_full_path=PurePath(folder,item)
        if os.path.isfile(item_full_path):
            file_list.append([item,item_full_path])
    return file_list
        
#Lectura de archivos y regresa el contenido de los archivos
def get_file_content(file_path):
    with open(file_path,'rb')as f:
        return f.read()
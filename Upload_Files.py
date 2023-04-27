from office365_api import SharePoint
import re
import sys,os
from pathlib import PurePath
from dotenv import set_key,dotenv_values
#Ruta a donde se va a subir
#ROOT_DIR=sys.argv[1]#Path de computador de desde donde se va a subir el archivo
ROOT_DIR=""
#Nombre del archivo, incluye subfolders para subir
#SHAREPOINT_FOLDER__NAME=sys.argv[2]#Ruta de SharePoint a donde se va a subir 
env=dotenv_values(".env")
ROOT_DIR="C:\\Users\IC0167A\Desktop\Proyecto_final\prueba_s"#!CONFIGURAR PATH DEL PC DE DONDE SE VAN A SUBIR LOS ARCHIVOS, UNA VEZ TERMINADO LOS DISEÑOS
SHAREPOINT_FOLDER__NAME=env["sharepoint_name_folder"]
#archivo nombre pattern, si se quiere subir un archivo en especifico colocar en ese parametro el nombre sin extension
#FILE_NAME_PATTERN=sys.argv[3]
FILE_NAME_PATTERN='None'

def upload_files(folder,keyword=None):
    """
    Esta función carga archivos en una carpeta de SharePoint en función de una palabra clave específica
    o de todos los archivos de una carpeta.
    
    :param folder: La ruta de la carpeta donde se encuentran los archivos que se cargarán
    :param keyword: El parámetro de palabra clave es un argumento opcional que se puede usar para
    filtrar los archivos que se cargan en función de una palabra clave específica. Si se proporciona una
    palabra clave, solo se cargarán los archivos que contengan la palabra clave en su nombre de archivo.
    Si no se proporciona ninguna palabra clave o si la palabra clave se establece en 'Ninguna', todos
    los archivos
    """
# Este código define una función llamada `upload_files` que toma dos parámetros: `carpeta` y `palabra
# clave`.
    file_list=get_list_of_files(folder)
    for file in file_list:
        if keyword is None or keyword == 'None' or re.search(keyword,file[0]):
            file_content=get_file_content(file[1])
            SharePoint().upload_file(file[0],SHAREPOINT_FOLDER__NAME,file_content)    


def get_list_of_files(folder):
    """
    Esta función toma la ruta de una carpeta como entrada y devuelve una lista de archivos dentro de esa
    carpeta junto con sus rutas completas.
    
    :param folder: El parámetro "carpeta" es una cadena que representa la ruta a un directorio
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
        
#Lectura de archivos y regresa el contenido de los archivos
def get_file_content(file_path):
    """
    Esta función lee el contenido de un archivo en modo binario y lo devuelve.
    
    :param file_path: El parámetro de la ruta del archivo es una cadena que representa la ubicación del
    archivo que debe leerse. Puede ser una ruta absoluta o relativa al archivo
    :return: el contenido del archivo ubicado en la ruta de archivo especificada como un objeto de
    bytes.
    """
    with open(file_path,'rb')as f:
        return f.read()
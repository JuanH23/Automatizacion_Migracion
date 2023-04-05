from office365_api import SharePoint
import sys
import csv
from pathlib import PurePath
from pathlib import Path
from openpyxl import Workbook
import pandas as pd
import time
import threading
import os
import ssl
#Nombre de la lista la cual se va a descargar
'''LIST_NAME=sys.argv[1]
#Tipo de archivo el cual se va a descargar "Ya sea excel ó csv"
EXPORT_TYPE=sys.argv[2]
#A que lugar del computador se va a guardar el archivo
FOLDER_DEST=sys.argv[3]
#Nombre del archivo al querer descargar solo uno 
FILE_NAME=sys.argv[4]
'''


def Type_file(file_name,export_type):
    if export_type == 'Excel':
        file_name_export='.'.join([file_name,'xlsx']) 
    elif export_type == 'CSV':
        file_name_export='.'.join([file_name,'csv'])
    else:
        file_name_export=file_name
    return file_name_export


def download_list(list_name,export_type,dir_path,file_name):
    
    sp_list=SharePoint().get_list(list_name)

    if export_type == 'Excel':
        
        file=threading.Thread(target= save_Execel(sp_list,dir_path,file_name))
        file.start()
    elif export_type =='CSV':
        save_file_csv(sp_list,dir_path,file_name)
    else:
        print("No se puede Descargar ese tipo de archivo")
    
    
    

def save_file_csv(list_items,dir_path,file_name):
    dir_file_path=PurePath(dir_path,file_name)
    with open (dir_file_path,'w',newline='\n',encoding='utf8') as f:
        header=list_items[0].properties.keys()
        w=csv.DictWriter(f,header)
        w.writeheader()
        for item in list_items:
            w.writerow(item.properties)


def save_Execel(list_items,dir_path,file_name):
    ssl._create_default_https_context=ssl._create_unverified_context
    dir_file_path=Path(dir_path,file_name).with_suffix('.xlsx')
    # dir_file_path=PurePath(dir_path,file_name)
    wb= Workbook()
    ws=wb.active
    #Obtiene las cabeceras de la lista
    header=list_items[0].properties.keys()
    #Escribe las columnas en la primera fila
    for idx,name in enumerate(header):
        ws.cell(row=1, column=idx+1,value=name)
    #Comienza a escribir los items desde la segunda fila
    row=2
    for dict_obj in list_items:
        for idx, item in enumerate(dict_obj.properties.items()):
            ws.cell(row=row,column=idx+1,value=item[1])
        row+=1
    dir_path=Path(dir_path)
    dir_path.mkdir(parents=True,exist_ok=True)
    wb.save(dir_file_path)


if __name__ =='__main__':
    pass

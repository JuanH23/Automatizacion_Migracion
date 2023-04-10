import pandas as pd
import os
from pathlib import Path
from multiprocessing import Pool,cpu_count,freeze_support
import numpy as np
name_files=["Arris_SCMSummary.xlsx","Casa_SCMSummary.xlsx","Ocupacion - Marcacion RPHY Harmonic.xlsx"]
ruta_de_busqueda=['C:\\Users\\pc\\Automatizacion_Migracion\\Documents','C\\Users']
sheet_names=[None,None,'Hoja2','Hoja5']

def buscar_archivo(name_file,ruta):
    for root,dirs, files in os.walk(ruta):
        for file in files:
            if file.endswith('.xlsx') and file==name_file:
                return Path(root)/file
            
def obtener_dataframes(name_files,ruta_de_busqueda):            
    if __name__=='__main__':
        freeze_support()       
        with Pool(processes=os.cpu_count()) as pool:
            rutas_files=pool.starmap(buscar_archivo,[(name_file,ruta) for ruta in ruta_de_busqueda for name_file in name_files])
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
    #print(dfs["Arris_SCMSummary.xlsx"])
def read_data():
    arris_df=None
    ocupacion_Cos=None
    ocupacion_Daas=None
    Casa_df=None
    if __name__=='__main__':  
        dataframes=obtener_dataframes(name_files,ruta_de_busqueda)
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
file_arris,file_despues_DAAS,file_despues_COS,file_casa=read_data()

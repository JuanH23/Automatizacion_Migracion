import pandas as pd
import os
from pathlib import Path
from multiprocessing import Pool,cpu_count,freeze_support
import numpy as np
name_files=["Arris_SCMSummary.xlsx","Casa_SCMSummary.xlsx","Ocupacion - Marcacion RPHY Harmonic.xlsx"]
ruta_de_busqueda=['C:\\Users\\IC0167A\\Desktop\\Documents','C\\Users']
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
#!Tarda 1:20 segundos en encontrar dos archivos dentro del PC
#########################################################################################
def complet_COS(df):
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


def complete_DAAS(df):
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
        for puerto in valores_faltantes[valores_faltantes <= 48]:
            puerto_str = 'xe-0/0/' + str(puerto)
            ip = df[df['Dispositivo'] == dispositivo]['IP'].iloc[0]
            ocupacion = df[df['Dispositivo'] == dispositivo]['Unnamed: 5'].iloc[0]
            nuevas_filas.append((ip, dispositivo, puerto_str, np.nan, np.nan, "PUERTOLIBRE"))
    nuevas_filas_df = pd.DataFrame(nuevas_filas, columns=df.columns)

    # Concatenar DataFrame original con nuevas filas y ordenar por dispositivo y puerto
    df = pd.concat([df, nuevas_filas_df]).sort_values(['Dispositivo', 'Puerto']).reset_index(drop=True)
    df=df.drop_duplicates()
    return df
#########################################################################################
#path="data/Arris_SCMSummary.xlsx"
#file=pd.read_excel(dfs["Arris_SCMSummary.xlsx"])
try:
    df=pd.DataFrame(file_arris)
    df_casa=pd.DataFrame(file_casa)
    df_casa=df_casa.loc[:,['CMTS','Upstream','Total','Description']]
    df_casa=df_casa.rename(columns={'Upstream':'S'})
    file_2=df.loc[:,['CMTS','Mac','Total','Description']]
    file_2[['Mac','Total','Description']] = file_2[['Mac','Total','Description']].astype(str)
    #print(file_2)
    df_concat = pd.concat([file_2, df_casa])
    print(df_concat)
    variable="1is1"
    variable=variable.upper()#*Debido a que todas las letras en la columna esta en mayuscula no importa lo que se digite en el LineEdit, lo transforma a mayuscula para facilitar el filtrado
    filtro=df_concat[df_concat['Description'].str.contains(variable,case=False,na=False,regex=True)]#*con el argumento contains revisa lo que se guarde en la varible,filtre y en la variable filtro guarde todo.
    print(filtro)
    ciudad=filtro['CMTS']
    #print(ciudad)
    valor=ciudad.index
    valor_list=valor.to_list()
    indice=valor_list[1]
    v = filtro.loc[indice, "CMTS"]

    print(v)
    sep=v.find("-")
    sep2=v.find("-",sep+1)
    variable3=v[:sep2]
    print(variable3)


    df2=pd.DataFrame(file_despues_DAAS)
    print(df2)
    df_das=complete_DAAS(df2)
    #print(df2)
    file_3=df_das.loc[:,['IP','Dispositivo','Puerto','status','Unnamed: 4','Unnamed: 5']].astype(str).fillna(value='No Data')
    print(df_das)            
    variable2="PUERTOLIBRE"
    #variable3="BOGO-GARCE"
    filtro2=file_3[file_3['Unnamed: 5'].str.contains(variable2,case=False,na=False,regex=True)].fillna(value='No Data')
    filtro3=filtro2[filtro2['Dispositivo'].str.contains(variable3,case=False,na=False,regex=True)].fillna(value='No Data')
    print(filtro3)
    filtro3_sin_duplicados = filtro3.drop_duplicates()
    print(filtro3_sin_duplicados)

    filtro3_sin_duplicados.to_excel("out1.xlsx")
    df_cos=pd.DataFrame(file_despues_COS)
    df_out=complet_COS(df_cos)
    print("")
    print("")
    
except KeyError as e:
    print(f"Error:{e}")


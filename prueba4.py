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
print(file_despues_COS)
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

def simpli_DAAS(df):
    Valor_Dispositivo=df['Dispositivo']
    Valor_Ip=df['IP']
    valor_dispositivo=Valor_Dispositivo.index
    valor_list_dispositivo=valor_dispositivo.to_list()
    valor_IP=Valor_Ip.index
    valor__list_IP=valor_IP.to_list()
    indice_IP=valor__list_IP[1]
    indice_IP2=valor__list_IP[0]
    indice_Dispositivo=valor_list_dispositivo[1]
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
    #variable="39g1"
    variable="fas1"
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
    variable2="PUERTOLIBRE"
    #variable3="BOGO-GARCE"
    filtro2=file_3[file_3['Unnamed: 5'].str.contains(variable2,case=False,na=False,regex=True)].fillna(value='No Data')
    
    filtro3=filtro2[filtro2['Dispositivo'].str.contains(variable3,case=False,na=False,regex=True)].fillna(value='No Data')
    filtro3_sin_duplicados = filtro3.drop_duplicates()
    print(filtro3_sin_duplicados)
    variable_disp,variable_ip,variable_ip2=simpli_DAAS(filtro3)
    filtro4=filtro3_sin_duplicados[filtro3_sin_duplicados['Dispositivo'].str.contains(variable_disp,case=False,na=False,regex=True)]#!Opcion 1
    ############!Opcion2
    if filtro3_sin_duplicados['IP'].str.contains(str(variable_ip)).any():
        in_colum=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip),case=False,na=False,regex=True)
        temp_df=filtro3_sin_duplicados[in_colum]
        en_tempo=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip+1),case=False,na=False,regex=True)
        CON_DAAS_COS=filtro3_sin_duplicados[in_colum | en_tempo]
        CON_DAAS_COS.to_excel("out4.xlsx")
        #print(filtro3_sin_duplicados[in_colum | en_tempo])
    elif filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2)).any():
        in_colum=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2),case=False,na=False,regex=True)
        temp_df=filtro3_sin_duplicados[in_colum]
        en_tempo=filtro3_sin_duplicados['IP'].str.contains(str(variable_ip2+1),case=False,na=False,regex=True)
        CON_DAAS_COS=filtro3_sin_duplicados[in_colum | en_tempo]
        CON_DAAS_COS.to_excel("out4.xlsx")
        #print(filtro3_sin_duplicados[in_colum | en_tempo]) 
    ############

    #!filtro4.to_excel("out2.xlsx")
    df_cos=pd.DataFrame(file_despues_COS)
    df_out=complet_COS(df_cos)
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
    print(final)

    DIS_COS=final['Dispositivo COS']
    index_DIS_COS=DIS_COS.index
    index_DIS_COS_list=index_DIS_COS.to_list()
    indice_DIS_COS=index_DIS_COS_list[1]
    UNO = final.loc[indice_DIS_COS, "Dispositivo COS"]

    print(UNO)
    first=UNO.find("-")
    second=UNO.find("-",first+1)
    three=UNO.find("-",second+1)
    four=UNO.find("-",three+1)
    UN_COS=UNO[three+1:four]
    print(UN_COS)
    if final['Dispositivo COS'].str.contains(UN_COS,case=False,na=False,regex=True).any():
        NO_dos_COS=final['Dispositivo COS'].str.contains(UN_COS,case=False,na=False,regex=True)
        FINAL_FILTRADO=final[NO_dos_COS]
    else:
        FINAL_FILTRADO=final
    print(FINAL_FILTRADO )    
    final.to_excel("out8.xlsx")
    FINAL_FILTRADO.drop("0")
    FINAL_FILTRADO.to_excel("out9.xlsx")
except KeyError as e:
    print(f"Error:{e}")


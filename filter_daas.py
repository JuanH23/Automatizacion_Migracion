import pandas as pd
import random
def sum_daas(df_cd,filter_daas,type_node):
    simil=[]
    #Realiza la conversion del segundo das en vez que comience de 0-48, empiece
    #de 49-97.
    if df_cd['Dispositivo DAAS'].str.contains(str(filter_daas+1)).any():#Revisa que tenga mas de un DAAS
            print("ENTRO AL DAAS")
            print(f"filter_DAAS==>{filter_daas+1}")
            #Organiza los valores 
            df_cd = df_cd.sort_values('Puerto COS',inplace=False,ascending=True)
            #Crea una mascara
            mask_range = df_cd['Puerto DAAS'].between('xe-0/0/0', 'xe-0/0/48')
            mask_name = df_cd['Dispositivo DAAS'].str.contains(str(filter_daas+1))
            mask_range_name = mask_name & mask_range
            #Le suma a cada valor que ya se le realizo un split con el simbolo "/" del segundo Daas y le suma 49 a cada valor que encuentre
            df_cd.loc[mask_range_name, 'Puerto DAAS'] = (
                df_cd.loc[mask_range_name, 'Puerto DAAS']
                .str.replace(r'xe-0/0/(\d+)', lambda x: 'xe-0/0/' + str(int(x.group(1))+49))
            )
            
            df_cd['Puerto DAAS']=df_cd['Puerto DAAS'].astype(str)
            df_cd['ultimo_num_DAAS'] = df_cd['Puerto DAAS'].apply(lambda x: get_x(x, 0))
            # Extraer el primer número de cada entrada en la columna puerto_COS
            df_cd['primer_num_COS'] = df_cd['Puerto COS'].str.split(':').str[0]
            print(f"df_cd==>{df_cd}")
            df_cd=df_cd.drop_duplicates(subset='primer_num_COS')
            print(f"df_cd_sin_duplicados==>{df_cd}")
            #df_cd.to_excel("new_numbers.xlsx")
            ###############################!
            #Crea una columna con los numeros unicos del DAAS
            numeros_coincidentes=df_cd['ultimo_num_DAAS'].unique()
            #Revisa cuales de los puertos del DAAS estan en la columna nueva donde se encuentran
            coincidente_COS=df_cd[df_cd['primer_num_COS'].isin(numeros_coincidentes)]
            #coincidente_COS.to_excel("coincidente.xlsx")
            coincidente_DAAS=df_cd[df_cd['ultimo_num_DAAS'].isin(coincidente_COS['primer_num_COS'])]
            #coincidente_DAAS.to_excel("coincidente_2.xlsx")
            coincidente_COS=coincidente_COS.loc[:,['Dispositivo COS','Puerto COS','primer_num_COS']]
            coincidente_COS=coincidente_COS.reset_index(drop=True)
            coincidente_DAAS=coincidente_DAAS.loc[:,['Dispositivo DAAS','Puerto DAAS']]
            coincidente_DAAS=coincidente_DAAS.reset_index(drop=True)
            #une ambos Dataframe para trabajar con un solo Data
            merge_coincidente=pd.concat([coincidente_COS,coincidente_DAAS],axis=1)
            merge_coincidente.to_excel('merge_coincidente.xlsx')
            valores_unicos=merge_coincidente['primer_num_COS'].unique().tolist()
            #Toma un valor aleatorio del puerto COS y lo coloca en el formato
            valor_aleatorio = random.choice(valores_unicos)
            valores_unicos.remove(valor_aleatorio)
            filas_aleatorias = merge_coincidente.loc[merge_coincidente['primer_num_COS'] == valor_aleatorio]           
            print(f"numero_random_solo_UNA__VEZ==>{filas_aleatorias}")
            print(f"TYPE_NODE==>{type_node}")
            ###############################!             
            #print(f"simil==>{simil}")
    else:                                                       #Si solo tiene un dispositivo DAAS
            df_cd['Puerto DAAS']=df_cd['Puerto DAAS'].astype(str)
            df_cd['ultimo_num_DAAS'] = df_cd['Puerto DAAS'].apply(lambda x: get_x(x, 0))
            # Extraer el primer número de cada entrada en la columna puerto_COS
            df_cd['primer_num_COS'] = df_cd['Puerto COS'].str.split(':').str[0]
            df_cd=df_cd.drop_duplicates(subset='primer_num_COS')
            #df_cd.to_excel("same_new_numbers.xlsx")
            ###############################!
            numeros_coincidentes=df_cd['ultimo_num_DAAS'].unique()
            coincidente_COS=df_cd[df_cd['primer_num_COS'].isin(numeros_coincidentes)]
            #coincidente=df_cd.loc[df_cd['ultimo_num_DAAS'].isin(df_cd['primer_num_COS'])]
            #coincidente_COS.to_excel("coincidente.xlsx")
            coincidente_DAAS=df_cd[df_cd['ultimo_num_DAAS'].isin(coincidente_COS['primer_num_COS'])]
            #coincidente_DAAS.to_excel("coincidente_2.xlsx")
            coincidente_COS=coincidente_COS.loc[:,['Dispositivo COS','Puerto COS','primer_num_COS']]
            coincidente_COS=coincidente_COS.reset_index(drop=True)
            coincidente_DAAS=coincidente_DAAS.loc[:,['Dispositivo DAAS','Puerto DAAS']]
            coincidente_DAAS=coincidente_DAAS.reset_index(drop=True)
            merge_coincidente=pd.concat([coincidente_COS,coincidente_DAAS],axis=1)
            #merge_coincidente.to_excel('merge_coincidente.xlsx')         
            print(f"TYPE_NODE==>{type_node}")
            ###############################!    
            merge_coincidente.to_excel("merge_same_numbers.xlsx")  
            valores_unicos=merge_coincidente['primer_num_COS'].unique().tolist()
            valor_aleatorio = random.choice(valores_unicos)
            valores_unicos.remove(valor_aleatorio)
            filas_aleatorias = merge_coincidente.loc[merge_coincidente['primer_num_COS'] == valor_aleatorio]
            filas_aleatorias['primer_num_COS']=filas_aleatorias['primer_num_COS'].astype(str)
            print(f"numero_random_solo_UNA__VEZ==>{filas_aleatorias}")           
            print(f"TYPE_NODE==>{type_node}")       
            print(f"simil==>{simil}")
    ######################################!
    return filas_aleatorias 
#funcion para realizar split de los elementos de la columna "Puerto DAAS"
def get_x(s, n=2):
    elements = s.split('/')
    if len(elements) >= n+1:
        return elements[-(n+1)]
    else:
        return None
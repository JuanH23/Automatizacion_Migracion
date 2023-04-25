import pandas as pd
from openpyxl.styles import Font, PatternFill
from openpyxl.styles import Alignment
from openpyxl.styles import Border, Side
from openpyxl.styles import Color,Font
import openpyxl
import os
from dotenv import set_key,dotenv_values 
from Advertencia import*
import numpy as np
# Crear DataFrame con información
def diseño(df,df_cos_daas,name_file,filter_daas):

    ###########
    env=dotenv_values(".env")
    ruth_list_download= env["path_list_download"]
    ruta_nueva_carpeta = ruth_list_download + "/Diseños_NODOS"
    os.makedirs(ruta_nueva_carpeta, exist_ok=True)
    ruta_archivo = os.path.join(ruta_nueva_carpeta,'Diseño Segmentaciones RPHY-NODO '+ name_file +'.xlsx')
    set_key(".env","path_files_upload",ruta_nueva_carpeta)
    ###########
    

    # Crear archivo Excel desde cero y escribir información del DataFrame
    archivo_excel = pd.ExcelWriter(ruta_archivo, engine='openpyxl')


    # Escribir el DataFrame en el archivo Excel
    df_cd=pd.DataFrame(df_cos_daas)
    print(f"df_cd==>{df_cd}")
    ################################################################
    
    df.to_excel(archivo_excel,sheet_name='Hoja1' ,index=False)

    ################################################################
    hoja = archivo_excel.sheets['Hoja1']
    # Obtener el libro de trabajo y la hoja
    workbook = archivo_excel.book
    worksheet = workbook.active
    
    '''celda_inicial = worksheet['A4']
    for i in range(len(df)):
        for j in range(len(df.columns)):
            # Obtener la celda actual en la hoja de trabajo
            celda_actual = worksheet.cell(row=i+celda_inicial.row, column=j+celda_inicial.column)
            # Asignar el valor del dataframe a la celda actual
            celda_actual.value = df.iloc[i, j]'''

    #######################
    # Escribir la primera columna del dataframe en la columna A de la hoja de trabajo
    columna = 1  # Columna A
    fila_inicial = 4  # Empezar a escribir desde la fila 2
    for i, valor in enumerate(df['CMTS']):
        celda_actual = worksheet.cell(row=fila_inicial+i, column=columna)
        celda_actual.value = valor
    # Escribir la primera columna del dataframe en la columna A de la hoja de trabajo
    columna = 2  # Columna B
    fila_inicial = 4  # Empezar a escribir desde la fila 2
    for i, valor in enumerate(df['S/CG/CH']):
        celda_actual = worksheet.cell(row=fila_inicial+i, column=columna)
        celda_actual.value = valor
    # Escribir la primera columna del dataframe en la columna A de la hoja de trabajo
    columna = 5  # Columna B
    fila_inicial = 4  # Empezar a escribir desde la fila 2
    
    for i, valor in enumerate(df['Total'].astype(int)):
        celda_actual = worksheet.cell(row=fila_inicial+i, column=columna)
        celda_actual.value = valor
    # Escribir la primera columna del dataframe en la columna A de la hoja de trabajo
    columna = 6  # Columna B
    fila_inicial = 4  # Empezar a escribir desde la fila 2
    for i, valor in enumerate(df['Description']):
        celda_actual = worksheet.cell(row=fila_inicial+i, column=columna)
        celda_actual.value = valor
    
    columna = worksheet["C"]
    rango=columna[3:12]
    # bucle para establecer el valor de cada celda en None
    for celda in rango:
        celda.value = None
        
    columna = worksheet["D"]
    rango=columna[3:12]
    # bucle para establecer el valor de cada celda en None
    for celda in rango:
        celda.value = None             
    #######################


    # Crear objeto de relleno blanco
    fill = PatternFill(fill_type='solid', start_color='FFFFFFFF', end_color='FFFFFFFF')

    # Recorrer todas las celdas y aplicar el relleno blanco
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        

        # Obtener el número de filas y columnas de la hoja
        max_row = sheet.max_row
        max_col = sheet.max_column
        # Recorrer todas las celdas de la hoja y establecer su color de fondo en blanco
        for row in range(1, max_row + 1):
            for col in range(1, max_col + 1):
                cell = sheet.cell(row=row, column=col)
                cell.fill = fill

    ########################################TABLA_ANTES##########################################
    hoja.merge_cells(start_row=1, start_column=1, end_row=1, end_column=7)
    hoja.merge_cells(start_row=4, start_column=7, end_row=7, end_column=7)
    hoja.row_dimensions[1].height=20
    hoja.column_dimensions['A'].width=28
    hoja.column_dimensions['F'].width=40
    fuente=Font(size=14)
    fuente.bold=True
    hoja.cell(row=1,column=1).font=fuente
    chasis_valor=df['CMTS']
    chasis_index=chasis_valor.index
    chasis_list=chasis_index.to_list()
    print(f"chasis_valor==>{chasis_valor}")
    print(f"chasis_index==>{chasis_list}")
    indice=chasis_list[1]
    texto=df.loc[indice,"CMTS"]
    #texto_chasis="MEDE-CABA-H-03-CS100G#"
    celda=hoja.cell(row=1,column=1)
    celda.value=texto

    hoja.merge_cells(start_row=2, start_column=1, end_row=2, end_column=7)
    hoja.row_dimensions[2].height=30
    hoja.column_dimensions['F'].width=40
    fuente=Font(size=12)
    fuente.bold=True
    hoja.cell(row=2,column=1).font=fuente
    texto="Antes"
    celda=hoja.cell(row=2,column=1)
    celda.value=texto
    cell = worksheet.cell(row=2, column=1)
    cell_range = worksheet['A2:G2']
    cell.alignment = Alignment(horizontal='center', vertical='center')
    border=Border(top=Side(style='thick'),bottom=Side(style='thick'),left=Side(style='thick'),right=Side(style='thick'))
    border_chasis=Border(top=Side(style='thick'),bottom=Side(style='thick'),left=Side(style='thick'),right=Side(style='thick'))
    for cells in cell_range:
        for cell in cells:
            cell.border = border
    texto="CHASIS"
    celda_CHASIS=hoja.cell(row=3,column=1)
    celda_CHASIS.value=texto
    texto="SLOT"
    celda=hoja.cell(row=3,column=2)
    celda.value=texto
    texto="CMAC"
    celda=hoja.cell(row=3,column=3)
    celda.value=texto
    texto="DMAC"
    celda=hoja.cell(row=3,column=4)
    celda.value=texto
    texto="CLIENTES"
    celda=hoja.cell(row=3,column=5)
    celda.value=texto
    texto="NOMBRE"
    celda=hoja.cell(row=3,column=6)
    celda.value=texto
    texto="USUARIOS"
    celda_USU=hoja.cell(row=3,column=7)
    celda_USU.value=texto
    celda_USU.border=border_chasis
    fuente=Font(size=10)
    fuente.bold=True
    hoja.cell(row=3,column=7).font=fuente
    cell_aligment_row3= Alignment(horizontal='center', vertical='center')
    fila = 3 # Aquí se selecciona la fila deseada
    for celda in hoja[fila]:
        celda.alignment = cell_aligment_row3
    hoja.column_dimensions['G'].width=10
    cell_range_row3 = worksheet['A3:F3']
    cell.alignment = Alignment(horizontal='center', vertical='center')
    dark_blue=Color(rgb='366092')
    relleno = PatternFill(start_color=dark_blue, end_color=dark_blue, fill_type='solid')
    border=Border(top=Side(style='thin'),bottom=Side(style='thin'),left=Side(style='thin'),right=Side(style='thin'))
    white_font = Font(color='FFFFFF')
    for cells in cell_range_row3:
        for cell in cells:
            cell.border = border
            cell.font=white_font
            cell.fill=relleno

    rango=hoja['E4:E12']
    
    #suma_columna = sum([celda.value for fila in rango for celda in fila ])
    suma_columna = sum([0 if celda.value is None else celda.value for fila in rango for celda in fila])

    celda_resultado = hoja['G4']
    celda_resultado.value = suma_columna
    cell = worksheet.cell(row=4, column=7)
    red=Color(rgb='FF0000')
    red_font = Font(color=red)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.font=red_font
    ########################################TABLA_DEPUES##########################################
    hoja.merge_cells(start_row=1, start_column=9, end_row=1, end_column=17)
    hoja.column_dimensions['I'].width=20
    hoja.column_dimensions['J'].width=25
    hoja.column_dimensions['K'].width=15
    hoja.column_dimensions['L'].width=25
    hoja.column_dimensions['N'].width=15
    hoja.column_dimensions['Q'].width=45

    fuente=Font(size=14)
    fuente.bold=True
    hoja.cell(row=1,column=9).font=fuente
    Dispositivo_cos_valor=df_cos_daas['Dispositivo COS']
    Dispositivo_cos_index=Dispositivo_cos_valor.index
    Dispositivo_cos_list=Dispositivo_cos_index.to_list()
    indice_Dispositivo_cos=Dispositivo_cos_list[1]
    texto_dispositivo_cos=df_cos_daas.loc[indice_Dispositivo_cos,"Dispositivo COS"]
    #texto_dispositivo_cos="BOGO-FONT-H-09-COS"
    celda=hoja.cell(row=1,column=9)
    celda.value=texto_dispositivo_cos
    hoja.merge_cells(start_row=2, start_column=9, end_row=2, end_column=17)
    hoja.merge_cells(start_row=4, start_column=9, end_row=8, end_column=9)
    fuente=Font(size=12)
    fuente.bold=True
    hoja.cell(row=2,column=9).font=fuente
    texto="DESPUES"
    celda=hoja.cell(row=2,column=9)
    celda.value=texto
    cell1 = worksheet.cell(row=1, column=9)
    cell2 = worksheet.cell(row=2, column=9)
    cell_range_row4 = worksheet['I2:Q2']
    cell_range_row5 = worksheet['I3:Q3']
    cell_range_row6 = worksheet['I4:Q4']
    cell_range_row7 = worksheet['I5:Q5']
    cell_range_row8 = worksheet['I7:Q7']
    cell_range_row9 = worksheet['I8:Q8']
    cell_range_row10 = worksheet['I6']

    cell1.alignment = Alignment(horizontal='center', vertical='center')
    cell2.alignment = Alignment(horizontal='center', vertical='center')
    border=Border(top=Side(style='thin'),bottom=Side(style='thin'),left=Side(style='thin'),right=Side(style='thin'))
    cell_range_row10.border=border

    for cells in cell_range_row4:
        for cell in cells:
            cell.border = border
    for cells in cell_range_row5:
        for cell in cells:
            cell.border = border
    for cells in cell_range_row6:
        for cell in cells:
            cell.border = border
    for cells in cell_range_row7:
        for cell in cells:
            cell.border = border
    for cells in cell_range_row8:
        for cell in cells:
            cell.border = border
    for cells in cell_range_row9:
        for cell in cells:
            cell.border = border                 
    texto="REGIONAL"
    celda=hoja.cell(row=3,column=9)
    celda.value=texto
    texto="DAAS"
    celda=hoja.cell(row=3,column=10)
    celda.value=texto
    texto="PUERTO DAAS"
    celda=hoja.cell(row=3,column=11)
    celda.value=texto
    texto="CHASIS"
    celda=hoja.cell(row=3,column=12)
    celda.value=texto
    ################################!
    celda=hoja.cell(row=4,column=12)
    celda.value=texto_dispositivo_cos
    celda=hoja.cell(row=5,column=12)
    celda.value=texto_dispositivo_cos
    celda=hoja.cell(row=7,column=12)
    celda.value=texto_dispositivo_cos
    celda=hoja.cell(row=8,column=12)
    celda.value=texto_dispositivo_cos
    ################################!CAMBIAR DEPENDIENDO DE QUE NODO SEA DESPUES DE LA EXPLICACION
    texto="RPD"
    celda=hoja.cell(row=3,column=13)
    celda.value=texto
    texto="UPSTREAM"
    celda=hoja.cell(row=3,column=14)
    celda.value=texto
    texto="DMAC"
    celda=hoja.cell(row=3,column=15)
    celda.value=texto     
    texto="CLIENTES"
    celda=hoja.cell(row=3,column=16)
    celda.value=texto 
    texto="NOMBRE"
    celda=hoja.cell(row=3,column=17)
    celda.value=texto 
    cell_range_row3_despues= worksheet['I3:Q3']
    alignment = Alignment(horizontal='center', vertical='center')
    border=Border(top=Side(style='thin'),bottom=Side(style='thin'),left=Side(style='thin'),right=Side(style='thin'))
    white_font = Font(color='FFFFFF')
    dark_blue=Color(rgb='366092')
    relleno = PatternFill(start_color=dark_blue, end_color=dark_blue, fill_type='solid')
    for cells in cell_range_row3_despues:
        for cell in cells:
            cell.border = border
            cell.font=white_font
            cell.fill=relleno
            cell.alignment=alignment
    texto="Nodo 2x4"
    celda=hoja.cell(row=4,column=9)
    celda.value=texto 
    cell = worksheet.cell(row=4, column=9)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    yellow=Color(rgb='FFC000')
    relleno = PatternFill(start_color=yellow, end_color=yellow, fill_type='solid')
    pink=Color(rgb='FCD5B4')
    relleno_pink=PatternFill(start_color=pink,end_color=pink,fill_type='solid')
    cell_range_row4=worksheet['J4:Q4']
    cell_range_row5=worksheet['J5:Q5']
    cell_range_row7=worksheet['J7:Q7']
    cell_range_row7=worksheet['J8:Q8']
    for cells in cell_range_row4:
        for cell in cells:
            cell.fill=relleno 
    for cells in cell_range_row5:
        for cell in cells:
            cell.fill=relleno_pink         
    for cells in cell_range_row7:
        for cell in cells:
            cell.fill=relleno 
    for cells in cell_range_row8:
        for cell in cells:
            cell.fill=relleno_pink
    ###############################################
    DISPOSITIVO_DAAS = df_cd['Dispositivo DAAS'].unique()
    simil=[]

    if df_cd['Dispositivo DAAS'].str.contains(str(filter_daas+1)).any():
            print("ENTRO AL DAAS")
            print(f"filter_DAAS==>{filter_daas+1}")
            
            mask_range = df_cd['Puerto DAAS'].between('xe-0/0/0', 'xe-0/0/48')
            mask_name = df_cd['Dispositivo DAAS'].str.contains(str(filter_daas+1))
            mask_range_name = mask_name & mask_range
            df_cd.loc[mask_range_name, 'Puerto DAAS'] = (
                df_cd.loc[mask_range_name, 'Puerto DAAS']
                .str.replace(r'xe-0/0/(\d+)', lambda x: 'xe-0/0/' + str(int(x.group(1))+49))
            )
            df_cd.to_excel("new_numbers.xlsx")
            df_cd['Puerto DAAS']=df_cd['Puerto DAAS'].astype(str)
            df_cd['ultimo_num_DAAS'] = df_cd['Puerto DAAS'].apply(lambda x: get_x(x, 0))

                # Extraer el primer número de cada entrada en la columna puerto_COS
            df_cd['primer_num_COS'] = df_cd['Puerto COS'].str.split(':').str[0]

            # Crear una máscara booleana que seleccione las filas donde los primeros números coinciden
            mask_coincide = df_cd['primer_num_COS'].isin(df_cd['ultimo_num_DAAS'])
            mask_coincide_2= df_cd['ultimo_num_DAAS'].isin(df_cd['ultimo_num_DAAS'])
            mask_coincide_range=mask_coincide & mask_coincide_2
            # Seleccionar las filas que cumplen con la máscara booleana
            df_coincidente = df_cd.loc[mask_coincide_range]
            df_coincidente=df_coincidente.reset_index(drop=True)
            df_coincidente=df_coincidente.loc[:,['Dispositivo COS','Puerto COS','ptp']].dropna()
            df_cd2=df_cd.copy()
            df_cd2=df_cd2.loc[:,['Dispositivo DAAS','Puerto DAAS','Unnamed: 5']].dropna()
            df_cd2=df_cd2.reset_index(drop=True)
            df_cd2.rename(columns={'Dispositivo DAAS': 'Dispositivo COS', 'Puerto DAAS': 'Puerto COS', 'Unnamed: 5': 'ptp'}, inplace=True)
            #df_out[['Dispositivo COS', 'Puerto COS', 'ptp']] = df_cd2[['Dispositivo COS', 'Puerto COS', 'ptp']]
            df_out = pd.concat([df_coincidente, df_cd2],axis=1)
            #df_out = df_out.sort_values(by=['Puerto COS'])
            print(f"df_out==>{df_out}")
            df_out=df_out.reset_index(drop=True)    
            df_out.to_excel("simil_new_numbers.xlsx")  
            

  
                    
            #print(f"simil==>{simil}")
    else:
        df_cd['Puerto DAAS']=df_cd['Puerto DAAS'].astype(str)
        df_cd['ultimo_num_DAAS'] = df_cd['Puerto DAAS'].apply(lambda x: get_x(x, 0))

        # Extraer el primer número de cada entrada en la columna puerto_COS
        df_cd['primer_num_COS'] = df_cd['Puerto COS'].str.split(':').str[0]
        df_cd.to_excel("same_new_numbers.xlsx")
        # Crear una máscara booleana que seleccione las filas donde los primeros números coinciden
        mask_coincide = df_cd['primer_num_COS'].isin(df_cd['ultimo_num_DAAS'])
        mask_coincide_2= df_cd['ultimo_num_DAAS'].isin(df_cd['ultimo_num_DAAS'])
        mask_coincide_range=mask_coincide & mask_coincide_2
        # Seleccionar las filas que cumplen con la máscara booleana
        df_coincidente = df_cd.loc[mask_coincide_range]
        df_coincidente=df_coincidente.reset_index(drop=True)
        df_coincidente=df_coincidente.loc[:,['Dispositivo COS','Puerto COS','ptp']].dropna()
        df_cd2=df_cd.copy()
        df_cd2=df_cd2.loc[:,['Dispositivo DAAS','Puerto DAAS','Unnamed: 5']].dropna()
        df_cd2=df_cd2.reset_index(drop=True)
        df_cd2.rename(columns={'Dispositivo DAAS': 'Dispositivo COS', 'Puerto DAAS': 'Puerto COS', 'Unnamed: 5': 'ptp'}, inplace=True)
        #df_out[['Dispositivo COS', 'Puerto COS', 'ptp']] = df_cd2[['Dispositivo COS', 'Puerto COS', 'ptp']]
        df_out = pd.concat([df_coincidente, df_cd2],axis=1)
        #df_out = df_out.sort_values(by=['Puerto COS'])
        print(f"df_out==>{df_out}")
        df_out=df_out.reset_index(drop=True)                
        df_out.to_excel("simil_same_numbers.xlsx")         
        print(f"simil==>{simil}")



    texto="SCRIPT  ANTES-NOC CABLE"
    celda=hoja.cell(row=17,column=6)
    celda.value=texto
    cell = worksheet.cell(row=17, column=6)
    red=Color(rgb='FF0000')
    red_font = Font(color=red)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.font=red_font 
    texto="config"
    celda=hoja.cell(row=19,column=6)
    celda.value=texto

    sep=0
    sep2=0
    text_script=""
    slot_valor=df['S/CG/CH']
    slot_index=slot_valor.index
    slot_list=slot_index.to_list()
    #print(f"slot_valor==>{slot_valor}")
    #print(f"slot_list==>{slot_list}")
    indice_slot=slot_list[0]
    texto_slot=df.loc[indice_slot,"S/CG/CH"]
    #print(texto_slot)
    if "U" in texto_slot:
        sep=texto_slot.find("/")
        sep2=texto_slot.find("/",sep+1)
        text_script=texto_slot[:sep2+2]
        text_script_a=text_script
        text_script_b=text_script
        text_script_c=text_script
        text_script_d=text_script
    else:
        #print(f"len_slot_list==>{len(slot_list)}")
        if len(slot_list)==4:
            a=df.loc[slot_list[0],"S/CG/CH"]
            b=df.loc[slot_list[1],"S/CG/CH"]
            c=df.loc[slot_list[2],"S/CG/CH"]
            d=df.loc[slot_list[3],"S/CG/CH"]
            #print(f"a==>{a}")
            #print(f"b==>{b}")
            #print(f"c==>{c}")
            #print(f"d==>{d}")
            sepa=a.find("/")
            sepa2=a.find("/",sepa+1)
            text_script_a=a[:sepa2]
            sepb=b.find("/")
            sepb2=b.find("/",sepb+1)
            text_script_b=b[:sepb2]
            sepc=c.find("/")
            sepc2=c.find("/",sepc+1)
            text_script_c=c[:sepc2]
            sepd=d.find("/")
            sepd2=d.find("/",sepd+1)
            text_script_d=d[:sepd2]
            #print(f"text_script_a==>{text_script_a}")
            #print(f"text_script_b==>{text_script_b}")
            #print(f"text_script_c==>{text_script_c}")
            #print(f"text_script_d==>{text_script_d}")                                  
        else:
            a=df.loc[slot_list[0],"S/CG/CH"]
            b=df.loc[slot_list[1],"S/CG/CH"]
            c=df.loc[slot_list[2],"S/CG/CH"]
            #print(f"a==>{a}")
            #print(f"b==>{b}")
            #print(f"c==>{c}")
            sepa=a.find("/")
            sepa2=a.find("/",sepa+1)
            text_script_a=a[:sepa2]
            sepb=b.find("/")
            sepb2=b.find("/",sepb+1)
            text_script_b=b[:sepb2]
            sepc=c.find("/")
            sepc2=c.find("/",sepc+1)
            text_script_c=c[:sepc2]
            text_script_d=""
            #print(f"text_script_a==>{text_script_a}")
            #print(f"text_script_b==>{text_script_b}")
            #print(f"text_script_c==>{text_script_c}") 

    texto="interface upstream "+text_script_a
    celda=hoja.cell(row=20,column=6)
    celda.value=texto
    texto='  description "PUERTO LIBRE"'
    celda=hoja.cell(row=21,column=6)
    celda.value=texto
    texto='  logical-channel 0 description "PUERTO LIBRE"'
    celda=hoja.cell(row=22,column=6)
    celda.value=texto
    texto="end"
    celda=hoja.cell(row=23,column=6)
    celda.value=texto
    texto="interface upstream "+text_script_b
    celda=hoja.cell(row=24,column=6)
    celda.value=texto
    texto='  description "PUERTO LIBRE"'
    celda=hoja.cell(row=25,column=6)
    celda.value=texto
    texto='  logical-channel 0 description "PUERTO LIBRE"'
    celda=hoja.cell(row=26,column=6)
    celda.value=texto
    texto="end"
    celda=hoja.cell(row=27,column=6)
    celda.value=texto
    texto="interface upstream "+text_script_c
    celda=hoja.cell(row=28,column=6)
    celda.value=texto
    texto='  description "PUERTO LIBRE"'
    celda=hoja.cell(row=29,column=6)
    celda.value=texto
    texto='  logical-channel 0 description "PUERTO LIBRE"'
    celda=hoja.cell(row=30,column=6)
    celda.value=texto
    texto="end"
    celda=hoja.cell(row=31,column=6)
    celda.value=texto
    texto="interface upstream "+text_script_d
    celda=hoja.cell(row=32,column=6)
    celda.value=texto
    texto='  description "PUERTO LIBRE"'
    celda=hoja.cell(row=33,column=6)
    celda.value=texto
    texto='  logical-channel 0 description "PUERTO LIBRE"'
    celda=hoja.cell(row=34,column=6)
    celda.value=texto

    description_valor=df['Description']
    description_index=description_valor.index
    description_list=description_index.to_list()
    #print(f"slot_valor==>{description_valor}")
    #print(f"slot_list==>{description_list}")
    indice_description=description_list[0]
    text_description=df.loc[indice_description,"Description"]

    sep=text_description.find("DO")
    sep2=text_description.find("(")
    text_script=text_description[sep+2:sep2]   

    texto="config"
    celda=hoja.cell(row=38,column=6)
    celda.value=texto
    texto="no service group "+text_script
    celda=hoja.cell(row=39,column=6)
    celda.value=texto
    texto="exit"
    celda=hoja.cell(row=40,column=6)
    celda.value=texto

    texto="NOTA: SI HAY CAMBIO DE IP"
    hoja.merge_cells(start_row=16, start_column=7, end_row=16, end_column=10)
    celda=hoja.cell(row=16,column=7)
    celda.value=texto
    cell_range_row16 = worksheet['G16:J16']
    cell = worksheet.cell(row=17, column=7)
    red_2=Color(rgb='FF0000')
    white=Color(rgb='FFFFFF')
    white_font = Font(color=white)
    relleno_2 = PatternFill(start_color=red_2, end_color=red_2, fill_type='solid')
    celda.alignment = Alignment(horizontal='center', vertical='center')
    celda.font=white_font
    for cells in cell_range_row16:
        for cell in cells:
            cell.fill=relleno_2                
    # Guardar archivo Excel
    
    archivo_excel.save()

def get_x(s, n=2):
    elements = s.split('/')
    if len(elements) >= n+1:
        return elements[-(n+1)]
    else:
        return None

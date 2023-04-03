import pandas as pd
 
excel_file = "Descargas/Arris.xlsx"
df = pd.read_excel(excel_file)
file=pd.DataFrame(df)
file=file.rename(columns={'S/CG/CH':'S\\CG\\CH'})
print(file)
file_2=file.loc[:,['CMTS','S\\CG\\CH','Total','Description']].fillna(value='No Data')#*Filtra las columnas y si en esas columnas no hay ningún valor coloca "No Data"
file_2['S\\CG\\CH']=file_2['S\\CG\\CH'].str.replace('/','\\')
file_2[['S\\CG\\CH','Total','Description']] = file_2[['S\\CG\\CH','Total','Description']].astype(str)#*Convierte los valores de estas columnas a tipo str
data = file_2.to_dict('records')#*Convierte el dataframe ya filtrado, en un diccionario
print(data)

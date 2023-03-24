import pandas as pd
path="data/Ocupacion.xlsx"
file_despues=pd.read_excel(path,sheet_name='Hoja2',engine='openpyxl')
df2=pd.DataFrame(file_despues)
file_3=df2.loc[:,['IP','Dispositivo','Puerto','status','Unnamed: 5']].astype(str).fillna(value='No Data')
variable2="PUERTOLIBRE"
filtro2=file_3[file_3['Unnamed: 5'].str.contains(variable2,case=False,na=False,regex=True)].fillna(value='No Data')
print(filtro2)
filtro2.to_excel("pruebaaaaa.xlsx",index=False,engine='openpyxl')

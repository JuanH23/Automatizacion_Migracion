import pandas as pd
import seaborn as sns

path="Descargas/Arris_SCMSummary.xlsx"
file=pd.read_excel(path)
df=pd.DataFrame(file)
#print(file)
file_2=df.loc[:,['CMTS','Mac','Total','Description']]
print(file_2)
file_2[['Mac','Total','Description']] = file_2[['Mac','Total','Description']].astype(str)
#file_2['Description']=file_2['Description'].str.strip()
file_2.style.text_gradient(cmap='PyiYG')
file_2.to_excel("./P.xlsx")
'''variable =""

while variable!='exit':
    variable=input("Busque el nodo==>")
    if not variable == 'exit':
        variable=variable.upper()      
        filtro=file_2[file_2['Description'].str.contains(variable,case=False,na=False,regex=True)]
        if not (filtro['Description'].str.contains(variable,case=False,na=False,regex=True)!=variable).any() == (filtro['Description'].str.contains(variable,case=False,na=False,regex=True)==variable).any():
            print(filtro)
            if  not variable=='':  
                filtro.style.background_gradient(axis=0)      
                filtro.to_excel(f'Nodo_{variable}.xlsx')    
            else:
                continue
        else:
            continue
    else:
        continue'''



# Aplicamos la función al DataFrame




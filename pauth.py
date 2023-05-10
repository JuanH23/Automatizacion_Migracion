from office365.sharepoint.client_context import ClientContext
#from office365.sharepoint.file import File
import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
import time
# Variables de configuración
site_url = "https://claromovilco.sharepoint.com/sites/Prueba35/"
username = "juan.hurtado@claro.com.co"
password = "JUEhp$9_23"
auth=True
list_title = "Lista_COS2"
while auth==True:
    try:
        auth_context = AuthenticationContext(site_url)
        auth_context.acquire_token_for_user(username, password)
        ctx = ClientContext(site_url, auth_context)
        list_obj = ctx.web.lists.get_by_title(list_title)
        ctx.load(list_obj)
        ctx.execute_query()
        if list_obj.properties:
            print("Autenticación exitosa. Se obtuvo la lista:", list_obj.properties["Title"])
        else:
            print("La autenticación falló. No se pudo obtener la lista.")
        auth=False    
    except ValueError as e:
        print("error MFA, reintentando conectar")
        time.sleep(2)
        continue
    
    ##!Lista_arris
    ##!Lista_Casa
    ##!Lista_Cos
    ##!Lista_COS2
    #*P_P
    #*Lista_Daas
    # Verificar la respuesta

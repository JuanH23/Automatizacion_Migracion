import environ
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential 
from office365.sharepoint.files.file import File
import ssl
from office365.runtime.auth.authentication_context import AuthenticationContext
from dotenv import set_key,dotenv_values
from dotenv import load_dotenv
load_dotenv()
env=dotenv_values(".env")
USERNAME=env["sharepoint_email"]
PASSWORD=env["sharepoint_password"]
SHAREPOINT_SITE=env['sharepoint_url_site']
SHAREPOINT_SITE_NAME=env['sharepoint_site_name']
SHAREPOINT_DOC=env['sharepoint_doc_library']

class SharePoint:
    
    def _auth(self):
        """
        :return: un objeto de conexión que se autentica con el nombre de usuario y la contraseña
        proporcionados para un sitio de SharePoint.
        """
        ssl._create_default_https_context=ssl._create_unverified_context
        auth_context = AuthenticationContext(SHAREPOINT_SITE)
        auth_context.acquire_token_for_user(USERNAME, PASSWORD)
        conn = ClientContext(SHAREPOINT_SITE, auth_context)
        #conn=ClientContext(SHAREPOINT_SITE).with_credentials(
        #    UserCredential(
        #        USERNAME,
        #        PASSWORD
        #    )
        #)
        return conn

    def _get_files_list(self,folder_name):
        """     
        :folder_name: El nombre de la carpeta en SharePoint para la que desea recuperar una lista de
        archivos
        :return: La función `_get_files_list` devuelve una lista de archivos en la carpeta de SharePoint
        especificada.
        """
        conn= self._auth()
        target_folder_url=f'{SHAREPOINT_DOC}/{folder_name}'
        root_folder=conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Files","Folders"]).get().execute_query()
        return root_folder.files
    def get_folder_list(self,folder_name):
        """
        :folder_name: El nombre de la carpeta para la que desea recuperar una lista de subcarpetas
        :return: La función `get_folder_list` devuelve una lista de carpetas dentro del nombre de carpeta
        especificado en SharePoint.
        """
        conn= self._auth()
        target_folder_url=f'{SHAREPOINT_DOC}/{folder_name}'
        root_folder=conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Folders"]).get().execute_query()
        return root_folder.folders


    def download_file(self,file_name,folder_name):
        """
        :file_name: El nombre del archivo que debe descargarse de SharePoint
        :folder_name: El nombre de la carpeta en la que se encuentra el archivo en SharePoint
        :return: Se devuelve el contenido del archivo con el nombre de archivo y el nombre de carpeta
        especificados en el sitio de SharePoint.
        """
        
        conn=self._auth()
        file_url=f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}/{file_name}'
        file=File.open_binary(conn,file_url)
        return file.content

    def upload_file(self,file_name,folder_name,content):
        """
        :file_name: El nombre del archivo que debe cargarse en SharePoint
        :folder_name: El nombre de la carpeta en la que se debe cargar el archivo
        :content: El parámetro de contenido es el contenido real del archivo que debe cargarse. Puede
        ser en forma de bytes o una cadena, según el tipo de archivo que se cargue
        :return: Se está devolviendo la respuesta de la operación de carga del archivo.
        """
        conn=self._auth()
        target_folder_url=f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}'
        target_folder=conn.web.get_folder_by_server_relative_path(target_folder_url)
        response= target_folder.upload_file(file_name,content).execute_query()   
        return response 
    def get_list(self,list_name):
        """
        :list_name: El nombre de la lista de SharePoint de la que desea recuperar datos
        :return: La función `get_list` devuelve una lista de elementos de una lista de SharePoint
        especificada por el parámetro `list_name`.
        """
        conn=self._auth()
        target_list=conn.web.lists.get_by_title(list_name)
        items= target_list.items.get().execute_query()
        return items
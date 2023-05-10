# Automatización diseños de migración de Tecnología



![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)


**Table of Contents**


*[Descripción del proyecto](#Descripción-del-proyecto)

*[Tecnologías](#Tecnología_utilizadas)

*[Librerias](#Librerias_utilizadas)

*[Instalación librerias](#Para-instalar-las-librerias)

*[Archivos del proyecto](#Archivos-del-proyecto)

* [config.py](#config)
* [Config_User.py](#Config_User)
* [download_list.py](#download_list)
* [Advertencia.py](#Advertencia)
* [Login_Final.py](#Login_Final)
* [Login.py](#Login)
* [search_files.py](#search_files)
* [Upload_Files.py](#Upload_Files)
* [Estructura_principal_FINAL.py](#Estructura_principal_FINAL)
* [main.py](#main)
* [office365_api.py](#office365_api)




### Descripción-del-proyecto
Este es un proyecto realizado con Python, el cual permite realizar subida de archivos Excel a listas de Sharepoint, descarga de listas de Sharepoint, esto con el fin de tener actualizada información acerca de los nodos que se estan utilizando y cuales estan disponibles para poder reemplazarlos a Remote PHY, en donde se tiene un apartado de filtrado de información, el cual se busca un nodo en especifíco y este va a generar un filtrado del nodo en caso de que este libre, con la respectiva información de los puertos DAAS y COS disponibles que se puedan utilzar mostrandolos en la UI.

 A su vez dependiendo del tipo de nodo que sea escogido, ya sea 1 x 2 ó 2 x 4, va a generar automaticamente un formato con el diseño del nodo, guardandose en una carpeta, permitiendo con un botón, subir todos los archivos a una carpeta de SharPoint.

Esto con el fin de optimizar tiempos al momento de actualizar la información de los nodos de la tecnología Arris y Casa, y los puertos disponibles que se pueden utilizar de los COS y DAAS, reduciendo los tiempos para generar los formatos de los diseños de nodos que se requieran.
### Tecnología_utilizadas 
- python 3.19

### Librerias_utilizadas   

- Office365-REST-Python-Client==2.3.13
- openpyxl==3.0.10
- pandas==1.5.3
- PyQt5==5.15.4
- pyqt5-plugins==5.15.4.2.2
- PyQt5-Qt5==5.15.2
- PyQt5-sip==12.11.1
- PyQt5Designer==5.14.1
- PySide2==5.15.2.1
- python-dateutil==2.8.2
- python-dotenv==0.21.1
- qt5-applications==5.15.2.2.2
- requests==2.28.1
----
# Para-instalar-las-librerias
1. Ir al cmd o terminal del editor
2. Posicionarse en la ruta de la carpeta del proyeto
3. Crear un entorno virtual  ` python -m venv env`
4. Activar el entorno virtual  ` env\Scripts\activate.bat`
5. Instalar las librerias  ` pip install -r requiriments_f.txt`


-------------
# Archivos-del-proyecto
## config
Este archivo contiene una clase llamada Ui_config, la cual tiene la codificación de toda la interfaz gráfica de la ventana de registro del programa, donde estan los siguientes componentes:
- label4: Texto de registro de usuario
- lineEdit: Espacio para registrar usuario
- lineEdit_2: Espacio para registrar el password
- lineEdit_3: Espacio para confirmar el password
- Login_button: Botón para guardar las configuraciones
- checkBox: Caja para visualizar el contenido de los password 
## Config_User
Este archivo contiene una clase llamada ConfigUsuarioView, la cual tiene la codificación del funcionamiento de la interfaz gráfica, este archivo esta dividido en varias funciones:
- __init__(self): Esta función inicializa y coloca parametros escenciales 
- generar_formulario(self): Esta función, se configuran los botones y checkBox de la UI
- mostrar_pass(self,clicked): Esta función le entra como parametro si fue presionado o no el checkbox, mostrando o no el texto que se introduce.
- cancelar(self): cierra la ventana
- configurar_usuario(self): Hace la comparación de los campos que se requieren para registrar o mostrar un mensaje de error.
## download_list
Este archivo contiene varias funciones, que le permite descargar una lista en especifíco de Sharepoint:
- Type_file(file_name,export_type): Esta función revisa el tipo de archivo que se predetermine y dependiendo si es uno u otro, adjunto esa extesión mas el nombre de archivo que recibe como parametro.
- download_list(list_name,export_type,dir_path,file_name): Esta función, 
Dependiendo del tipo de archivo que sea, va ejecutar la función para guardar un archivo Excel ó CSV.
- mostrar_pass(self,clicked): Esta función le entra como parametro si fue presionado o no el checkbox, mostrando o no el texto que se introduce.
- save_Execel(list_items,dir_path,file_name): Esta función, de los datos obtenidos de la lista de SharePoint que se quiere descargar, va a comenzar a escribir en un archivo Excel los datos, ademas de revisar cada uno de los archivos para que filtre y solo se obtenga el archivo con la información necesaria.
## Advertencia
Este archivo contiene una clase llamada Ui_ADVERTENCIA, el cual contiene todas los parametros de la UI, además de funciones que realiza los botones que contiene:

- self.label: Contiene un mensaje que se muestra en la ventana emergente.
- self.pushButton: Ejecuta la función para subir los archivos de los Diseños
- self.pushButton_2: Cierra la ventana emergente y no realiza ninguna subida de archivos
- upload_file(self): Esta función,llama del archivo Upload_Files.py la función upload_files, para subir los archivos de los diseños a una carpeta del SharPoint.
- no(self): Cierra la ventana
## Login_Final
Este archivo contiene una clase llamada Ui_Form, la cual tiene la codificación de toda la interfaz gráfica de la ventana de inicio del programa, donde estan los siguientes componentes:
- label4: Texto de inicio de usuario
- lineEdit: Espacio para registrar usuario
- lineEdit_2: Espacio para registrar el password
- Login_button: Botón para guardar realizar el Login
- checkBox: Caja para visualizar el contenido de los password
- Config_button: Botón para entrar a la ventana de configuración de usuario.
## Login
Este archivo contiene una clase llamada Login, la cual tiene la codificación del funcionamiento de la interfaz gráfica, este archivo esta dividido en varias funciones:
- __init__(self): Esta función inicializa y coloca parametros escenciales 
- generar_formulario(self): Esta función, se configuran los botones y checkBox de la UI
- mostrar_pass(self,clicked): Esta función le entra como parametro si fue presionado o no el checkbox, mostrando o no el texto que se introduce.
- control_close(self): cierra la ventana
- login(self):revisa si en el archivo de users esta los nombres registrados.
- open_main(self): Abre el programa principal
- config_usuario(self): Abre la ventana de configuración de usuario
## search_files
Este archivo contiene una clase llamada Search, la cual esta en un archivo aparte para ejecutarse en paralelo y no congelar la UI.
- buscar_archivo(self,name_file,ruta):Esta función, busca los archivos con los nombres que estan en una lista y ademas que tengan la extensión ".xlsx"
## Upload_Files
Este archivo tiene funciones las cuales permiten realizar una subida de archivos de una carpeta del PC, a una carpeta de SharePoint.
- upload_files(folder,keyword=None):Esta función carga archivos en una carpeta de SharePoint en función de una palabra clave específica o de todos los archivos de una carpeta.
    filtrar los archivos que se cargan en función de una palabra clave específica. Si se proporciona una palabra clave, solo se cargarán los archivos que contengan la palabra clave en su nombre de archivo.
    Si no se proporciona ninguna palabra clave o si la palabra clave se establece en 'Ninguna', todos
    los archivos.
- get_list_of_files(folder): Esta función toma la ruta de una carpeta como entrada y devuelve una   lista de archivos dentro de esa carpeta junto con sus rutas completas.
- get_file_content(file_path): Esta función lee el contenido de un archivo en modo binario y lo devuelve.
## Estructura_principal_FINAL
Este archivo contiene una clase llamada principal del programa, donde estan los siguientes componentes:
- bt_inicio: Botón para entrar a la ventana principal
- bt_base_datos: Botón para la ventana de subir los datos a lista de SharePoint
- bt_list: Botón para la ventana de descarga los datos a lista de SharePoint
- bt_confi: Botón para la ventana de configuraciones de parametros
- label_21: Texto en la ventana(page_tres) "DESPUES" 
- label_22: Texto en la ventana(page_tres) "COS"
- label_23: Texto en la ventana(page_tres) "DAAS"
- label_17: Texto en la ventana(page_tres) "ANTES"
- label_19: Texto en la ventana(page_tres) "DISEÑO NODOS"
- lineEdit_buscar: Espacio para buscar el nodo deseado 
- bt_filtrar: Botón que ejecuta las funciones para mostrar los datos en los Qtable y realiza el filtrado
- bt_search_files: Botón para buscar los archivos necesarios en el PC, para realizar el filtrado
- bt_upload_file: Botón que abre una ventana emergente para subir los Diseños creados
- label_27:Texto en la ventana(page_uno) "DESCARGA DE LISTAS"
- lineEdit_descargar_lista: Espacio para insertar el nombre de la lista que se desea descargar
- label_28:Texto en la ventana(page_uno) "GUARDAR COMO"
- download_LIST: Botón para llamar la función download_list, del archivo download_lists.py 
- comboBox: Espacio para seleccionar los nombres disponibles, del archivo de la lista que se desee descargar de SharePoint
- comboBox2: Espacio para seleccionar el tipo de nodo el cual va a tomar el diseño para realizar el diseño
- label_29:Texto en la ventana(page_dos) "SUBIR LISTA A SHAREPOINT"
- lineEdit_buscar_2: Espacio para insertar el nombre de la lista que se desea subir los datos
- bt_filtrar_2: Espacio que ejecuta la función upload_LIST
- search_files: Botón para abrir el buscador de Windows para buscar el archivo .xlsx que se desea subir
- bt_stop: Botón que ejecuta la función cancelar_stop
- label_15:Texto en la ventana(page_cuatro) "Adicione una vez mas este caracter \'\\\' , a la ruta como este ejemplo: C:-->\\\\<--Users\\PC\\Desktop"
- label_16:Texto en la ventana(page_cuatro) "CONFIGURACION"
- label_17:Texto en la ventana(page_cuatro) "Ejemplo: https://claromovilco.sharepoint.com/sites/nombre_sitio_SharePoint/" "
- lineEdit_site_Sharepoint: Espacio para configurar el Path donde se va a guardar el sitio de SharePoint y se guardara en el archivo .env
- lineEdit_folder_subir_archivo: Espacio para configurar el nombre de la carpeta donde se va a guardar los archivos de los diseños en SharePoint y se guardara en el archivo .env
- lineEdit_Path_lists: Espacio para configurar el Path donde se va a guardar el sitio donde se guardaran todos los archivos y se guardara en el archivo .env
- bt_save_con: Botón para guardar los parametros.
## main
Este archivo contiene una clase llamada MiApp, la cual tiene la codificación del funcionamiento de la interfaz gráfica, este archivo esta dividido en varias funciones:
- __init__(self): Esta función inicializa y coloca parametros escenciales 
-abrir_archivo(self): Esta función abre un cuadro de diálogo de archivo para seleccionar un archivo de Excel
- complet_COS(self,df): La función agrega los puertos faltantes a un marco de datos y devuelve el marco de datos actualizado.
- complete_DAAS(self,df): La función agrega filas a un DataFrame para dispositivos a los que les faltan puertos y ordena el DataFrame resultante por dispositivo y puerto.
- simpli_DAAS(self,df): Toma varias columnas del Dataframe de DAAS para regresar variables que sirven para filtrar.
- filtrado_COS_DAAS(self): Recibe todos los Dataframes, y regresa en el antes el nodo filtrado, y en el despues los disponibles del COS y el DAAS, ademas de llamar a la función para que realice los archivos de diseños.
- mostrar_tabla(self): Crea tres hilos escencialmente para ejecutar en paralelo el filtrado y la interfaz gráfica.
- crear_tabla(self): Crea una tabla del antes, para mostrarlos en una interfaz gráfica.
- crear_despues_COS(self): Crea una tabla del despues COS, para mostrarlos en una interfaz gráfica.
- crear_despues_DAAS(self): Crea una tabla del despues DAAS, para mostrarlos en una interfaz gráfica.
- control_bt_minimizar(self): Minimiza la ventana cuando ejecute el evento el botón.
- control_close(self): Cierra la ventana
- upload_file(self): llama del archivo Upload_files.py la clase Ui_ADVERTENCIA y lo muestra en la ventana principal.
- cancelar_stop(self): Esta función cancela la subida de datos a lista de SharePoint.
- seleccion_archivo(self): Guarda el nombre de como se va a descargar la lista 
- seleccion_archivo(self): Guarda el tipo de nodo que se va a generar el diseño
- upload_LIST(self): La función crea un hilo para cargar una lista
-  obtener_dataframes(self,name_files,ruta_de_busqueda): Esta función busca archivos específicos en un directorio determinado y devuelve sus datos como marcos de datos de pandas.
- obtener_dataframes(self,name_files,ruta_de_busqueda): Esta función lee datos de archivos de Excel y devuelve cuatro marcos de datos.
- search_file_filter(self): Esta función busca archivos en función de un filtro
- subir_list(self): Esta función carga datos de un archivo de Excel a una lista de SharePoint, maneja interrupciones y descoexniones y vuelve a intentar intentos fallidos.
- save_path_list(self): Esta función establece una nueva ruta de descarga para una lista de archivos y la guarda en un archivo .env
- save_parameters_url_sharepoint(self): Esta función establece una nueva ruta de el sitio de SharePint donde se realizara todo el procedimiento y la guarda en un archivo .env
- save_parameters_name_folder_Sharepoint(self): Esta función establece una nueva ruta de la carpeta de SharePint donde se guardaran los .xlsx de los diseños generados y la guarda en un archivo .env
## office365_api
Este archivo contiene funciones, principalmente, para la descarga de las listas  y para la subida de archivos al Sharepoint
- def _auth(self): Esta función crea una conexión a un sitio de SharePoint utilizando un nombre de usuario y una contraseña proporcionados.
- _get_files_list(self,folder_name): Esta función recupera una lista de archivos de una carpeta de SharePoint específica mediante la API de Microsoft Graph.
- get_folder_list(self,folder_name): Esta función recupera una lista de carpetas dentro de una carpeta específica en SharePoint.
- download_file(self,file_name,folder_name):Esta función descarga un archivo de un sitio de SharePoint dado el nombre del archivo y el nombre de la carpeta.
- upload_file(self,file_name,folder_name,content): Esta función carga un archivo en una carpeta específica en un sitio de SharePoint.
- get_list(self,list_name): Esta función recupera todos los elementos de una lista de SharePoint con un nombre dado.

## Prueba_formato
Este archivo contiene diferentes funcionalidades que utiliza principalmente de la libreria, openpyxl, especificamente de openpyxl.styles, en donde se genera el diseño de los nodos, dependiendo si se selecciona un nodo 1 x 2 ó 2 x 4, obteniendo texto del resultado final del Dataframe filtrado, caracterizando las celdas necesarias con color de fondo, rellenos, contorno, tipo de letra, tamaño de celda, tamaño de texto, ajustandose la información en el espacio de "SCRIPT  ANTES-NOC CABLE",dependiendo de la cantidad de información que tenga un nodo, seleccionando un puerto en especifico dentro de los disponibles y coincidentes entre el dispositivo COS y el dispositivo DAAS, y dejando solo uno para el diseño final. 

                
----

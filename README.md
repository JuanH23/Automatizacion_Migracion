# Automatización diseños de migración de Tecnología
### Features

# Editor.md

![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)


**Table of Contents**


*[Descripción del proyecto](#Descripción-del-proyecto)

*[Tecnologías](#Tecnología_utilizadas)

*[Librerias](#Librerias_utilizadas)

*[Instalación librerias](#Para-instalar-las-librerias)

*[Archivos del proyecto](#Archivos-del-proyecto)

* [config.py](#config.py)
* [Config_User.py](#Config_User.py)
* [download_list.py](#download_list.py)
* [Advertencia.py](#Advertencia.py)
* [Login_Final.py](#Login_Final.py)
* [Login.py](#Login.py)
* [search_files.py](#search_files.py)
* [Upload_Files.py](#Upload_Files.py)





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
## config.py
Este archivo contiene una clase llamada Ui_config, la cual tiene la codificación de toda la interfaz gráfica de la ventana de registro del programa, donde estan los siguientes componentes:
- label4: Texto de registro de usuario
- lineEdit: Espacio para registrar usuario
- lineEdit_2: Espacio para registrar el password
- lineEdit_3: Espacio para confirmar el password
- Login_button: Botón para guardar las configuraciones
- checkBox: Caja para visualizar el contenido de los password 
## Config_User.py
Este archivo contiene una clase llamada ConfigUsuarioView, la cual tiene la codificación del funcionamiento de la interfaz gráfica, este archivo esta dividido en varias funciones:
- __init__(self): Esta función inicializa y coloca parametros escenciales 
- generar_formulario(self): Esta función, se configuran los botones y checkBox de la UI
- mostrar_pass(self,clicked): Esta función le entra como parametro si fue presionado o no el checkbox, mostrando o no el texto que se introduce.
- cancelar(self): cierra la ventana
- configurar_usuario(self): Hace la comparación de los campos que se requieren para registrar o mostrar un mensaje de error.
## download_list.py
Este archivo contiene varias funciones, que le permite descargar una lista en especifíco de Sharepoint:
- Type_file(file_name,export_type): Esta función revisa el tipo de archivo que se predetermine y dependiendo si es uno u otro, adjunto esa extesión mas el nombre de archivo que recibe como parametro.
- download_list(list_name,export_type,dir_path,file_name): Esta función, 
Dependiendo del tipo de archivo que sea, va ejecutar la función para guardar un archivo Excel ó CSV.
- mostrar_pass(self,clicked): Esta función le entra como parametro si fue presionado o no el checkbox, mostrando o no el texto que se introduce.
- save_Execel(list_items,dir_path,file_name): Esta función, de los datos obtenidos de la lista de SharePoint que se quiere descargar, va a comenzar a escribir en un archivo Excel los datos, ademas de revisar cada uno de los archivos para que filtre y solo se obtenga el archivo con la información necesaria.
## Advertencia.py
Este archivo contiene una clase llamada Ui_ADVERTENCIA, el cual contiene todas los parametros de la UI, además de funciones que realiza los botones que contiene:

- self.label: Contiene un mensaje que se muestra en la ventana emergente.
- self.pushButton: Ejecuta la función para subir los archivos de los Diseños
- self.pushButton_2: Cierra la ventana emergente y no realiza ninguna subida de archivos
- upload_file(self): Esta función,llama del archivo Upload_Files.py la función upload_files, para subir los archivos de los diseños a una carpeta del SharPoint.
- no(self): Cierra la ventana
## Login_Final.py
Este archivo contiene una clase llamada Ui_Form, la cual tiene la codificación de toda la interfaz gráfica de la ventana de inicio del programa, donde estan los siguientes componentes:
- label4: Texto de inicio de usuario
- lineEdit: Espacio para registrar usuario
- lineEdit_2: Espacio para registrar el password
- Login_button: Botón para guardar realizar el Login
- checkBox: Caja para visualizar el contenido de los password
- Config_button: Botón para entrar a la ventana de configuración de usuario.
## Login.py
Este archivo contiene una clase llamada Login, la cual tiene la codificación del funcionamiento de la interfaz gráfica, este archivo esta dividido en varias funciones:
- __init__(self): Esta función inicializa y coloca parametros escenciales 
- generar_formulario(self): Esta función, se configuran los botones y checkBox de la UI
- mostrar_pass(self,clicked): Esta función le entra como parametro si fue presionado o no el checkbox, mostrando o no el texto que se introduce.
- control_close(self): cierra la ventana
- login(self):revisa si en el archivo de users esta los nombres registrados.
- open_main(self): Abre el programa principal
- config_usuario(self): Abre la ventana de configuración de usuario
## search_files.py
Este archivo contiene una clase llamada Search, la cual esta en un archivo aparte para ejecutarse en paralelo y no congelar la UI.
- buscar_archivo(self,name_file,ruta):Esta función, busca los archivos con los nombres que estan en una lista y ademas que tengan la extensión ".xlsx"
## Upload_Files.py
Este archivo tiene funciones las cuales permiten realizar una subida de archivos de una carpeta del PC, a una carpeta de SharePoint.
- upload_files(folder,keyword=None):Esta función carga archivos en una carpeta de SharePoint en función de una palabra clave específica o de todos los archivos de una carpeta.
    filtrar los archivos que se cargan en función de una palabra clave específica. Si se proporciona una palabra clave, solo se cargarán los archivos que contengan la palabra clave en su nombre de archivo.
    Si no se proporciona ninguna palabra clave o si la palabra clave se establece en 'Ninguna', todos
    los archivos.
- get_list_of_files(folder): Esta función toma la ruta de una carpeta como entrada y devuelve una   lista de archivos dentro de esa carpeta junto con sus rutas completas.
- get_file_content(file_path): Esta función lee el contenido de un archivo en modo binario y lo devuelve.



                
----

~~Strikethrough~~ <s>Strikethrough (when enable html tag decode.)</s>
*Italic*      _Italic_
**Emphasis**  __Emphasis__
***Emphasis Italic*** ___Emphasis Italic___

Superscript: X<sub>2</sub>，Subscript: O<sup>2</sup>

**Abbreviation(link HTML abbr tag)**

The <abbr title="Hyper Text Markup Language">HTML</abbr> specification is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.

###Blockquotes

> Blockquotes

Paragraphs and Line Breaks
                    
> "Blockquotes Blockquotes", [Link](http://localhost/)。

###Links

[Links](http://localhost/)

[Links with title](http://localhost/ "link title")

`<link>` : <https://github.com>

[Reference link][id/name] 

[id/name]: http://link-url/

GFM a-tail link @pandao

###Code Blocks (multi-language) & highlighting

####Inline code

`$ npm install marked`

####Code Blocks (Indented style)

Indented 4 spaces, like `<pre>` (Preformatted Text).

    <?php
        echo "Hello world!";
    ?>
    
Code Blocks (Preformatted text):

    | First Header  | Second Header |
    | ------------- | ------------- |
    | Content Cell  | Content Cell  |
    | Content Cell  | Content Cell  |

####Javascript　



####HTML code

```html
<!DOCTYPE html>
<html>
    <head>
        <mate charest="utf-8" />
        <title>Hello world!</title>
    </head>
    <body>
        <h1>Hello world!</h1>
    </body>
</html>
```


###Lists

####Unordered list (-)

- Item A
- Item B
- Item C
     
####Unordered list (*)

* Item A
* Item B
* Item C

####Unordered list (plus sign and nested)
                
+ Item A
+ Item B
    + Item B 1
    + Item B 2
    + Item B 3
+ Item C
    * Item C 1
    * Item C 2
    * Item C 3

####Ordered list
                
1. Item A
2. Item B
3. Item C
                
----
                    
###Tables
                    
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell 

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

| Function name | Description                    |
| ------------- | ------------------------------ |
| `help()`      | Display the help window.       |
| `destroy()`   | **Destroy your computer!**     |

| Item      | Value |
| --------- | -----:|
| Computer  | $1600 |
| Phone     |   $12 |
| Pipe      |    $1 |

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |
                
----



###Emoji mixed :smiley:

> Blockquotes :star:

####GFM task lists & Emoji & fontAwesome icon emoji & editormd logo emoji :editormd-logo-5x:

- [x] :smiley: @mentions, :smiley: #refs, [links](), **formatting**, and <del>tags</del> supported :editormd-logo:;
- [x] list syntax required (any unordered or ordered list supported) :editormd-logo-3x:;
- [x] [ ] :smiley: this is a complete item :smiley:;
- [ ] []this is an incomplete item [test link](#) :fa-star: @pandao; 
- [ ] [ ]this is an incomplete item :fa-star: :fa-gear:;
    - [ ] :smiley: this is an incomplete item [test link](#) :fa-star: :fa-gear:;
    - [ ] :smiley: this is  :fa-star: :fa-gear: an incomplete item [test link](#);
 
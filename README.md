# Automatización diseños de migración de Tecnología
### Features

# Editor.md

![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)


**Table of Contents**
##Índice

*[Features](#Features)

*[Tecnologías](#Tecnología_utilizadas :smiley: )

*[Librerias](#Librerias_utilizadas)

*[Instalación librerias](#Para-instalar-las-librerias)

*[Archivos del proyecto](#Archivos-del-proyecto)

* [config.py](#config.py)

*[Características de la aplicación y demostración](#Características-de-la-aplicación-y-demostración)

*[Acceso al proyecto](#acceso-proyecto)

*[Tecnologías utilizadas](#tecnologías-utilizadas)

*[Personas Contribuyentes](#personas-contribuyentes)

*[Personas-Desarrolladores del Proyecto](#personas-desarrolladores)

* [Licencia](#licencia)

*[Editor.md](# Editor.md)



### Tecnología_utilizadas :smiley: 
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
###Characters
                
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
 
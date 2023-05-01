# Automatización diseños de migración de Tecnología
### Features

# Editor.md

![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)


**Table of Contents**
##Índice

*[Features](#Features)

*[Tecnologías](#Tecnología_utilizadas)

*[Librerias](#Librerias_utilizadas)

*[Instalación librerias](#Para-instalar-las-librerias)

*[Estado del proyecto](#Estado-del-proyecto)

*[Características de la aplicación y demostración](#Características-de-la-aplicación-y-demostración)

*[Acceso al proyecto](#acceso-proyecto)

*[Tecnologías utilizadas](#tecnologías-utilizadas)

*[Personas Contribuyentes](#personas-contribuyentes)

*[Personas-Desarrolladores del Proyecto](#personas-desarrolladores)

* [Licencia](#licencia)

*[Editor.md](# Editor.md)



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

=============


-------------
# Archivos-del-proyecto
## config.py
```python
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_config(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 550)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(40, 70, 370, 480))
        self.widget.setStyleSheet("QPushButton#Login_button:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"QPushButton#Login_button:hover{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgb(9, 121, 226), stop:1 rgb(105, 118, 132));\n"
"}\n"
"QPushButton#Login_button{\n"
"\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:15px;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"QPushButton#Close_button{\n"
"\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:8px;\n"
"}\n"
"QPushButton#Close_button:pressed{\n"
"padding-left:1px;\n"
"padding-top:1px;\n"
"background-color:rgba(105, 118, 132, 200);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 30, 300, 420))
        self.label.setStyleSheet("background-image: url(images/images/BG-9.jpg);\n"
"border-radius:20px")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(80, 90, 231, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily(u"Segoe UI Semibold")
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("")
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 165, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setFamily(u"Segoe UI Semibold")
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:None;\n"
"border-bottom:2px solid rgb(0,0,0);\n"
"\n"
"padding-bottom:7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 230, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:None;\n"
"border-bottom:2px solid rgb(0,0,0);;\n"
"\n"
"padding-bottom:7px;")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 300, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:None;\n"
"border-bottom:2px solid rgb(0,0,0);;\n"
"\n"
"padding-bottom:7px;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.Login_button = QtWidgets.QPushButton(self.widget)
        self.Login_button.setGeometry(QtCore.QRect(80, 390, 200, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily(u"Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.Login_button.setFont(font)
        self.Login_button.setStyleSheet("")
        self.Login_button.setObjectName("Login_button")
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setGeometry(QtCore.QRect(80, 350, 181, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(u"Segoe UI Semibold")
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.Close_button = QtWidgets.QPushButton(self.widget)
        self.Close_button.setGeometry(QtCore.QRect(290, 50, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Close_button.setFont(font)
        self.Close_button.setStyleSheet("")
        self.Close_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/cerca.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close_button.setIcon(icon)
        self.Close_button.setObjectName("Close_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Registro usuario"))
        self.lineEdit.setPlaceholderText(_translate("Form", "User Name"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Password"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "Confirme Password"))
        self.Login_button.setText(_translate("Form", "Guardar"))
        self.checkBox.setText(_translate("Form", "Ver Password"))
if __name__ == "__main__":    
    app=QtWidgets.QApplication(sys.argv)
    Form=QtWidgets.QWidget()
    ui=Ui_config()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
```
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
 
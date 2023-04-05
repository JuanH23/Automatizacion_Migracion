# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'estructura_principal.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *
from dotenv import set_key,dotenv_values
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(814, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_Sup = QtWidgets.QFrame(self.centralwidget)
        self.frame_Sup.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_Sup.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_Sup.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.frame_Sup.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Sup.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Sup.setObjectName("frame_Sup")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_Sup)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.bt_menu = QtWidgets.QPushButton(self.frame_Sup)
        self.bt_menu.setMinimumSize(QtCore.QSize(200, 35))
        self.bt_menu.setMaximumSize(QtCore.QSize(16777215, 35))
        self.bt_menu.setStyleSheet("QPushButton{\n"
"backgroud-color:#aa00ff;\n"
"font:87 12pt \"Arial Black\";\n"
"border radius:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"font:87 12pt \"Arial Black\";\n"
"background-color:white;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_menu.setIcon(icon)
        self.bt_menu.setObjectName("bt_menu")
        self.horizontalLayout_2.addWidget(self.bt_menu)
        spacerItem = QtWidgets.QSpacerItem(519, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.bt_minimizar = QtWidgets.QPushButton(self.frame_Sup)
        self.bt_minimizar.setMaximumSize(QtCore.QSize(16777215, 35))
        self.bt_minimizar.setStyleSheet("QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:white;\n"
"}")
        self.bt_minimizar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/minimizar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_minimizar.setIcon(icon1)
        self.bt_minimizar.setObjectName("bt_minimizar")
        self.horizontalLayout_2.addWidget(self.bt_minimizar)
        self.bt_restaurar = QtWidgets.QPushButton(self.frame_Sup)
        self.bt_restaurar.setMaximumSize(QtCore.QSize(16777215, 35))
        self.bt_restaurar.setStyleSheet("QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:white;\n"
"}")
        self.bt_restaurar.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/cuadricula.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_restaurar.setIcon(icon2)
        self.bt_restaurar.setObjectName("bt_restaurar")
        self.horizontalLayout_2.addWidget(self.bt_restaurar)
        self.bt_max = QtWidgets.QPushButton(self.frame_Sup)
        self.bt_max.setMaximumSize(QtCore.QSize(16777215, 35))
        self.bt_max.setStyleSheet("QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:white;\n"
"}")
        self.bt_max.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/expandir.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_max.setIcon(icon3)
        self.bt_max.setObjectName("bt_max")
        self.horizontalLayout_2.addWidget(self.bt_max)
        self.bt_close = QtWidgets.QPushButton(self.frame_Sup)
        self.bt_close.setMaximumSize(QtCore.QSize(16777215, 35))
        self.bt_close.setStyleSheet("QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:white;\n"
"}")
        self.bt_close.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/cerrar-el-simbolo-de-la-cruz-en-un-circulo (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_close.setIcon(icon4)
        self.bt_close.setObjectName("bt_close")
        self.horizontalLayout_2.addWidget(self.bt_close)
        self.verticalLayout.addWidget(self.frame_Sup)
        self.frame_Inf = QtWidgets.QFrame(self.centralwidget)
        self.frame_Inf.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Inf.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Inf.setObjectName("frame_Inf")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_Inf)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_lateral = QtWidgets.QFrame(self.frame_Inf)
        self.frame_lateral.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_lateral.setMaximumSize(QtCore.QSize(0, 16777215))
        self.frame_lateral.setStyleSheet("QFrame{\n"
"background-color:#d50000;\n"
"}"
"QPushButton{\n"
"background-color:#d50000;\n"
"boder-top-left-radius:20px;\n"
"border-bottom-left-radius:20px;"
"font:75 12pt \"Arial Narrow\";\n"
"}\n"
"QPushButton:hover{\n"
"background-color:white;\n"
"boder-top-left-radius:20px;\n"
"border-bottom-left-radius:20px;\n"
"\n"
"font:75 12pt \"Arial Narrow\";\n"
"}\n"
"")
        self.frame_lateral.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_lateral.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_lateral.setObjectName("frame_lateral")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_lateral)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.bt_inicio = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_inicio.setMinimumSize(QtCore.QSize(0, 40))
        self.bt_inicio.setMaximumSize(QtCore.QSize(16777215, 40))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/hogar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_inicio.setIcon(icon5)
        self.bt_inicio.setObjectName("bt_inicio")
        self.verticalLayout_3.addWidget(self.bt_inicio)
        self.bt_list = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_list.setMinimumSize(QtCore.QSize(0, 40))
        self.bt_list.setMaximumSize(QtCore.QSize(16777215, 40))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/flecha-hacia-abajo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_list.setIcon(icon6)
        self.bt_list.setObjectName("bt_list")
        self.verticalLayout_3.addWidget(self.bt_list)
        self.bt_base_datos = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_base_datos.setMinimumSize(QtCore.QSize(0, 40))
        self.bt_base_datos.setMaximumSize(QtCore.QSize(16777215, 40))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/flecha-hacia-arriba.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_base_datos.setIcon(icon7)
        self.bt_base_datos.setObjectName("bt_base_datos")
        self.verticalLayout_3.addWidget(self.bt_base_datos)
        self.bt_congif = QtWidgets.QPushButton(self.frame_lateral)
        self.bt_congif.setMinimumSize(QtCore.QSize(0, 40))
        self.bt_congif.setMaximumSize(QtCore.QSize(16777215, 40))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/configuraciones.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bt_congif.setIcon(icon8)
        self.bt_congif.setObjectName("bt_congif")
        self.verticalLayout_3.addWidget(self.bt_congif)
        spacerItem1 = QtWidgets.QSpacerItem(20, 360, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.frame_lateral)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout.addWidget(self.frame_lateral)
        self.frame_2 = QtWidgets.QFrame(self.frame_Inf)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_2)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_uno = QtWidgets.QWidget()
        self.page_uno.setObjectName("page_uno")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_uno)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.page_uno)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_4.setMouseTracking(False)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.label_2 = QtWidgets.QLabel(self.page_uno)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.lineEdit_descargar_lista = QtWidgets.QLineEdit(self.page_uno)
        self.lineEdit_descargar_lista.setObjectName("lineEdit_descargar_lista")
        self.verticalLayout_4.addWidget(self.lineEdit_descargar_lista)
        self.label_3 = QtWidgets.QLabel(self.page_uno)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.page_uno)
        self.comboBox.setGeometry(QtCore.QRect(100, 80, 211, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout_4.addWidget(self.comboBox)
        self.lineEdit_nombre_lista = QtWidgets.QLineEdit(self.page_uno)
        self.lineEdit_nombre_lista.setObjectName("lineEdit_nombre_lista")
        self.verticalLayout_4.addWidget(self.lineEdit_nombre_lista)
        self.download_LIST = QtWidgets.QPushButton(self.page_uno)
        self.download_LIST.setObjectName("download_LIST")
        self.verticalLayout_4.addWidget(self.download_LIST)
        self.progressBar = QtWidgets.QProgressBar(self.page_uno)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_4.addWidget(self.progressBar)
        self.stackedWidget.addWidget(self.page_uno)
        self.page_dos = QtWidgets.QWidget()
        self.page_dos.setObjectName("page_dos")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page_dos)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_10 = QtWidgets.QLabel(self.page_dos)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(16)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_6.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.page_dos)
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("images/claro.jpg"))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_6.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.page_dos)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_6.addWidget(self.label_12)
        self.lineEdit_buscar_2 = QtWidgets.QLineEdit(self.page_dos)
        self.lineEdit_buscar_2.setObjectName("lineEdit_buscar_2")
        self.verticalLayout_6.addWidget(self.lineEdit_buscar_2)
        self.bt_buscar_archivo=QtWidgets.QPushButton(self.page_dos)
        font=QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.bt_buscar_archivo.setFont(font)
        self.bt_buscar_archivo.setObjectName("bt_buscar_archivo")
        self.verticalLayout_6.addWidget(self.bt_buscar_archivo)
        self.bt_filtrar_2 = QtWidgets.QPushButton(self.page_dos)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.bt_filtrar_2.setFont(font)
        self.bt_filtrar_2.setObjectName("bt_filtrar_2")
        self.verticalLayout_6.addWidget(self.bt_filtrar_2)
        self.bt_cancelar = QtWidgets.QPushButton(self.page_dos)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.bt_cancelar.setFont(font)
        self.bt_cancelar.setObjectName("bt_cancelar")
        self.verticalLayout_6.addWidget(self.bt_cancelar)
        self.progressBar_2 = QtWidgets.QProgressBar(self.page_dos)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")
        self.verticalLayout_6.addWidget(self.progressBar_2)
        self.stackedWidget.addWidget(self.page_dos)
        self.page_tres = QtWidgets.QWidget()
        self.page_tres.setObjectName("page_tres")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_tres)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.page_tres)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.label_9 = QtWidgets.QLabel(self.page_tres)
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap("images/claro.jpg"))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_5.addWidget(self.label_9)
        self.label_8 = QtWidgets.QLabel(self.page_tres)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.lineEdit_buscar = QtWidgets.QLineEdit(self.page_tres)
        self.lineEdit_buscar.setObjectName("lineEdit_buscar")
        self.verticalLayout_5.addWidget(self.lineEdit_buscar)
        self.bt_filtrar = QtWidgets.QPushButton(self.page_tres)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.bt_filtrar.setFont(font)
        self.bt_filtrar.setObjectName("bt_filtrar")
        self.verticalLayout_5.addWidget(self.bt_filtrar)

        self.bt_upload_file = QtWidgets.QPushButton(self.page_tres)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.bt_upload_file.setFont(font)
        self.bt_upload_file.setObjectName("bt_upload_file")
        self.verticalLayout_5.addWidget(self.bt_upload_file)
        '''self.bt_Up_file = QtWidgets.QPushButton(self.page_tres)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.bt_Up_file.setFont(font)
        self.bt_Up_file.setObjectName("bt_UP_file")
        self.verticalLayout_5.addWidget(self.bt_Up_file)'''
        self.label_6 = QtWidgets.QLabel(self.page_tres)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.tableWidget = QtWidgets.QTableWidget(self.page_tres)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_5.addWidget(self.tableWidget)
        self.label_7 = QtWidgets.QLabel(self.page_tres)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_5.addWidget(self.label_7)
        self.tabla = QtWidgets.QTableWidget(self.page_tres)
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(0)
        self.tabla.setRowCount(0)
        self.verticalLayout_5.addWidget(self.tabla)
        self.stackedWidget.addWidget(self.page_tres)
        self.page_cuatro = QtWidgets.QWidget()
        self.page_cuatro.setObjectName("page_cuatro")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_cuatro)
        self.stackedWidget.addWidget(self.page_cuatro)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame_Inf)
        
        self.label_path_list = QtWidgets.QLabel(self.page_cuatro)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.label_path_list.setFont(font)
        self.label_path_list.setAlignment(QtCore.Qt.AlignCenter)
        self.label_path_list.setObjectName("label_path_list")
        self.verticalLayout_7.addWidget(self.label_path_list)
        self.label_path_description = QtWidgets.QLabel(self.page_cuatro)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.label_path_description.setFont(font)
        self.label_path_description.setAlignment(QtCore.Qt.AlignCenter)
        self.label_path_description.setObjectName("label_path_list")
        self.verticalLayout_7.addWidget(self.label_path_description)
        self.lineEdit_path_list = QtWidgets.QLineEdit(self.page_cuatro)
        self.lineEdit_path_list.setObjectName("lineEdit_path_list")
        self.verticalLayout_7.addWidget(self.lineEdit_path_list)
        self.bt_save_path_list = QtWidgets.QPushButton(self.page_cuatro)
        font = QtGui.QFont()
        font.setFamily("Lucida Bright")
        font.setPointSize(9)
        self.bt_save_path_list.setFont(font)
        self.bt_save_path_list.setObjectName("bt_save_path_list")
        self.verticalLayout_7.addWidget(self.bt_save_path_list)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        return self.lineEdit_buscar_2
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bt_menu.setText(_translate("MainWindow", "MENU"))
        self.bt_inicio.setText(_translate("MainWindow", "INICIO"))
        self.bt_list.setText(_translate("MainWindow", "DESCARGA LISTA"))
        self.bt_base_datos.setText(_translate("MainWindow", "SUBIR A BASE DE DATOS"))
        self.bt_congif.setText(_translate("MainWindow", "CONFIGURACIONES"))
        self.label.setText(_translate("MainWindow", "AUTOMATIZACION"))
        self.label_4.setText(_translate("MainWindow", "DESCARGA DE LISTAS"))
        self.label_2.setText(_translate("MainWindow", "Lista a descargar"))
        self.label_3.setText(_translate("MainWindow", "Guardar Como:    "))
        self.download_LIST.setText(_translate("MainWindow", "Descargar Lista"))
        self.label_10.setText(_translate("MainWindow", "SUBIR A BASE DE DATOS"))
        self.label_12.setText(_translate("MainWindow", "LISTA A SUBIR EN SHAREPOINT"))
        self.bt_buscar_archivo.setText(_translate("MainWindow","Buscar Archivo"))
        self.bt_filtrar_2.setText(_translate("MainWindow", "SUBIR"))
        self.bt_cancelar.setText(_translate("MainWindow", "Detener"))
        self.label_5.setText(_translate("MainWindow", "DISEÑO NODOS"))
        self.label_8.setText(_translate("MainWindow", "BUSCAR"))
        self.bt_filtrar.setText(_translate("MainWindow", "FILTRAR"))
        self.bt_upload_file.setText(_translate("MainWindow", "SUBIR ARCHIVO"))
        self.label_6.setText(_translate("MainWindow", "ANTES"))
        self.label_7.setText(_translate("MainWindow", "DESPUES"))
        self.bt_save_path_list.setText(_translate("MainWindow","Guardar Ruta"))
        self.label_path_list.setText(_translate("MainWindow","Ruta en donde va a guardar los archivos"))
        self.label_path_description.setText(_translate("MainWindow","Porfavor agregue una vez mas este caracter ' \\ ', a la ruta como este ejemplo: C:-->\\\<--Users\IC0167A\Desktop"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Elija nombre del archivo"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Arris_SCMSummary"))
        self.comboBox.setItemText(2, _translate("Mainwindow", "Casa_SCMSummary"))
        self.comboBox.setItemText(3, _translate("Mainwindow", "Ocupacion - Marcacion RPHY Harmonic"))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

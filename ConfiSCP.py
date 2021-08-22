# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 00:29:59 2020

@author: Enrique Ramos
"""
import PyQt5
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
import csv
import sys
import pandas as pd
import numpy as np

qtCreatorFile="Configuracion.ui"
Ui_QDialog, QtBaseClass=uic.loadUiType(qtCreatorFile)
class Configuracion_App(QtWidgets.QDialog, Ui_QDialog):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        
        self.configuracion()
        self.toolButton.clicked.connect(self.path_entrada)
        self.toolButton_2.clicked.connect(self.path_guardado)
        self.Save_Button.clicked.connect(self.guarda_valores)
        
    def configuracion(self): 
        with open ('ScorpConfig.txt', 'r') as config_file:
            Dato_Config=config_file.readlines()
        config_file.close()
        Dato_Con=[]
        for i in Dato_Config:
            if i != '\n':
                Dato_Con.append(i)
        Data=[]
        for i in Dato_Con:
            Data.append(i.split(';'))
        self.DirectIN.setText(Data[0][1])
        self.DirectSave.setText(Data[1][1])
        self.Assembly_Name.setText(Data[7][1])
        self.Board_Style.setText(Data[8][1])
        self.Equipo_Name.setText(Data[9][1])
        self.Data=Data
      
    def path_entrada(self):
        dir_default=str(QFileDialog.getExistingDirectory(self, "Select Directory")) 
        self.DirectIN.setText(dir_default)
        
    def path_guardado(self):
        dir_default=str(QFileDialog.getExistingDirectory(self, "Select Directory")) 
        self.DirectSave.setText(dir_default)
    
    def guarda_valores(self):
        "------------------------Lectura de datos en Configuracion------------"
        Confi_New=[]
        self.path_Open=str(self.DirectIN.text())
        Confi_New.append(self.path_Open)
        
        self.path_Save=str(self.DirectSave.text())
        Confi_New.append(self.path_Save)
        
        self.Customer=str(self.comboBox_CustomName.currentText())
        Confi_New.append(self.Customer)
        
        self.TesterName=str(self.comboBox_Tester_Name.currentText())
        Confi_New.append(self.TesterName)
        
        self.AsseRev=str(self.comboBox_5.currentText())
        Confi_New.append(self.AsseRev)
        
        self.TestProcess=str(self.comboBox_TestProcess.currentText())
        Confi_New.append(self.TestProcess)
        
        self.TestStatus=str(self.comboBox_TestStatus.currentText())
        Confi_New.append(self.TestStatus)
        
        self.AsseName=str(self.Assembly_Name.text())
        Confi_New.append(self.AsseName)
        
        self.BStyle=str(self.Board_Style.text())
        Confi_New.append(self.BStyle)
        
        self.Equipo_Name=str(self.Equipo_Name.text())
        Confi_New.append(self.Equipo_Name)
        
        self.SITE=str(self.Site.value())
        Confi_New.append(self.SITE)
        
        self.Line=str(self.Line.value())
        Confi_New.append(self.Line)
        print(Confi_New)
        
        for i in range(len(Confi_New)):
            self.Data[i][1]=Confi_New[i]
            
        for i in range(len(self.Data)):
            self.Data[i]=';'.join(self.Data[i])
        self.Data=[i.replace('\n', '') for i in (self.Data)]
        with open ('ScorpConfig.txt' , 'w') as confi:
            for i in self.Data:
                confi.write(str(i)+'\n')
        confi.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    windown=Configuracion_App()
    windown.show()
    sys.exit(app.exec_())
    # ex = Example()
    # sys.exit(app.exec_())


if __name__ == '__main__':
    main()
        
# if __name__=="__main__":
#     app=QtWidgets.QApplication(sys.argv)
#     windown=Configuracion_App()
#     windown.show()
#     sys.exit(app.exec_())


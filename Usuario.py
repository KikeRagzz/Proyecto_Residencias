# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 20:39:36 2020

@author: Enrique Ramos
"""
"Registro"
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import sys
from PruebaconLogin import *
 
QCreatorFile="Resgistro.ui"
Ui_QDialog, QtBaseClass = uic.loadUiType(QCreatorFile)

class Registro_user(QtWidgets.QDialog, Ui_QDialog):
    def __init__(self, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        self.Registro_Button.clicked.connect(self.validar_registro)
                    
    def validar_registro(self):
        if self.lineEdit.text() != '':
            with open ('Registro.txt', 'a') as Registro:
                Registro.write(self.lineEdit.text())
                Registro.write(':')
            Registro.close()
            QtWidgets.qApp.closeAllWindows()
            self.User=QtWidgets.QMainWindow()
            self.user=MyApp()
            self.user.show()   
        else:
            QMessageBox.information(self, "Usuario", "Favor de ingrese su numero \n"
                                    "de empleado para acceder", QMessageBox.Ok)
            
def main():
    app=QtWidgets.QApplication(sys.argv)
    windown=Registro_user()
    windown.setWindowIcon(QtGui.QIcon(str("scorpion-tail_38917.ico")))
    windown.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()


        

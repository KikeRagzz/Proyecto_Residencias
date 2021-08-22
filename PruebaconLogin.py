 #-*- coding: utf-8 -*-
"""
Created on Sat Jun 27 03:46:29 2020

@author: Enrique Ramos
"""
# """Interfaz con Qt desginer 
# """
import sys,os 
import re
import csv
import time
import numpy as np
import pandas as pd
from decimal import Decimal
from itertools import islice
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import * 
from ConfiSCP import Configuracion_App
#from Usuario import Registro_user

"Archivos de Base"
Registro_Fallas=''
with open('Registro_Fallas.csv', "w") as A:
    A.write(Registro_Fallas)
A.close()
    
qtCreatorFile="Interfaz.ui"
Ui_MainWindow, QtBaseClass= uic.loadUiType(qtCreatorFile)

#---------------------Clase de Archivos----------------------------------------

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        "-----------------Botones para las funciones--------------------------"
        self.OpenButton.clicked.connect(self.abrir_archivo)
        self.ConvertButton.clicked.connect(self.convert_txt)
        self.ConvertButton.clicked.connect(self.datos_interfaz)
        self.SaveButton.clicked.connect(self.save_csv)
        self.ConvertButton.clicked.connect(self.extraer_nodos)
        self.ConvertButton.clicked.connect(self.datos_generados)
        self.Graficar.clicked.connect(self.grafica_nodos)
        self.ValidaButton.clicked.connect(self.validar_reporte)
        self.ValidaButton.clicked.connect(self.archivo_MES)
        self.Ayuda.clicked.connect(self.ayuda)
        self.FailButton.clicked.connect(self.add_pendientes)
        self.radioButton.clicked.connect(self.fallas_pendientes)
        self.radioButton_2.clicked.connect(self.fallas_PenCom)
        self.radioButton_3.clicked.connect(self.fallas_completas)
        "------------------------Acciones del MenuBar-------------------------"
        self.actionConfiguraci_n.triggered.connect(self.path_configuracion)
        self.actionBuscar_Archivo.triggered.connect(self.abrir_archivo)
        self.actionInformaci_n_general.triggered.connect(self.informacion_general)
        "------------------------Menu de configuraciones----------------------"
        self.ConFig=QtWidgets.QDialog()
        self.CON=Configuracion_App()
        self.paths()
        
    def linea_final(self):
        contador=open("Log.txt", "r")
        Total=len(contador.readlines())
        return Total 
    
    def contadorFallas_general(self):
        Total=self.df['CRD'].count()
        return Total  
    
    def paths(self):
        with open ('ScorpConfig.txt', 'r') as config_file:
            Dato_Config=config_file.readlines()
        config_file.close()
        Origen=str(Dato_Config[0])
        Guardado=str(Dato_Config[1])
        Origen=Origen.replace('PathIn;', '')
        Guardado=Guardado.replace('PathSave;', '')
        return Origen, Guardado
    
    def abrir_archivo(self):
        Origen, Guardado=self.paths()
        Origen=str(Origen)+'/'
        fileName, _= QFileDialog.getOpenFileName(self,"Open File",Origen,
                                                 "Text File(*.txt);;"
                                                 "Python Files" 
                                                 "(*.py);;All Files (*)")
        self.File_Seleccion=fileName
        Archivo=open(self.File_Seleccion, "r")
        Serie=Archivo.read().split('\n')
        nombre=str(Serie[5])
        Fecha=str(Serie[3])
        TesterName=str(Serie[1])
        Time=str(Serie[4])
        self.nombre=''.join( c for c in nombre if  c not in 'SN:    ' )
        self.Fecha=''.join( c for c in Fecha if  c not in 'Date:   ' )
        self.Time=str(''.join(filter(str.isdigit, Time)))
        self.Tester_Name=''.join(c for c in TesterName if c
                                 not in 'Testername: ')
        if len(self.Time) < 6:
            self.Time='0'+self.Time
        fecha=self.Fecha.split('/')
        dia=fecha[0]
        year=fecha[-1]
        fecha[-1]=dia
        fecha[0]=year
        
        for i in range(len(fecha)):
            if len(fecha[i])<2:
                fecha[i]='0'+fecha[i]
            if len(fecha[i])>2:
                fecha[i]=fecha[i][2:] 
        fecha_Default=fecha
        "--------------------Ingreso del reporte para validacion--------------"
        hora=time.strftime("%H%M%S")
        fecha=time.strftime("%y%m%d")
        self.DateIn=str(fecha+hora)
        self.Serial=self.nombre
        self.Date_Default=''.join(fecha_Default)+self.Time
        "---------Extraer la hora en la que se genero el programa------------"
        self.fecha.setText('Fecha Log:'+self.Fecha)
        self.fecha.setStyleSheet("background-color: blue") 
        self.fecha.setFont(QtGui.QFont("Arial Narrow", 12, QtGui.QFont.Bold ))
        self.Numero.setText('N° Serie:'+self.nombre)
        self.Numero.setStyleSheet("background-color:    blue") 
        self.Numero.setFont(QtGui.QFont("Arial Narrow", 12, QtGui.QFont.Bold ))
        "------------------------Registro Usuario-----------------------------"
        with open ("Registro.txt", "r") as user_registro:
            usuarios_register=user_registro.readlines()
        user_registro.close()
        usuarios_register[-1]=''
        current_user=usuarios_register[-1]+ self.Serial+':' + self.Date_Default+ '\n'
        with open ("Registro.txt", "a") as add_user:
            add_user.write(current_user)
        add_user.close()
        
    def convert_txt(self):
        inicio=open(self.File_Seleccion, "r")
        lectura_txt=inicio.read()
        with open("Log.txt", "wt") as S:
            S.write(lectura_txt)
        S.close()
    
        lectura_txt=open("Log.txt", "r+")
        Lectura=lectura_txt.readlines()
        Rango_lectura=islice(Lectura, 6, self.linea_final()-14)
        Datos_usar=('').join(Rango_lectura)
        for linea in Datos_usar:
            linea
        with open("Log.txt", "wt") as S:
            S.write(Datos_usar)
        S.close()
        # "Reemplazo de caracteres para manipulacion"
        Datos=open("Log.txt", "r")
        Cambio1=Datos.read().split('\n\n')
        Cambio2=[i.replace('FAIL','\n    FAIL;') for i in (Cambio1)]
        Cambio3=[i.replace('; \n','\n')for i in (Cambio2)]
        Cambio4=[i.replace('\n',';\n')for i in (Cambio3)]
        Cambio5=[i.replace('','')for i in (Cambio4)]
        Cambio6=[i.replace(';\n  ->','  ->')for i in (Cambio5)]
        Cambio7=[i.replace(';;', ';')for i in (Cambio6)]
        Cambio8=[i.replace('\n', '')for i in (Cambio7)]
        Cambio9=[i.replace('->', '->**-')for i in (Cambio8)]
        Cambio10=[i.replace('    2-Wire: ', '')for i in (Cambio9)]
        Cambio11=[i.replace('FAIL;    O' , 
                            'FAIL;    Note: O')for i in (Cambio10)]
        Cambio12=[i.replace('FAIL;    S' , 
                            'FAIL;    Note: S')for i in (Cambio11)]
        
        for i in range(len(Cambio12)):
            Cambio12[i]=Cambio12[i]+'\n' 
        x=('').join(Cambio12)
        for linea in x:
            linea
        with open("Log.txt", "wt") as S:
            S.write(x)
        S.close()
        Datos=open("Log.txt", "r")
        Lista=Datos.read().split('->')
        del(Lista[0])

        for i in range(len(Lista)):
            Lista[i]=Lista[i].split(";")   
        d=[]
        for i in range(len(Lista)):
            d.append([])
            for j in Lista[i]:
                if '**' or 'FAIL' or 'Cmt' or 'Note' or 'Result' or 'Measured' or 'Expected' or 'N1' or 'Gnd' or 'G='in j:
                    if '**-' in j:
                        d[i].append(j)
                    if 'FAIL' in j:
                        d[i].append(j)
                    if 'Cmt:'in j:
                        d[i].append(j)
                    if 'Note:' in j:
                        d[i].append(j)
                    if 'Result:' in j:
                        d[i].append(j)
                    if 'Measured:' in j:
                        d[i].append(j)
                    if 'Expected:' in j:
                        d[i].append(j)
                    if 'N1:' in j:
                        d[i].append(j)
                    if 'Gnd:' in j:
                        d[i].append(j)
                    if 'G=' in j:
                        d[i].append(j)
                    if 'Anode' in j:
                        d[i].append(j)
                    if 'mode not' in j:
                        d[i].append(j)
                    if 'Result forward:' in j:
                        d[i].append(j)

        d=pd.DataFrame(d)
        d.to_csv("DataBase1.csv", index=False, header=False)
        self.df=pd.read_csv("DataBase1.csv", names=['CRD', 'Status','Note',
                                          'Result/Measured','Expect', 'Nodes'])
        self.df.to_csv("DataBase1.txt", index=False, header=False)
        self.df.to_csv("DataTable.csv")
        modifica=open ("DataBase1.txt","r")
        Inicio=modifica.readlines()
        L1=[i.replace('  "\n','')for i in (Inicio)]
        L2=[i.replace(',  ',';')for i in (L1)]
        L3=[i.replace(',"  ',';')for i in (L2)]
        L4 =[i.replace(',"Gnd',';Gnd')for i in (L3)]
        L5=[i.replace('**-','')for i in (L4)]
        x=('').join(L5)
        for linea in x:
            linea
        with open ('DataBase1.txt', 'w') as S:
            S.write(x)
        S.close()
        
        data=np.genfromtxt('DataBase1.txt',delimiter=';',dtype=str, 
                           skip_header=0, usecols=(0,1,2,3,4,5))
        with open('DataBase1.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        "Adicion de encabezados"
        df = pd.read_csv('DataBase1.csv', sep=None,names=['CRD', 'Status',
                                                          'Note',
                                                          'Result/Measured',
                                                          'Expect','Nodes'] ) 
        df.to_csv('DataBase1.csv') 
        "Imprimir las fallas del registro"
        self.fallasregistradas=str(self.contadorFallas_general())
        self.fallaslbl.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.fallaslbl.setStyleSheet("background-color: red") 
        self.fallaslbl.setText(self.fallasregistradas)
        self.fallaslbl.setAlignment(QtCore.Qt.AlignCenter)
        
    def registro_usuario(self):
        "Registar al usuario que realiza la validacion"
        
    def ayuda(self):
         QMessageBox.information(self, "Ayuda", 
                                 "Llenar la parte de validacion con pass \n"
                                 + "si el nodo coincide con lo esperado o\n "
                                 +"fail en caso contrario", 
                                 QMessageBox.Ok)
        
    def datos_interfaz(self):
        "Mostar la base de datos en pantalla"
        df  = pd.read_csv('DataBase1.csv', index_col = 0,header = 0)
        self.dframe=pd.DataFrame(df)
        self.dframe["Validacion"]=''
        "Contar numero de filas"
        fila=len(df.index)
        self.FailtableWidgetnodo.setColumnCount(7)
        self.FailtableWidgetnodo.setRowCount(fila)
        for i in range(fila):
            for j in range(7):
                self.FailtableWidgetnodo.setItem(i,j,
                                                 QTableWidgetItem(str(
                                                     df.iloc[i,j])))
        self.FailtableWidgetnodo.show()
        
    def columnas_fallas(self, df_Nodo):
        columna=[]
        for linea in df_Nodo:
            linea=columna.append(linea)
        Nodo=df_Nodo.index
        #Conteo=columna
        Fallas={'Nodo':Nodo, 'Fallas':columna}
        df_fallas=pd.DataFrame(Fallas)
        return df_fallas

    def extraer_nodos(self):
        "Funcion para extraer las fallas en los nodos"
        file="DataBase1.csv" 
        df=pd.read_csv(file, header=0)
        Nodo=df['Nodes']
        df=Nodo.str.split(',')
        self.df=df.sort_values(ascending=True)
        with open('DataNode.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.df)
        df = pd.read_csv('DataNode.csv', sep=None , names=["N1", "N2", "N3"]) 
        df.to_csv('DataNode.csv')
      
        df1=df['N1'].value_counts()
        df2=df['N2'].value_counts()
        df3=df['N3'].value_counts()
        Col=len(df3.index)
        
        df_1=self.columnas_fallas(df1)
        df_2=self.columnas_fallas(df2)
        
        if Col != 0:
            df_3=self.columnas_fallas(df3)
            df_totalnodo=df_1['Nodo'].append(
                df_2['Nodo'].append(df_3['Nodo']))
            df_totalfalla=df_1['Fallas'].append(
                df_2['Fallas'].append(df_3['Fallas']))
            
        else: 
             df_totalnodo=df_1['Nodo'].append(df_2['Nodo'])
             df_totalfalla=df_1['Fallas'].append(df_2['Fallas'])        
             
        df_final={'Nodos':df_totalnodo, 'Fallas':df_totalfalla}
        df_final=pd.DataFrame(df_final)
        df_final=df_final.sort_values('Fallas', ascending=False)
        self.MainFail=pd.DataFrame(df_final)
        #---------------------------------------------------------------------
        "Creacion de fallas acumuladas"
        primer=open('Registro_Fallas.csv', 'r')
        primer=primer.readlines()
        if primer == []:
            df_acum=pd.read_csv('Registro_Fallas.csv','r',
                                names=['Nodos', 'Fallas'])
        else:
            df_acum=pd.read_csv('Registro_Fallas.csv',header=0)
            
        df_acumNodo=df_acum['Nodos'].append(df_final['Nodos'])
        df_acumFalla=df_acum['Fallas'].append(df_final['Fallas'])
        df_acumNodo=df_acum['Nodos'].append(df_final['Nodos'])
        df_acumFalla=df_acum['Fallas'].append(df_final['Fallas'])
        df_ACUMULADA={'Nodos':df_acumNodo, 'Fallas':df_acumFalla}
        self.df_ACUMULADA=pd.DataFrame(df_ACUMULADA)
        self.df_ACUMULADA.to_csv('Registro_Fallas.csv')
#------------------------------------------------------------------------------        
        self.df_ACUMULADA=self.df_ACUMULADA.sort_values('Nodos')
        self.df_ACUMULADA= self.df_ACUMULADA.groupby(
            ["Nodos"],as_index=False)["Fallas"].sum()
        self.df_ACUMULADA=self.df_ACUMULADA.sort_values('Fallas', 
                                                        ascending=False)
        filaN=len(self.df_ACUMULADA.index)
        self.tableWidgetN.setColumnCount(2)
        self.tableWidgetN.setRowCount(filaN)
        for i in range(filaN):
            for j in range(2):
                self.tableWidgetN.setItem(i, j, QTableWidgetItem(
                    str(self.df_ACUMULADA.iloc[i,j])))
        self.tableWidgetN.show()
        #----------------------------------------------------------------------
        self.DatoReporte1=filaN
        self.DatoReporte2=df_ACUMULADA['Fallas'].sum()           
        #---------------------------------------------------------------------
        self.tableWidget=QTableWidget()
        filaN=len(self.MainFail.index)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(filaN)
        nombreColumnas = ("Nodo","Fallas")
        self.tableWidget.setHorizontalHeaderLabels(nombreColumnas)
        for i in range(filaN):
            for j in range(2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(
                    str(self.MainFail.iloc[i,j])))
        
        self.DatoReporte3=filaN
        self.DatoReporte4=self.MainFail['Fallas'].sum()
        
    def grafica_nodos(self):
        "Muestra la tabla de la tarjeta actual que se encuntra validando"
        self.tableWidget.show()
        
    def datos_generados(self):
        self.Datos_Generados.setText('Nodos Acumulados: '
                                     +str(self.DatoReporte1)
                                     + '\nTotal de Fallas: '
                                     +str(self.DatoReporte2) 
                                     + '\nNodos Tarjeta Actual: ' 
                                     + str(self.DatoReporte3) 
                                     +'\nFallas en Tarjeta Actual: ' 
                                     + str(self.DatoReporte4)) 
               
    def validar_reporte(self):
        "validar el reporte de la tabla"
        with open("Reporte_Final.csv", "w", newline='', 
                  encoding='utf-8') as Reportefinal:
            writer=csv.writer(Reportefinal)
            for row in range(self.FailtableWidgetnodo.rowCount()):
                rowdata=[]
                for column in range(self.FailtableWidgetnodo.columnCount()):
                    item=self.FailtableWidgetnodo.item(row, column)
                    if item is not None:
                        rowdata.append(item.text())
                    else:
                        rowdata.append('---')
                writer.writerow(rowdata)
                   
        df = pd.read_csv('Reporte_Final.csv', sep=None , names=["CRD", 
                                                                "Status", 
                                                                "Note", 
                                                                "Result",
                                                                "Expect",
                                                                "Nodes",
                                                                "Validacion"])
        self.df_incompleto=df
        if df.isnull().values.any() == False:
            self.df_MES=df
            validacion_pass=df['Validacion'].value_counts()
            rango_validacion=len(validacion_pass)
            if rango_validacion==1:
                if validacion_pass.index=="pass":
                    self.mensajefinal.setStyleSheet("background-color: green") 
                    self.mensajefinal.setText("Pass")
                    self.mensajefinal.setFont(QtGui.QFont("Arial", 20, 
                                                          QtGui.QFont.Bold ))
                    df.to_csv('Reporte_Final.csv', index=False)
                else:
                    self.mensajefinal.setStyleSheet("background-color: red") 
                    self.mensajefinal.setText("Fail")
                    self.mensajefinal.setFont(QtGui.QFont("Arial", 20, 
                                                          QtGui.QFont.Bold ))
                    df.to_csv('Reporte_Final.csv', index=False)
            else:
                self.mensajefinal.setStyleSheet("background-color: red") 
                self.mensajefinal.setText("Fail")
                self.mensajefinal.setFont(QtGui.QFont("Arial", 20, 
                                                  QtGui.QFont.Bold ))
                if rango_validacion != 0:
                    QMessageBox.information(self, "Validar", 
                                            """Realizar la validacion \n 
                                            de la tarjeta""",
                                            QMessageBox.Ok)    
            #------------------------------------------------------------------
                validar=df.sort_values('Validacion')
                rango_fallas=validar["Validacion"].value_counts()
                Repeti_F=[]
                for linea in rango_fallas:
                    linea=Repeti_F.append(linea)
                NodoF=rango_fallas.index
                fallasss={'state':NodoF, 'Fallas':Repeti_F}
                dfail=pd.DataFrame(fallasss)
                dfail=dfail.sort_values('state')
                r=dfail.iloc[0,1]
                validar=validar.iloc[0:r]
                validarF=pd.DataFrame(validar)
                validarF.to_csv('Reporte_Final.csv', index=False)
        else:
            print('Vaalidacion incompleta')
            self.mensajefinal.setStyleSheet("background-color: yellow") 
            self.mensajefinal.setText("Validacion\nIncompleta")
            self.mensajefinal.setFont(QtGui.QFont("Arial", 12, 
                                                  QtGui.QFont.Bold ))
            
            df__pendiente= self.df_incompleto['Validacion']
            print(self.df_incompleto)
            pendientes=[]
            completados=[]
            for i in range(len(df__pendiente)):
                if df__pendiente[i] != 'pass':
                    fila_pendiente=[]
                    for j in range(7):
                        fila_pendiente.append(self.df_incompleto.iloc[i][j])
                    pendientes.append(fila_pendiente)
                else:
                    fila_completa=[]
                    for j in range(7):
                        fila_completa.append(self.df_incompleto.iloc[i][j])
                    completados.append(fila_completa)
            
            print(pendientes ,'\nCompletados\n', completados)
            self.df_pendientes=pd.DataFrame(pendientes)
            self.df_completados=pd.DataFrame(completados)
            self.df_pendientes.to_csv('Reporte_Final_incompleto.csv')
      
    def fallas_pendientes(self):
        "Oculta las fallas que el operador ya valido, pero aun no esta "
        "completa la revision de la tarjeta en su totalidad"
        df  = pd.read_csv('Reporte_Final_incompleto.csv', index_col = 0,
                          header = 0)
        self.dframe=pd.DataFrame(df)
        self.dframe["Validacion"]=''
        "Contar numero de filas"
        fila=len(df.index)
        self.FailtableWidgetnodo.setColumnCount(7)
        self.FailtableWidgetnodo.setRowCount(fila)
        for i in range(fila):
            for j in range(7):
                self.FailtableWidgetnodo.setItem(i,j,
                                                 QTableWidgetItem(str(
                                                     df.iloc[i,j])))
        self.FailtableWidgetnodo.show()
            
    def fallas_PenCom(self):
        "Mostar todas las fallas"
        df=self.df_incompleto
        fila=len(df.index)
        self.FailtableWidgetnodo.setColumnCount(7)
        self.FailtableWidgetnodo.setRowCount(fila)
        for i in range(fila):
            for j in range(7):
                self.FailtableWidgetnodo.setItem(i,j,
                                                 QTableWidgetItem(str(
                                                     df.iloc[i,j])))
        self.FailtableWidgetnodo.show()
    
    def fallas_completas(self):
        df=self.df_completados
        df=pd.concat([df,self.df_Revalidado])
        fila=len(df.index)
        self.FailtableWidgetnodo.setColumnCount(7)
        self.FailtableWidgetnodo.setRowCount(fila)
        for i in range(fila):
            for j in range(7):
                self.FailtableWidgetnodo.setItem(i,j,
                                                 QTableWidgetItem(str(
                                                     df.iloc[i,j])))
        self.FailtableWidgetnodo.show()
        
    def add_pendientes(self):
        "añade las fallas que tiene pendiente de una validacion"
        incompleto=[]
        for row in range(self.FailtableWidgetnodo.rowCount()):
            rowdata=[]
            for column in range(self.FailtableWidgetnodo.columnCount()):
                item=self.FailtableWidgetnodo.item(row, column)
                if item is not None:
                    rowdata.append(item.text())
                else:
                    rowdata.append('---')
            incompleto.append(rowdata)
        self.df_Revalidado=pd.DataFrame(incompleto)
        
    def path_configuracion(self):
        "Configuracion de los paths de los paths de los reporte de Scorpion" 
        self.CON.show()
    
    def informacion_general(self):
        "Brindar informacion al operdaor"
        QMessageBox.information(self, "Informacion",
                                "El programa esta diseñado para hacer "+
                                "una validacion de las fallas\n"+
                                "detectadas mediante Scorpion "+
                                "de manega que genere el archivo\n"+
                                "correspondiente para poder cargar "+
                                "en el sistema MES", QMessageBox.Ok)
    
    def archivo_MES(self):
        "Edicion del archivo para MES"
        with open ("Base_final.txt", 'r+') as MesFile:
            Llenado=MesFile.readlines()
        MesFile.close()  
        "Datos del reportes"
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
        self.Data=Data
        
        self.PathIn=self.Data[0][1]
        self.PathSave=self.Data[1][1]
        self.Custom=self.Data[2][1]
        self.TestName=self.Data[3][1]
        self.AssemblyRev=self.Data[4][1]
        self.Process=self.Data[5][1]
        self.Status=self.Data[6][1]
        self.AssemblyName=self.Data[7][1]
        self.BoardStyle=self.Data[8][1]
        self.Equipo_Name=self.Data[9][1]
        self.Line=self.Data[10][1]
        self.Site=self.Data[11][1]
        
        Ensamble=self.AssemblyName
        Revision_Defecto=self.Date_Default
        DateIn=self.DateIn
        Empleado='Pendiente'
        Assembly_name=self.BoardStyle
        Nombre_Equipo=self.Tester_Name
        Customer_name=self.Custom
        DateOut=str(time.strftime("%y%m%d")+time.strftime("%H%M%S"))
        Codigo_falla='pendiente'
        Test_Process=self.Process
        Line=self.Line
        site=self.Site
        Test_Status=self.Status
        "-------------------Llenado de Datos Linea 1--------------------------"
        Dato1_Reporte=[i.replace('ENSAMBLE', 
                                 Ensamble)for i in Llenado]
        Dato2_Reporte=[i.replace('REVISIONPORDEFECTO', 
                                 Revision_Defecto)for i in Dato1_Reporte]
        Dato3_Reporte=[i.replace('NOMBREdelEquipo',
                                 self.Tester_Name)for i in Dato2_Reporte]
        Dato4_Reporte=[i.replace('Numero de empleado', 
                                 Empleado)for i in Dato3_Reporte]
        "------------------------------linea2---------------------------------"
        Dato5_Reporte=[i.replace('SERIAL',
                                 self.Serial )for i in Dato4_Reporte]
        Dato6_Reporte=[i.replace('codigo de falla', 
                                 Codigo_falla)for i in Dato5_Reporte]
        Dato7_Reporte=[i.replace('hora_inicio_validacion', 
                                 DateIn)for i in Dato6_Reporte]
        Dato8_Reporte=[i.replace('analog', 
                                 Test_Process)for i in Dato7_Reporte]
        Dato9_Reporte=[i.replace('hora_final_validacion',
                                 DateOut)for i in Dato8_Reporte]
        Dato10_Reporte=[i.replace('CISCO SMT'
                                ,Customer_name)for i in Dato9_Reporte]
        Dato11_Reporte=[i.replace('Moor Park', 
                                  Assembly_name)for i in Dato10_Reporte]
        Dato12_Reporte=[i.replace('@LINE|15',
                                  '@LLINE|'+Line)for i in Dato11_Reporte]
        Dato13_Reporte=[i.replace('@SITE|5',
                                 '@SITE|'+site)for i in Dato12_Reporte]
        Dato14_Reporte=[i.replace('shorts',
                                  Test_Status)for i in Dato13_Reporte]
        Formato_MES=Dato14_Reporte
        Datos_to_MES=self.df_MES
        Result=Datos_to_MES['Result']
        Expect=Datos_to_MES['Expect']
        CRD_name=Datos_to_MES['CRD']
        Resistor_index,Capacitor_index,Diodo_index,Voltaje_index=[],[],[],[]
        """##RESISTOR
        {@BlOCK|CRD|00
        {@A-RES|0|+Result/Measured+02|{@LIM|Expect+02|Expect+%tolerancia
                                       |Expect-%tolerancia|}}
        }
        """
        i=0
        for CRD in Datos_to_MES['Note']:
            i=i+1
            if 'RES' in CRD:
                CRD_R=CRD
                Resistor_index.append(i-1)
            if 'CAP' in CRD:
                CRD_C=CRD
                Capacitor_index.append(i-1)
            if 'C//' in CRD:
                CRD_C=CRD
                Capacitor_index.append(i-1)
                
            if 'DIO' in CRD:
                CRD_DIO=CRD
                Diodo_index.append(i-1)
            if 'SHORT' in CRD:
                CRD_Power=CRD
                Voltaje_index.append(i-1)
            else:
                pass
        Co_Regi=Resistor_index + Capacitor_index + Diodo_index + Voltaje_index
        Co_total=[]
        for i in range(len(Datos_to_MES['CRD'])):
            Co_total.append(i)   
        set1, set2=set(Co_Regi), set(Co_total)
        Jumper_index=list(set2.symmetric_difference(ste1))
        #Jumper_index=list(set(Co_Regi)-set(Co_total))
        "------------------------Adicion en Formato---------------------------"
        "---------------------------Resistencias------------------------------"
        for value in Resistor_index:
            CRD_R=CRD_name[value]
            Rvalue=re.findall("\d+\.\d+",Result[value])
            Rvalue=float(''.join(Rvalue))
            Evalue=re.findall("\d+\.\d+", Expect[value])
            if len(Evalue)>=2:
                TolMax, TolMin=Evalue[0], Evalue[1]
            Evalue=float(''.join(Evalue))     
            if '%' in Expect[value]:
                Tolerancia=str(''.join(filter(str.isdigit, Expect[value])))
                Tolerancia=int(Tolerancia[-2:])
                TolMax=  Evalue + Evalue*(Tolerancia/100)
                TolMin= Evalue - Evalue*(Tolerancia/100)
            if '<' in Expect[value]:
                TolMax, TolMin=Evalue - 0.000001,  1.0
            if 'kOhm' in Result[value]:
                Rvalue, Evalue=Rvalue*1000, Evalue*1000    
                TolMax, TolMin=TolMax*1000, TolMin*1000 
           
            Rvalue, Evalue='%E' %Decimal(Rvalue),'%E' %Decimal(Evalue)
            TolMax, TolMin='%E' %Decimal(TolMax),'%E' %Decimal(TolMin)    
            Resist_MES='{@BlOCK|'+CRD_R+'|00--\n'+'{@A-RES|0|+'+str(
                Rvalue)+'|{@LIM3|+'+str(Evalue)+'|+'+str(
                    TolMax)+'|+'+str(TolMin)+'|}}\n}'
            Formato_MES.append(Resist_MES)
        "--------------------------Capacitor----------------------------------"
        """##Capacitor
        {@BLOCK|CRD|00
        {@A-CAP|0|+Result-08{@LIM3|+Expect+E-08/07|+Expect+%tolerancia|Expect-%toleranci|}}
        }
        """
        for value in Capacitor_index:
            CRD_C=CRD_name[value]
            Cvalue=re.findall("\d+\.\d+",Result[value])
            Cvalue=float(''.join(Cvalue))
            CEvalue=re.findall("\d+\.\d+", Expect[value])
            if len(CEvalue) >= 2:
                TolMax=CEvalue[0]
                TolMin=CEvalue[1]
                if TolMax < TolMin:
                    Max=(float(TolMax)*1000)
                    Tolerancia=(Max + float(TolMin)) / 2
                    TolMax=Max
                    CEvalue=Tolerancia
                else:
                    Tolerancia=(float(CEvalue[0])+float(CEvalue[1])) /2
            if '%' in Expect[value]:
                if len(CEvalue)==1:
                    CEvalue=float(''.join(CEvalue))   
                Tolerancia=str(''.join(filter(str.isdigit, Expect[value])))
                Tolerancia=int(Tolerancia[-2:])
                TolMax=  CEvalue + CEvalue*(Tolerancia/100)
                TolMin= CEvalue - CEvalue*(Tolerancia/100)
    
            if 'nF' in Result[value]:
                TolMax, TolMin=float(TolMax),float(TolMin)
                Cvalue, CEvalue=Cvalue/(10**9), CEvalue/(10**9)    
                TolMax, TolMin=TolMax/(10**9), TolMin/(10**9)
            if 'µF' in Result[value]:
                TolMax, TolMin=float(TolMax),float(TolMin)
                Cvalue, CEvalue=Cvalue/(10**6), CEvalue/(10**6)    
                TolMax, TolMin=TolMax/(10**6), TolMin/(10**6)
            if 'pF' in Result[value]:
                TolMax, TolMin=float(TolMax),float(TolMin)
                if 'nF' in Expect[value]:
                    Cvalue=Cvalue/(10**12)
                else:
                    Cvalue, CEvalue=Cvalue/(10**12), CEvalue/(10**12)    
                    TolMax, TolMin=TolMax/(10**12), TolMin/(10**12)
            
            Cvalue, CEvalue='%E' %Decimal(Cvalue),'%E' %Decimal(CEvalue)
            TolMax, TolMin='%E' %Decimal(TolMax),'%E' %Decimal(TolMin)
                
            Cap_MES='{@BlOCK|'+CRD_C+'|00--\n'+'{@A-CAP|0|+'+str(
                Cvalue)+'|{@LIM3|+'+str(CEvalue)+'|+'+str(
                    TolMax)+'|+'+str(TolMin)+'|}}\n}'
            Formato_MES.append(Cap_MES)
        "---------------------------POWER(Shorts)-----------------------------"
        #######################################################################
        """##Voltaje Nodos
        {@BLOCK|PWR_CHECK|00
        {@A-MEAN|0|+Measured'E'+/- 00/01|CRD}
        }"""
        for value in Voltaje_index:
            CRD_Power=CRD_name[value]
            Vvalue=re.findall('\d+\.+\d', Result[value])
            Vvalue=float(''.join(Vvalue))
            VEvalue=re.findall('\d+\.+\d', Expect[value])
            VEvalue=float(''.join(VEvalue))
            Vvalue='%E' %Decimal(Vvalue)
            Cap_MES='{@BlOCK|'+CRD_Power+'|00--\n'+'{@A-MEA|0|+'+str(
                Vvalue)+'|'+CRD_Power+'}\n}'
            Formato_MES.append(Cap_MES)
        ######################################################################3
        "---------------------------DIODO-------------------------------------"
        """
        {@BLOCK|q35%cr|00
        {@A-DIO|0|+6.377791E-01{@LIM2|+9.500000E-01|+4.000000E-01}}
        }
        """
        for value in Diodo_index:
            CRD_D =CRD_name[value]
            Dvalue=re.findall("\d+\.+\d", Result[value])
            Dvalue=float(''.join(Dvalue))
            DEvalue=re.findall("\d+\.+\d", Expect[value])
            DEvalue=float(''.join(DEvalue))
            if '%' in Expect[value]:
                Tol=str(''.join(filter(str.isdigit, Expect[value])))
                Tol=int(Tol[-2:])
                TolMax=DEvalue + DEvalue*(Tol/100)
                TolMin=DEvalue - DEvalue*(Tol/100)
            if 'mV' in Expect[value]:
                if 'V' in Result[value]:
                    Dvalue=Dvalue*(10**3)
                Dvalue, DEvalue=Dvalue/1000, DEvalue/1000
                TolMax, TolMin=TolMax/1000, TolMin/1000
            Dvalue,DEvalue='%E' %Decimal(Dvalue),'%E' %Decimal(Dvalue)
            TolMax, TolMin='%E' %Decimal(TolMax),'%E' %Decimal(TolMin) 
            
            Dio_MES='{@BLOCK|'+CRD_D+'|00--\n{@A-DIO|0|+'+str(
                Dvalue)+'{@LIM2|+'+str(TolMax)+'|+'+str(TolMin)+'}}\n}'
            Formato_MES.append(Dio_MES)
            CRD_Diodo=CRD_name[value]
            Dvalue=re.findall('\d+\.+\d', Result[value])
            Dvalue=float(''.join(Dvalue))
            DEvalue=re.findall('\d+\.+\d', Expect[value])
            DEvalue=float(''.join(DEvalue))
            if '%' in Expect[value]:
                Tol=str(''.join(filter(str.isdigit, Expect[value])))
                Tol=int(Tol[-2:])
                TolMax=  DEvalue + DEvalue*(Tol/100)
                TolMin= DEvalue - DEvalue*(Tol/100)
            if 'mV' in Expect[value]:
                if Dvalue < DEvalue:
                    DEvalue=DEvalue/(10**3)    
                    TolMax, TolMin=TolMax/(10**3), TolMin/(10**3)
                else:
                    Dvalue, DEvalue=Dvalue/(10**3), DEvalue/(10**3)    
                    TolMax, TolMin=TolMax/(10**3), TolMin/(10**3)
                
            Dvalue, DEvalue='%E' %Decimal(Dvalue),'%E' %Decimal(DEvalue)
            TolMax, TolMin='%E' %Decimal(TolMax),'%E' %Decimal(TolMin)        
            
            Dio_MES='{@BLOCK|'+ CRD_Diodo +'|00--\n'+'{@A-DIO|0|+'+str(
                Dvalue)+'{@LIM2|+'+str(TolMax)+'|+'+str(TolMin
                                                        )+'}}\n}'
            Formato_MES.append(Dio_MES)    
        "---------------------------JUMP--------------------------------------"
        """##Jumper
        {@BLOCK|CRD(gmar##)|00
        {@A-JUMP|0|+Measured/Result'E'+03-04{@LIM2|Expect|###|
        """
        for value in Jumper_index:
            CRD_J=CRD_name[value]
            Jvalue=re.findall("\d+\.+\d", Result[value])
            Jvalue=float(''.join(Jvalue))
            JEvalue=re.findall("\d+\.+\d", Expect[value])
            JEvalue=float(''.join(JEvalue))
            if '%' in Expect[value]:
                Tol=str(''.join(filter(str.isdigit, Expect[value])))
                Tol=int(Tol[-2:])
                TolMax=JEvalue + JEvalue*(Tol/100)
                TolMin=JEvalue - JEvalue*(Tol/100)
            if '>':
                TolMax=9.999999*10**99 
                TolMin=JEvalue +1
            if 'mV' in Result[Value]:
                Jvalue,JEvalue=Jvalue/1000,JEvalue/1000
                TolMax, TolMin=TolMax/1000, TolMin/1000
                
            Jvalue,JEvalue='%E' %Decimal(Jvalue),'%E' %Decimal(Jvalue)
            TolMax, TolMin='%E' %Decimal(TolMax),'%E' %Decimal(TolMin)
            Jum_MES='{@BLOCK|'+CRD_J+'|00--\n{@A-JUMP|0|+'+str(
                Jvalue)+'{@LIM2|+'+str(TolMax)+'|+'+str(JEvalue)+'|}}\n}'
            Formato_MES.append(Jum_MES)
        Formato_MES=pd.DataFrame(Formato_MES)
        print(Formato_MES)
        format_mes=[]
        for elemento in Formato_MES[0]:
            print(elemento)
            format_mes.append(elemento)
        format_mes=[i.replace('\n', '')for i in (format_mes)]
        format_mes=[i.replace('--', '\n')for i in (format_mes)]
        print(format_mes)
        with open ('MES.txt' , 'w') as confi:
            for i in range(len(format_mes)):
                print(format_mes[i])
                confi.write(str(format_mes[i]+'\n'))
        confi.close()
    
    def save_csv(self):
        Archivo=open(self.File_Seleccion, "r")
        Serie=Archivo.read().split('\n')
        nombre=str(Serie[5])
        self.nombre=''.join( c for c in nombre if  c not in 'SN:   ' )
        hora=time.strftime("%H%M%S")
        fecha=time.strftime("%y%m%d")
        Date=str(fecha+hora)
        nombre=self.nombre
        Origen, Guardado=self.paths()
        Guardado=str(Guardado)+'/'
        fileName, _= QFileDialog.getSaveFileName(self,"Save File",Guardado+
                                                 nombre+Date,
                                                 "CSV File(*.csv);;Excel"
                                                 "Files (*.xls);;All Files (*)")
        file1=pd.read_csv("Reporte_Final.csv")
        file1.to_csv("Reporte_Final.csv", index=False)
        file1=open("Reporte_Final.csv", "r")
        file1_read=file1.read()                                                   
        if fileName!='':
            file_test=open(fileName, "w", encoding="utf-8")
            file_test.write(file1_read)
            file_test.close()
        
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    windown=MyApp()
    windown.setWindowIcon(QtGui.QIcon(str("scorpion-tail_38917.ico")))
    windown.show()
    sys.exit(app.exec_())
           

        

             
 
    
    
       
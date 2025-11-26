# -*- coding: utf-8 -*-
from mimetypes import common_types
import os
import sys
import subprocess
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
import importlib
import csv
from Duc_Data import F_Data
from Duc_Data import K_Data
from Duc_Data import NS_Data
from Duc_Data import GX_Data
from Duc_Data import NSE_Data
from Duc_Data import S_Data
from Duc_Data import T_Data
from Duc_Data import U_Data
from Duc_Data import UF_Data
from Duc_Data import US_Data
from Duc_Data import ParamFDuctile
from Duc_Data import ParamKDuctile
from Duc_Data import ParamNSDuctile
from Duc_Data import ParamGXDuctile
from Duc_Data import ParamNSEDuctile
from Duc_Data import ParamSDuctile
from Duc_Data import ParamTDuctile
from Duc_Data import ParamUDuctile
from Duc_Data import ParamUFDuctile
from Duc_Data import ParamUSDuctile
#doc=App.ActiveDocument
DEBUG = True # set to True to show debug messages
lang=['English','Japanese']
#JDPA A300
#Duc_type=['Flange_type','K_type','NS_type','GX_type','NSE_type','S_type','T_type','U_type','UF_type','US_type',]
Duc_type=['Flange_type','K_type',]
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(330, 550)
        Dialog.move(1000, 0)
        #種別
        self.label_type = QtGui.QLabel('Type',Dialog)
        self.label_type.setGeometry(QtCore.QRect(20, 10, 61, 22))
        self.label_type.setStyleSheet("color: black;")
        self.combo_type = QtGui.QComboBox(Dialog)
        self.combo_type.setGeometry(QtCore.QRect(90, 5, 205, 22))
        self.combo_type.setObjectName("comboBox")

        #異形管
        self.label = QtGui.QLabel('Fittings',Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 61, 22))
        self.label.setStyleSheet("color: black;")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(90, 32, 205, 22))
        self.comboBox.setObjectName("comboBox")
       
        #呼び径
        self.label_2 = QtGui.QLabel('Dia',Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 115, 60, 22))
        self.label_2.setStyleSheet("color: black;")
        self.comboBox_2 = QtGui.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 113, 75, 22))
        self.comboBox_2.setObjectName("comboBox_2")

        #切管長
        self.label_5 = QtGui.QLabel('cuttingTubeLength',Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 80, 61, 22))
        self.label_5.setStyleSheet("color: black;")
        self.spinBoxL=QtGui.QSpinBox(Dialog)
        self.spinBoxL.setGeometry(90, 80, 60, 32)
        self.spinBoxL.setMinimum(10)  # 最小値
        self.spinBoxL.setMaximum(5500)  # 最大値
        self.spinBoxL.setValue(5500)  # 
        self.spinBoxL.setSingleStep(10) #step
        self.spinBoxL.setAlignment(QtCore.Qt.AlignCenter)
        #ステップ
        self.label_step = QtGui.QLabel('Step',Dialog)
        self.label_step.setGeometry(QtCore.QRect(170, 80, 50, 22))
        self.label_step.setStyleSheet("color: black;")
        self.le_step = QtGui.QLineEdit('10',Dialog)
        self.le_step.setGeometry(QtCore.QRect(210, 80, 50, 22))
        self.le_step.setAlignment(QtCore.Qt.AlignCenter)

        #異形管　和文
        #self.le_la = QtGui.QLabel(Dialog)
        #self.le_la.setGeometry(QtCore.QRect(150, 60, 170, 12))
        #self.le_la.setObjectName("label_3")
        self.le_la = QtGui.QLineEdit(Dialog)
        self.le_la.setGeometry(QtCore.QRect(90, 58, 170, 20))
        self.le_la.setAlignment(QtCore.Qt.AlignLeft)  
        #create
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 140, 75, 22))
        self.pushButton.setObjectName("pushButton")

        #更新
        self.pushButton_update = QtGui.QPushButton('upDate',Dialog)
        self.pushButton_update.setGeometry(QtCore.QRect(113, 140, 70, 22))

        #インポートデータ
        self.pushButton3 = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(205, 140, 75, 22))
        
        #胴付き寸法
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(20, 195, 170, 22))
        self.label_7.setStyleSheet("color: black;")
        #spreadsheet
        self.pushButton_m2 = QtGui.QPushButton('massTally_spreadsheet',Dialog)
        self.pushButton_m2.setGeometry(QtCore.QRect(20, 165, 150, 22))

        #言語
        self.pushButton_la=QtGui.QPushButton('language',Dialog)
        self.pushButton_la.setGeometry(QtCore.QRect(180, 165, 90, 22))
        self.comboBox_lan = QtGui.QComboBox(Dialog)
        self.comboBox_lan.setGeometry(QtCore.QRect(180, 190, 90, 22))
        self.comboBox_lan.setEditable(True)
        self.comboBox_lan.lineEdit().setAlignment(QtCore.Qt.AlignRight)
        #質量計算
        self.pushButton_m = QtGui.QPushButton('massCulculation',Dialog)
        self.pushButton_m.setGeometry(QtCore.QRect(20, 190, 150, 22))

        #count
        self.pushButton_ct = QtGui.QPushButton('Count',Dialog)
        self.pushButton_ct.setGeometry(QtCore.QRect(20, 215, 95, 22))
        self.le_ct = QtGui.QLineEdit(Dialog)
        self.le_ct.setGeometry(QtCore.QRect(120, 215, 50, 22))
        self.le_ct.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_ct.setText('1')
        
        #質量入力
        self.pushButton_m3 = QtGui.QPushButton('massImput[kg]',Dialog)
        self.pushButton_m3.setGeometry(QtCore.QRect(20, 240, 95, 22))
        self.pushButton_m3.setObjectName("pushButton")  
        self.le_mass = QtGui.QLineEdit(Dialog)
        self.le_mass.setGeometry(QtCore.QRect(120, 240, 50, 22))
        self.le_mass.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_mass.setText('10.0')
        #密度
        self.lbl_gr = QtGui.QLabel('SpecificGravity',Dialog)
        self.lbl_gr.setGeometry(QtCore.QRect(20, 265, 80, 22))
        self.lbl_gr.setStyleSheet("color: black;")
        self.le_gr = QtGui.QLineEdit(Dialog)
        self.le_gr.setGeometry(QtCore.QRect(120, 265, 50, 22))
        self.le_gr.setAlignment(QtCore.Qt.AlignCenter)  
        self.le_gr.setText('7.85')

        #図形
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(15, 300, 300, 200))
        self.label_6.setText("")
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "img","img_00.png")
        self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        self.label_6.setAlignment(QtCore.Qt.AlignTop)
        self.label_6.setObjectName("label_6")

        self.combo_type.addItems(Duc_type)
        self.comboBox_lan.addItems(lang)

        self.combo_type.setCurrentIndex(1)
        self.combo_type.currentIndexChanged[int].connect(self.on_type)
        self.combo_type.setCurrentIndex(0)

        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.on_lst)
        self.comboBox.currentIndexChanged[int].connect(self.on_size)
        self.comboBox.setCurrentIndex(0)

        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_2.currentIndexChanged[int].connect(self.on_lst2)
        self.comboBox_2.setCurrentIndex(0)

        self.combo_type.setCurrentIndex(1)
        self.combo_type.currentIndexChanged[int].connect(self.on_lst2)
        self.combo_type.setCurrentIndex(0)

        self.spinBoxL.valueChanged[int].connect(self.spinMove) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.fc_create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton_update, QtCore.SIGNAL("pressed()"), self.update)
        QtCore.QObject.connect(self.pushButton_ct, QtCore.SIGNAL("pressed()"), self.countCulc)
        QtCore.QObject.connect(self.pushButton_m, QtCore.SIGNAL("pressed()"), self.massCulc)
        QtCore.QObject.connect(self.pushButton_m2, QtCore.SIGNAL("pressed()"), self.massTally)
        QtCore.QObject.connect(self.pushButton_m3, QtCore.SIGNAL("pressed()"), self.massImput)
        QtCore.QObject.connect(self.pushButton_la, QtCore.SIGNAL("pressed()"), self.language)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.retranslateUi(Dialog)
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", 'FcdPipeFittings', None))
        
    def language(self):
        doc = App.activeDocument()
        if doc:
            group_names = []
            for obj in doc.Objects:
                print(obj.Label)
                try:
                    type=obj.type
                    self.combo_type.setCurrentText(type)
                except:
                    pass
                try:
                    fittings=obj.Fittings
                    dia=obj.dia
                    self.comboBox.setCurrentText(fittings)
                    self.comboBox_2.setCurrentText(dia)

                    gengo=self.comboBox_lan.currentText()
                    label2=obj.JPN
                    label=self.comboBox.currentText()[3:]
                    
                    if gengo=='Japanese':
                       obj.Label=label2
                    else:
                       obj.Label=label 
                    print(gengo,label,label2)  
                except:
                    pass     
    def massImput(self):
         # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g=float(self.le_mass.text())
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g

    def countCulc(self):
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        count=int(self.le_ct.text())
        try:
            obj.addProperty("App::PropertyFloat", "count",label)
            obj.count=count
        except:
            obj.count=count 

    def massCulc(self):
        # 選択したオブジェクトを取得する
        c00 = Gui.Selection.getSelection()
        if c00:
            obj = c00[0]
        label='mass[kg]'
        g0=float(self.le_gr.text())
        try:
            g=round(obj.Shape.Volume*g0*1000/10**9 ,2)
            count=int(self.le_ct.text())
            print(count)
        except:
             pass
        try:
            obj.addProperty("App::PropertyFloat", "mass",label)
            obj.mass=g
        except:
            obj.mass=g  
    
    def massTally(self):#spreadsheet
        doc = App.ActiveDocument
        spreadsheet = doc.getObject("Parts_List") 
        if spreadsheet is None:
            spreadsheet = doc.addObject("Spreadsheet::Sheet", "Parts_List")
            #return  
        # ヘッダー行を記入
        headers = ["No",  "Name", "Dia", "Standard",'Count','Unit[kg]','Mass[kg]']
        for header in enumerate(headers):
            #spreadsheet.set(f"A{i+1}", str(i + 1))  # 行番号
            spreadsheet.set("A1", headers[0])
            spreadsheet.set("B1", headers[1])
            spreadsheet.set("C1", headers[2])
            spreadsheet.set("D1", headers[3])
            spreadsheet.set("E1", headers[4])
            spreadsheet.set("F1", headers[5])
            spreadsheet.set("G1", headers[6])
        # パーツを列挙して情報を書き込む
        row = 2
        i=1
        s=0
        for i,obj in enumerate(doc.Objects):
            if hasattr(obj, "count") and obj.count > 0:
                try:
                    spreadsheet.set(f"A{row}", str(row-1))  # No
                    spreadsheet.set(f"B{row}", obj.Label)  
                    spreadsheet.set(f"C{row}", obj.dia)
                    try:
                        try:
                            spreadsheet.set(f"D{row}", 'L='+obj.L0+'mm') 
                        except:
                            pass    
                        n=obj.count
                        spreadsheet.set(f"E{row}", str(n))   # count
                        spreadsheet.set(f"F{row}", str(obj.mass))
                        spreadsheet.set(f"G{row}", f"{obj.mass*n:.2f}")  # mass
                    except:
                        pass
                    s=obj.mass*n+s
                    row += 1
                except:
                    print('error')
                    pass    
                spreadsheet.set(f'G{row}',str(s))
        App.ActiveDocument.recompute()

    def setParts(self):
        selection = Gui.Selection.getSelection()
        for obj in selection:
            type=obj.type
            label=obj.Label
            print(label)
            Fittings=obj.Fittings
            dia=obj.dia
            JPN=obj.JPN
            try:
                L=obj.L0
                self.spinBoxL.setValue(int(L))
            except:
                pass
            
            self.combo_type.setCurrentText(type)
            self.comboBox_2.setCurrentText(dia)
            self.comboBox.setCurrentText(Fittings)
            self.le_la.setText(JPN)
            print(type,Fittings,dia)
        App.ActiveDocument.recompute() 
    def spinMove(self):
        step=self.le_step.text()
        self.spinBoxL.setSingleStep(int(step)) 
        selection = Gui.Selection.getSelection()
        for obj in selection:
           myShape=obj
           
           try:
               L=self.spinBoxL.value()
               try: 
                   myShape.L0=str(L)
               except: 
                   myShape.L=str(L)
           except:
               
               #myShape.L=str(L)
               myShape=None
           App.ActiveDocument.recompute() 
                         
    def on_mass(self):
        doc = Gui.ActiveDocument
        object_list = []
        for obj in doc.Objects:
            if hasattr(obj, "mass"):
                object_list.append([obj.Label,obj.dia, 1, obj.mass])
            else:
                try:
                    object_list.append([obj.Label,obj.dia, 1, 0.0])
                except:
                    pass
        doc_path = doc.FileName
        csv_filename = os.path.splitext(os.path.basename(doc_path))[0] + "_counts_and_masses.csv"
        csv_path = os.path.join(os.path.dirname(doc_path), csv_filename)
        try:
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Object Name', 'dia','Count', 'mass[kg]'])
                for obj in object_list:
                    writer.writerow(obj)
        except:
            pass        

    def update(self):
        selection = Gui.Selection.getSelection()
        for obj in selection:
            #myShape=obj
            dia=self.comboBox_2.currentText()
            Fittings=self.comboBox.currentText()
            type=self.combo_type.currentText()
            obj.dia=dia
            obj.Fittings=Fittings
            obj.type=type
            label=self.comboBox.currentText()[3:]
            try:
                L0=self.spinBoxL.value()
                try:
                    obj.L0=str(L0)
                except:    
                    obj.L=str(L0)
            except:
                pass
            try:
                obj.JPN=self.le_la.text()
            except:
                JPN=self.le_la.text()
                obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN   

                    


        App.ActiveDocument.recompute() 

    def on_type(self):
        type=self.combo_type.currentText()
        key=self.comboBox.currentText()[:2]
        self.comboBox.clear()
        if type=='Flange_type':
            self.comboBox.addItems(F_Data.lst)
        elif type=='K_type':
            self.comboBox.addItems(K_Data.lst) 
        elif type=='NS_type':
            self.comboBox.addItems(NS_Data.lst) 
        elif type=='GX_type':
            self.comboBox.addItems(GX_Data.lst) 
        elif type=='NSE_type':
            self.comboBox.addItems(NSE_Data.lst) 
        elif type=='S_type':
            self.comboBox.addItems(S_Data.lst) 
        elif type=='T_type':
            self.comboBox.addItems(T_Data.lst) 
        elif type=='U_type':
            self.comboBox.addItems(U_Data.lst) 
        elif type=='UF_type':
            self.comboBox.addItems(UF_Data.lst) 
        elif type=='US_type':
            self.comboBox.addItems(US_Data.lst) 
    def on_size(self):
        global dia
        type=self.combo_type.currentText()
        key=self.comboBox.currentText()[:2]
        self.comboBox_2.clear()
        if type=='Flange_type':
            if key=='00' or key=='01':
                dia=F_Data.strp
            elif key=='02':
                dia=F_Data.trct
            elif key=='03':
                dia=F_Data.trct2
            elif key=='04':
                dia=F_Data.trct3
            elif key=='05':
                dia=F_Data.strp
            elif key=='06':
                dia=F_Data.strp
            elif key=='07':
                dia=F_Data.gvsp
            elif key=='08':
                dia=F_Data.flgt
            elif key=='09':
                dia=F_Data.strp
            elif key=='10':
                dia=F_Data.mhlc
            elif key=='11':
                dia=F_Data.strp
            elif key=='12' or key=='13':
                dia=F_Data.gate
            self.comboBox_2.addItems(dia)

        elif type=='K_type':
            if key=='00' :
                dia=K_Data.strp
            elif key=='01' :
                dia=K_Data.trct
            elif key=='02':
                dia=K_Data.trct2
            elif key=='03' or key=='04':
                dia=K_Data.trct3
            elif key=='05' :
                dia=K_Data.strp [:-5]   
            elif key=='06' or key=='07' or key=='08' :
                dia=K_Data.strp
            elif  key=='09':
                dia=K_Data.strp[5:]    
            elif key=='10':
                dia=K_Data.gvsp
            elif key=='11':
                dia=K_Data.gvsp
            elif key=='12':
                dia=K_Data.ttf
            elif key=='13':
                dia=K_Data.ttf2
            elif key=='14':
                dia=K_Data.dtp
            elif key=='15':
                dia=K_Data.strp
            elif key=='16' or key=='17' or key=='18' or key=='19':
                dia=K_Data.strp
            elif key=='20' or key=='21' :
                dia=K_Data.strp[:6]
            self.comboBox_2.addItems(dia)

        elif type=='NS_type':
            if key=='00' :
                dia=NS_Data.strp
            elif key=='01' :
                dia=NS_Data.trct
            elif key=='02':
                dia=NS_Data.trct2
            elif key=='03' or key=='04':
                dia=NS_Data.trct3
            elif key=='05' or key=='06' or key=='07' or key=='08' or key=='09':
                dia=NS_Data.strp
            elif key=='10':
                dia=NS_Data.strp
            elif key=='11':
                dia=NS_Data.strp
            elif key=='12':
                dia=NS_Data.gvsp
            elif key=='13':
                dia=NS_Data.gvsp
            elif key=='14' :
                dia=NS_Data.ttf
            elif key=='15':
                dia=NS_Data.ttf3
            elif key=='16':
                dia=NS_Data.ttf2
            elif key=='17':
                dia=NS_Data.dtp
            elif key=='18' or key=='19':
                dia=NS_Data.strp
            elif key=='20' or key=='21'  or key=='22':
                if key=='21':
                    dia=NS_Data.strp[:9]
                elif key=='22':
                    dia=NS_Data.strp[9:]
                else:
                    dia=NS_Data.strp

            elif key=='23' or key=='24' :
                dia=NS_Data.strp
            elif key=='25' :
                dia=NS_Data.gate
            elif key=='26' :
                dia=NS_Data.gate2
            self.comboBox_2.addItems(dia)

        elif type=='GX_type':
            if key=='00' :
                dia=GX_Data.strp
            elif key=='01' :
                dia=GX_Data.trct2
            elif key=='02' or key=='03':
                dia=GX_Data.reduc
            elif key=='04' or key=='05':
                dia=GX_Data.strp
            elif key=='06' or key=='07':
                dia=GX_Data.strp
            elif key=='08' or key=='09':
                dia=GX_Data.strp
            elif key=='10' :
                dia=GX_Data.strp
            elif key=='11' :
                dia=GX_Data.frjt
            elif key=='12' :
                dia=GX_Data.sfrjt
            elif key=='13' :
                dia=GX_Data.pfrjt
            elif key=='14' :
                dia=GX_Data.dfrjt
            elif key=='15' :
                dia=GX_Data.strp
            elif key=='16' :
                dia=GX_Data.strp
            elif key=='17' :
                dia=GX_Data.zshp
            elif key=='18' :
                dia=GX_Data.strp
            elif key=='19' :
                dia=GX_Data.strp
            elif key=='20' :
                dia=GX_Data.strp
            elif key=='21' :
                dia=GX_Data.strp[:6]
            elif key=='22' :
                dia=GX_Data.strp[:6]
            elif key=='23' :
                dia=GX_Data.strp
            elif key=='24' :
                dia=GX_Data.strp
            elif key=='25' :
                dia=GX_Data.strp
            self.comboBox_2.addItems(dia)

        elif type=='NSE_type':
            if key=='00' :
                dia=NSE_Data.strp
            elif key=='01' :
                dia=NSE_Data.trct2
            elif key=='02' :
                dia=NSE_Data.trct3
            elif key=='03' or key=='04':
                dia=NSE_Data.strp
            elif key=='05' or key=='06':
                dia=NSE_Data.strp
            elif key=='07' or key=='08':
                dia=NSE_Data.strp
            elif key=='09' :
                dia=NSE_Data.strp
            elif key=='10' :
                dia=NSE_Data.trct4
            elif key=='11' :
                dia=NSE_Data.strp
            elif key=='12' :
                dia=NSE_Data.strp
            elif key=='13' :
                dia=NSE_Data.strp
            elif key=='14' :
                dia=NSE_Data.strp
            elif key=='15' :
                dia=NSE_Data.strp
            elif key=='16' :
                dia=NSE_Data.strp
            elif key=='17' :
                dia=NSE_Data.strp
            self.comboBox_2.addItems(dia)
                
        elif type=='S_type':
            if key=='00' :
                dia=S_Data.strp
            elif key=='01' :
                dia=S_Data.strp
            elif key=='02' :
                dia=S_Data.strp
            elif key=='03' :
                dia=S_Data.strp
            self.comboBox_2.addItems(dia)

        elif type=='T_type':
            if key=='00' :
                dia=T_Data.strp
            elif key=='01' :
                dia=T_Data.trct
            elif key=='02' :
                dia=T_Data.trct2
            elif key=='03' or key=='04':
                dia=T_Data.trct3
            elif key=='05' or key=='06':
                dia=T_Data.strp
            elif key=='07' or key=='08':
                dia=T_Data.strp
            elif key=='09':
                dia=T_Data.ttf
            elif key=='10':
                dia=T_Data.ttf3
            elif key=='11':
                dia=T_Data.ttf2
            elif key=='12':
                dia=T_Data.dtp
            elif key=='13':
                dia=T_Data.strp[:5]
            elif key=='14':
                dia=T_Data.strp[:5]
            elif key=='15':
                dia=T_Data.strp[:5]
            elif key=='16':
                dia=T_Data.strp[:5]
            elif key=='17':
                dia=T_Data.strp
            self.comboBox_2.addItems(dia)

        elif type=='U_type':
            if key=='00' :
                dia=U_Data.strp
            elif key=='01' :
                dia=U_Data.trct
            elif key=='02' :
                dia=U_Data.trct2
            elif key=='03' or key=='04':
                dia=U_Data.trct3
            elif key=='05' or key=='06':
                dia=U_Data.strp
            elif key=='07' or key=='08':
                dia=U_Data.strp
            elif key=='09':
                dia=U_Data.strp
            elif key=='10':
                dia=U_Data.gvsp
            elif key=='11':
                dia=U_Data.gvsp
            elif key=='12':
                dia=U_Data.ttf
            elif key=='13':
                dia=U_Data.dtp
            elif key=='14':
                dia=U_Data.strp
            elif key=='15':
                dia=U_Data.strp
            elif key=='16':
                dia=U_Data.strp
            elif key=='17':
                dia=U_Data.strp
            self.comboBox_2.addItems(dia)

        elif type=='UF_type':
            if key=='00' :
                dia=UF_Data.strp
            elif key=='01' :
                dia=UF_Data.trct
            elif key=='02' :
                dia=UF_Data.trct2
            elif key=='03' or key=='04':
                dia=UF_Data.trct3
            elif key=='05' or key=='06':
                dia=UF_Data.strp
            elif key=='07' or key=='08':
                dia=UF_Data.strp
            elif key=='09':
                dia=UF_Data.strp
            elif key=='10':
                dia=UF_Data.strp
            elif key=='11':
                dia=UF_Data.strp
            elif key=='12':
                dia=UF_Data.strp
            elif key=='13':
                dia=UF_Data.strp
            elif key=='14':
                dia=UF_Data.strp
            elif key=='15':
                dia=UF_Data.gvsp
            elif key=='16':
                dia=UF_Data.gvsp
            elif key=='17':
                dia=UF_Data.ttf
            elif key=='18':
                dia=UF_Data.dtp
            elif key=='19':
                dia=UF_Data.strp
            elif key=='20':
                dia=UF_Data.strp
            self.comboBox_2.addItems(dia)    

        elif type=='US_type':
            if key=='00' :
                dia=US_Data.strp
            elif key=='01' :
                dia=US_Data.strp
            self.comboBox_2.addItems(dia)  

        selection = Gui.Selection.getSelection()
        for obj in selection:    
            self.comboBox_2.setCurrentText(obj.dia)

    def on_lst2(self):
        type=self.combo_type.currentText()
        key = self.comboBox.currentText()[:2]
        if type=='Flange_type':
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=F_Data.flngs[key_1]
                L=sa[9]
            except:
                pass 
    
            try: 
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='K_type':
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=K_Data.rcvd[key_1]
                L=sa[7]
            except:
                pass
    
            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='NS_type':
            global Y
            global P
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=NS_Data.rcvd[key_1]
                if key=='00' or key=='23':
                    sa=NS_Data.rcvd[key_1]
                    Y=sa[6]
                    L=sa[7]
                    lbl='胴付き寸法Y[mm]='+str(Y)
                elif key=='18':
                    sa=NS_Data.rcvd1[key_1]
                    Y=sa[9]
                    lbl='胴付き寸法Y[mm]='+str(Y)
                elif key=='21':
                    sa=NS_Data.rcvd1[key_1]
                    P=sa[3]
                    lbl='のみ込み寸法P[mm]='+str(P)  
                self.label_7.setText(QtGui.QApplication.translate("Dialog", lbl, None))
            except:
                pass
            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='GX_type':
            ta=GX_Data.strp
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=GX_Data.rcvd[key_1]
                L=sa[5]
                if key=='00':
                    sa=GX_Data.rcvd[key_1]
                    Y=sa[6]
                    lbl='胴付き寸法Y[mm]='+str(Y)
                elif key=='15':
                    sa=GX_Data.rcvd1[key_1]
                    y1=sa[12]
                    lbl='胴付き寸法y1[mm]='+str(y1)  
                elif key=='18':
                    sa=GX_Data.rcvd1[key_1]
                    P=sa[4]
                    lbl='のみ込み寸法P[mm]='+str(P)     
                elif key=='20':
                    sa=GX_Data.rcvd1[key_1]
                    Y=sa[12]
                    lbl='胴付き寸法Y[mm]='+str(Y)
                elif key=='21':
                    sa=GX_Data.rcvd1[key_1]
                    P=sa[4]
                    lbl='のみ込み寸法P[mm]='+str(P)  
                self.label_7.setText(QtGui.QApplication.translate("Dialog", lbl, None))
            except:
                pass

            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='NSE_type':
            ta=NSE_Data.strp
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=NSE_Data.rcvd[key_1]
                L=sa[5]
                if key=='00':
                    sa=NSE_Data.rcvd[key_1]
                    Y=sa[3]
                    lbl='胴付き寸法Y[mm]='+str(Y)
                elif key=='12':
                    sa=NSE_Data.rcvdk[key_1]
                    Y=sa[8]
                    lbl='胴付き寸法Y[mm]='+str(Y)
                self.label_7.setText(QtGui.QApplication.translate("Dialog", lbl, None))    
            except:
                pass
            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='S_type':
            ta=S_Data.strp
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=S_Data.rcvd[key_1]
                L=sa[5]
            except:
                pass
            
            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='T_type':
            ta=T_Data.strp
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=T_Data.rcvd[key_1]
                L=sa[6]
            except:
                pass
            
            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='U_type':
            ta=U_Data.strp
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=U_Data.rcvd[key_1]
                L=sa[5]
            except:
                pass
            
            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='UF_type':
            ta=UF_Data.strp
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=UF_Data.rcvd[key_1]
                L=sa[5]
                if key=='00':
                    sa=UF_Data.rcvd[key_1]
                    Y=sa[3]
                    lbl='胴付き寸法Y[mm]='+str(Y)
                self.label_7.setText(QtGui.QApplication.translate("Dialog", lbl, None))    
            except:
                pass
            
            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

        elif type=='US_type':
            ta=US_Data.strp
            a=self.comboBox_2.currentText()
            key_1=a
            try:
                sa=US_Data.rcvd[key_1]
                L=sa[5]
                if key=='00':
                    sa=UF_Data.rcvd[key_1]
                    Y=sa[3]
                    lbl='dimensionWithbody胴付き寸法Y[mm]='+str(Y)
                self.label_7.setText(QtGui.QApplication.translate("Dialog", lbl, None))    
            except:
                pass
            
            try:
                self.lineEdit_1.setText(QtGui.QApplication.translate("Dialog", str(L), None))
            except:
                pass

    def on_lst(self):
        global key_1
        global key_2
        global sa
        global a
        global xlc
        global FC
        global pic

        type=self.combo_type.currentText()
        key = self.comboBox.currentText()[:2]
        if type=='Flange_type':
            try:
                FC=F_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_f' + key + '.png'
            except:
                pass   

        elif type=='K_type':
            try:
                FC=K_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_k' + key + '.png'  
            except:
                pass    
            
        elif type=='NS_type':
            try:
                FC=NS_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_ns' + key + '.png'
            except:
                pass
            
        elif type=='GX_type':
            try:
                FC=GX_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_GX' + key + '.png'  
            except:
                pass
            
        elif type=='NSE_type':
            try:
                FC=NSE_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_nse' + key + '.png'  
            except:
                pass
            
        elif type=='S_type':
            try:
                FC=S_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_s' + key + '.png'  
            except:
                pass
            
        elif type=='T_type':
            try:
                FC=T_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_t' + key + '.png'    
            except:
                pass
            
        elif type=='U_type':
            try:
                FC=U_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_u' + key + '.png' 
            except:
                pass
            
        elif type=='UF_type':
            try:
                FC=UF_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_uf' + key + '.png'  
            except:
                pass
            
        elif type=='US_type':
            try:
                FC=US_Data.FC_type[key]
                self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))
                pic='img_us' + key + '.png'      
            except:
                pass
                     
        try:
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, "Duc_data",pic)
            self.label_6.setPixmap(QtGui.QPixmap(joined_path))
        except:
            pass

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base,"Duc_data","d_license.txt")
        ff= open(joined_path)
        data1 = ff.read()  # ファイル終端まで全て読んだデータを返す
        try:
            self.lineEdit.setText(QtGui.QApplication.translate("Dialog", str(data1), None))
        except:
            pass
        ff.close()
    def fc_create(self):
        type=self.combo_type.currentText()
        key = self.comboBox.currentText()[:2]
        L0=self.spinBoxL.value()
        try:
            self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None, QtGui.QApplication.UnicodeUTF8))
        except:
            self.le_la.setText(QtGui.QApplication.translate("Dialog", FC, None))

        a=self.comboBox_2.currentText()
        try:
            if a[3]=='x':
                key_1=a[:3]
                key_2=a[4:]
            else:
                key_1=a[:4]
                key_2=a[5:]
        except:
            key_1=a     
        if type=='Flange_type':
            label=self.comboBox.currentText()[3:]
            if key=='00' :#---------------------------------------------------------------
                sa=F_Data.flngs[key_1]
                #label ='Flange Length Tube'
                #label=self.comboBox.currentText()[3:]
                #label=self.le_la.text()
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    pass
                obj.addProperty("App::PropertyString", "type",label).type=type
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.addProperty("App::PropertyString", "L0",label).L0=str(L0)
                obj.dia=F_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.strp[i]
            elif key=='01' :#---------------------------------------------------------------
                #label ='Single Flange Length Tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)      
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.addProperty("App::PropertyString", "L0",label).L0=str(L0)
                obj.dia=F_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.strp[i]
            elif key=='02' :#---------------------------------------------------------------
                label ='F3T-shaped Tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.trct
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.trct[i]
            elif key=='03' :#---------------------------------------------------------------
                label ='F2T-shaped Tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.trct2
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.trct2[i]    
            elif key=='04' :#---------------------------------------------------------------
                label ='Flange Reducer'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.trct3
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.trct3[i] 
            elif key=='05' :#---------------------------------------------------------------
                label ='F90Elbow'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.strp[i] 
            elif key=='06' :#---------------------------------------------------------------
                label ='F45Elbow'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.strp[i] 
            elif key=='07' :#---------------------------------------------------------------
                label ='Gate_valve_Secondary Pipe B1'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.gvsp
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.gvsp[i]   
            elif key=='08' :#---------------------------------------------------------------
                label ='Flange Short Tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.flgt
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.flgt[i]  
            elif key=='09' :#---------------------------------------------------------------
                label ='Flange Lid'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.strp[i]          
            elif key=='10' :#---------------------------------------------------------------
                label ='Manhole Cover'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.mhlc
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.mhlc[i]  
            elif key=='11' :#---------------------------------------------------------------
                label ='Trumpet Mouth'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.strp[i]    
            elif key=='12' :#---------------------------------------------------------------
                label ='F Soft seal gate valve_internal thread'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.gate
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.gate[i]    
            elif key=='13' :#---------------------------------------------------------------
                label ='F Soft seal gate valve_external thread'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=F_Data.gate
                i=self.comboBox_2.currentIndex()
                obj.dia=F_Data.gate[i]   

            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamFDuctile.f_ductile(obj) 
            obj.ViewObject.Proxy=0
            
        elif type=='K_type':
            if key=='00' or key=='20':#---------------------------------------------------------------

                if key=='00':
                    label ='K_Straight tube'
                elif key=='20':
                    label ='K_Straight tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)   
                obj.addProperty("App::PropertyString", "type",label).type=type       
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=K_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=K_Data.strp[i]
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)
            elif key=='01' :
                label ='K_Three recieved cross tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)       
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=K_Data.trct
                i=self.comboBox_2.currentIndex()
                obj.dia=K_Data.trct[i]
            elif key=='02' :
                label ='K_Tee tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)      
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=K_Data.trct2
                i=self.comboBox_2.currentIndex()
                obj.dia=K_Data.trct2[i]
            elif key=='03' or key=='04':
                if key=='03':
                    label ='K_Reducer'
                else:
                    label ='K_Reducer'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)      
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=K_Data.trct3
                i=self.comboBox_2.currentIndex()
                obj.dia=K_Data.trct3[i]
            elif key=='05' or key=='06' or key=='07' or key=='08' or key=='09':
                if key=='05':
                    label ='K_90Elbow'   
                elif key=='06':
                    label ='K_45Elbow'   
                elif key=='07':
                    label ='K_22Elbow'   
                elif key=='08':
                    label ='K_11Elbow'    
                elif key=='09':
                    label ='K_5Elbow'  
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)        
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                if key=='09':
                    obj.dia=K_Data.strp[5:]
                else:
                    obj.dia=K_Data.strp    
                i=self.comboBox_2.currentIndex()
                if key=='09':
                    obj.dia=K_Data.strp[i+5]               
                else:
                    obj.dia=K_Data.strp[i]  
            elif key=='10' or key=='11':
                if key=='10':
                    label='K_Gate_valve_secondary pipe_A1'
                elif key=='11':
                    label='K_Gate_valve_secondary pipe_A2'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label)      
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=K_Data.gvsp
                i=self.comboBox_2.currentIndex()
                obj.dia=K_Data.gvsp[i]   
            elif key=='12' or key=='13':
                if key=='12':
                   label='K_T-shaped tube with flange'
                   try:
                       doc=App.activeDocument() 
                       obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                   except:
                        doc=App.newDocument()   
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)     
                   obj.addProperty("App::PropertyEnumeration", "dia",label)     
                   obj.dia=K_Data.ttf
                   i=self.comboBox_2.currentIndex()
                   obj.dia=K_Data.ttf[i]   
                elif key=='13':
                    label='K_T-shaped pipe with a spiral flange'   
                    try:
                        doc=App.activeDocument() 
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                    except:
                        doc=App.newDocument()   
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)         
                    obj.addProperty("App::PropertyEnumeration", "dia",label)     
                    obj.dia=K_Data.ttf2
                    i=self.comboBox_2.currentIndex()
                    obj.dia=K_Data.ttf2[i]  
            elif key=='14': 
                label='K_Drainage T-shaped pipe' 
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)     
                obj.dia=K_Data.dtp
                i=self.comboBox_2.currentIndex()
                obj.dia=K_Data.dtp[i]  
            elif key=='15' or key=='16' or key=='17' or key=='18' or key=='19' or key=='20' or key=='21' : 
                if key=='15':
                    label='K_Collar' 
                elif key=='16':
                    label='K_Short tube No.1th'   
                elif key=='17':
                    label='K_Short tube No.2th'  
                elif key=='18':
                    label='K_Plug' 
                elif key=='19':
                    label='K_Retainer gland'  
                elif key=='20':
                    label='K_Straight tube no socket' 
                elif key=='21':
                    label='K Gate valve_Internal'    

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)     
                if key=='21':
                    obj.dia=K_Data.strp[:6]
                    i=self.comboBox_2.currentIndex()
                    obj.dia=K_Data.strp[i]  
                else:
                    obj.dia=K_Data.strp
                    i=self.comboBox_2.currentIndex()
                    obj.dia=K_Data.strp[i]  
            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamKDuctile.k_ductile(obj) 
            obj.ViewObject.Proxy=0    

        elif type=='NS_type':
            if key=='00' or key=='23':
                label ='NS_Straight tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyString", "type",label).type=type    
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.strp[i]
                
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)
            elif key=='01' :
                label ='NS_Three recieved cross tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.trct
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.trct[i]
            elif key=='02' :
                label ='NS_Tee tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.trct2
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.trct2[i] 
            elif key=='03' or key=='04':
                label ='NS_Reducer'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.trct3
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.trct3[i] 
            elif key=='05' or key=='05' or key=='06'or key=='07' or key=='08' or key=='09':
                if key=='05':
                    label ='NS_90Bent tube'
                elif key=='06':
                    label ='NS_45Bent tube'
                elif key=='07':
                    label ='NS_22_1/2Bent tube'
                elif key=='08':
                    label ='NS_11_1/4Bent tube'   
                elif key=='09':
                    label ='NS_5_5/8Bent tube'        

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.strp[i]   
            elif key=='10' or key=='11':
                if key=='10':
                    label ='NS_45Two-track tube'
                elif key=='11':
                    label ='NS_22_1/2Two-track tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.strp[i]    
            elif key=='12' or key=='13':
                if key=='12':
                    label ='Partition Valve Sub-tube A1'
                elif key=='13':
                    label ='Partition Valve Sub-tube A2'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.gvsp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.gvsp[i]         
            elif key=='14' or key=='15' or key=='16':
                if key=='14':
                    label ='NS_T-shaped tube with flange'
                    try:
                        doc=App.activeDocument() 
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                    except:
                        doc=App.newDocument()   
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                    obj.addProperty("App::PropertyEnumeration", "dia",label)
                    obj.dia=NS_Data.ttf
                    i=self.comboBox_2.currentIndex()
                    obj.dia=NS_Data.ttf[i] 
                    
                elif key=='15':
                    label ='NS_T-shaped pipe with shallow buried Flange'
                    try:
                        doc=App.activeDocument() 
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                    except:
                        doc=App.newDocument()   
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                    obj.addProperty("App::PropertyEnumeration", "dia",label)
                    obj.dia=NS_Data.ttf3
                    i=self.comboBox_2.currentIndex()
                    obj.dia=NS_Data.ttf3[i] 
                elif key=='16':
                    label ='NS_T-shaped pipe with a spiral flange'
                    try:
                        doc=App.activeDocument() 
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                    except:
                        doc=App.newDocument()   
                        obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                    obj.addProperty("App::PropertyEnumeration", "dia",label)
                    obj.dia=NS_Data.ttf2
                    i=self.comboBox_2.currentIndex()
                    obj.dia=NS_Data.ttf2[i] 
            elif key=='17':
                label ='NS_Drainage T-shaped pipe'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.dtp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.dtp[i]     
            elif key=='18':
                label ='NS_Collar'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.strp[i] 

            elif key=='19' or key=='20':
                if key=='19':
                    label ='NS_Short tube No.1th'
                elif key=='20':
                    label ='NS_Short tube No.2th'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.strp[i]         
            elif key=='21':
                label ='NS_Cap'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.strp[i]  
            elif key=='22':
                label ='NS_Retainer gland'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.strp[i]   
            elif key=='24':
                label ='NS_Liner'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NS_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NS_Data.strp[i] 

            elif key=='25' or key=='26':
                if key=='25':
                    label ='Gate valve_Internal'
                else:
                    label ='Gate valve_Internal2'

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                if key=='25':
                    obj.dia=NS_Data.gate
                    i=self.comboBox_2.currentIndex()
                    obj.dia=NS_Data.gate[i] 
                if key=='26':
                    obj.dia=NS_Data.gate2
                    i=self.comboBox_2.currentIndex()
                    obj.dia=NS_Data.gate2[i]     


            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamNSDuctile.ns_ductile(obj) 
            obj.ViewObject.Proxy=0        

        elif type=='GX_type':
            if key=='00' or key=='20':
                if key=='00':
                    label='GX_Straight tube'
                elif key=='20':
                    label='Straight tube'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyString", "type",label).type=type    
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i] 
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)   
            elif key=='01':
                label='GX_Tee tube'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.trct2
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.trct2[i] 
            if key=='02' or key=='03':
                label='GX_Reducer'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.reduc
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.reduc[i] 
            elif key=='04' or key=='05' or key=='06' or key=='07' or key=='08' :#曲管
                if key=='04':
                    label='GX_90Bent tube'
                elif key=='05':
                    label='GX_45Bent tube'  
                elif key=='06':
                    label='GX_22Bent tube'          
                elif key=='07':
                    label='GX_11Bent tube'   
                elif key=='08':
                    label='GX_5Bent tube' 
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]           
            elif key=='09' or key=='10':#両受曲管
                if key=='09':
                    label='GX_45Two-track tube'
                elif key=='10':
                    label='GX_22Two-track tube'  
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]           
            elif key=='11':
                label='GX_T-shaped pipe with shallow buried Flange'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.frjt
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.frjt[i] 
            elif key=='12':
                label='GX_T-shaped pipe with shallow buried Flange'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.sfrjt
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.sfrjt[i]     
            elif key=='13':
                label='GX_T-shaped pipe with a spiral flange'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.pfrjt
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.pfrjt[i]      
            elif key=='14':
                label='GX_Drainage T-shaped pipe'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.dfrjt
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.dfrjt[i]   
            elif key=='15':
                label='GX Collar'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]    
            elif key=='16':
                label='GX Both received short pipe'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]       
            elif key=='17':
                label='GX Z-shaped pipe'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.zshp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.zshp[i]         
            elif key=='18':
                label='GX_Cap'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]     
            elif key=='19':
                label='GX_Retainer gland'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]            
            elif key=='21':
                label='GX_P-Link'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]   
            elif key=='22':
                label='GX_G-Link'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]   
            elif key=='23':
                label='GX Liner'
                obj = App.ActiveDocument.addObject("Part::FeaturePython",label)        
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]    
            elif key=='24':
                label='GX_Gate valve(Internal)'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]      
            elif key=='25':
                label='GX_Gate valve(External)'
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=GX_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=GX_Data.strp[i]   
            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamGXDuctile.gx_ductile(obj) 
            obj.ViewObject.Proxy=0      

        elif type=='NSE_type':
            if key=='00' or key=='15':
                if key=='00':
                    label='NSE_Straight tube'
                elif key=='15':
                    label='Straight tube'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyString", "type",label).type=type    
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i] 
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)   
            elif key=='01':
                label='NSE Tee tube'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.trct2
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.trct2[i] 
            elif key=='02':
                label='NSE Both receiving reducer'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.trct3
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.trct3[i]     
            elif key=='03' or key=='04' or key=='05' or key=='06' or key=='07':
                if key=='03':
                    label='NSE 90Bent tube'  
                elif key=='04':
                    label='NSE 45Bent tube'  
                elif key=='05':
                    label='NSE 22Bent tube'  
                elif key=='06':
                    label='NSE 11_1/4Bent tube'  
                elif key=='07':
                    label='NSE 5_5/8Bent tube'   

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i]   
            elif key=='08' or key=='09' :
                if key=='08':
                    label='NSE_45Two-track tube'    
                if key=='09':
                    label='NSE_22Two-track tube'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i]  
            elif key=='10':
                label='NSE T-shaped pipe with shallow buried Flange'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.trct4
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.trct4[i]       
            elif key=='11' :
                label='NSE Short tube with socket'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i]    
            elif key=='12' :
                label='NSE Collar'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i]    
            elif key=='13' :
                label='NSE Cap'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i]    
            elif key=='14' :
                label='NSE Retainer gland'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i]    
            elif key=='16' :
                label='NSE N-Link'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i]  
            elif key=='17':
                label='NSE_Liner'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=NSE_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=NSE_Data.strp[i] 
            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamNSEDuctile.nse_ductile(obj) 
            obj.ViewObject.Proxy=0      
            
        elif type=='S_type':
            if key=='00':
                label='S_Straight tube'    
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyString", "type",label).type=type    
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=S_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=S_Data.strp[i] 
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)   
            if key=='01' or key=='02' or key=='03':
                if key=='01':
                    label='S_Coller'  
                elif key=='02':
                    label='S_Long coller'  
                elif key=='03':
                    label='S_Retainer gland'      
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=S_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=S_Data.strp[i] 

            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamSDuctile.s_ductile(obj) 
            obj.ViewObject.Proxy=0  

        elif type=='T_type':
            if key=='00' or key=='17':
                if key=='00':
                    label='T_Straight tube'   
                elif key=='17':
                    label='Straight tube'   

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyString", "type",label).type=type    
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=T_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=T_Data.strp[i] 
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)   
            elif key=='01' or key=='02':
                if key=='01':
                    label='T_Three recieved cross tube'   
                elif key=='02':
                    label='T_Tee tube'   

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                if key=='01':
                    obj.dia=T_Data.trct
                    i=self.comboBox_2.currentIndex()
                    obj.dia=T_Data.trct[i] 
                elif key=='02':  
                    obj.dia=T_Data.trct2
                    i=self.comboBox_2.currentIndex()
                    obj.dia=T_Data.trct2[i]   
            elif key=='03' or key=='04':
                if key=='03':
                    label='T_Reducer'   
                elif key=='04':
                    label='T_Reducer'   

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=T_Data.trct3
                i=self.comboBox_2.currentIndex()
                obj.dia=T_Data.trct3[i]   
            elif key=='05' or key=='06' or key=='07' or key=='08':
                if key=='05':
                    label='T_90Elbow'   
                elif key=='06':
                    label='T_45Elbow' 
                elif key=='07':
                    label='T_22Elbow'     
                elif key=='08':
                    label='T_11Elbow'       

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=T_Data.trct3
                i=self.comboBox_2.currentIndex()
                obj.dia=T_Data.trct3[i]       
            elif key=='09' or key=='10' or key=='11' :
                if key=='09':
                    label='T_T-shaped tube with flange'   
                elif key=='10':
                    label='T_T-shaped tube with flange' 
                elif key=='11':
                    label='T_T-shaped pipe with a spiral flange'     
                
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                if key=='09':
                    obj.dia=T_Data.ttf
                    i=self.comboBox_2.currentIndex()
                    obj.dia=T_Data.ttf[i]    
                elif key=='10':
                    obj.dia=T_Data.ttf3
                    i=self.comboBox_2.currentIndex()
                    obj.dia=T_Data.ttf3[i]  
                elif key=='11':
                    obj.dia=T_Data.ttf2
                    i=self.comboBox_2.currentIndex()
                    obj.dia=T_Data.ttf2[i]      
            elif key=='12':
                label='T_Drainage T-shaped pipe'     
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=T_Data.dtp
                i=self.comboBox_2.currentIndex()
                obj.dia=T_Data.dtp[i]    
            elif key=='13':
                label='T_Collar'     
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=T_Data.strp[:5]
                i=self.comboBox_2.currentIndex()
                obj.dia=T_Data.strp[i]       
            elif key=='14' or key=='15':
                if key=='14':
                    label='T_Short tube No.1th'  
                elif key=='15':
                    label='T_Short tube No.2th'      

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=T_Data.strp[:5]
                i=self.comboBox_2.currentIndex()
                obj.dia=T_Data.strp[i]   
            elif key=='16' :
                label='T_Plug'      
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=T_Data.strp[:5]
                i=self.comboBox_2.currentIndex()
                obj.dia=T_Data.strp[i]            
            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamTDuctile.t_ductile(obj) 
            obj.ViewObject.Proxy=0   
        
        elif type=='U_type':
            if key=='00' or key=='17':
                if key=='00':
                    label='U_Straight tube'   
                elif key=='17':
                    label='Straight tube'   

                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyString", "type",label).type=type    
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.strp[i] 
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)          
            elif key=='01' :
                label='U_Three recieved cross tube'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.trct
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.trct[i] 

            elif key=='02':
                label='U_Tee tube'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.trct2
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.trct2[i] 
            elif key=='03' or key=='04':
                label='U_Reducer'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.trct3
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.trct3[i]   
            elif key=='05' or key=='06' or key=='07' or key=='08' or key=='09':
                label='U_Reducer'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.elb90
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.elb90[i]     
            elif key=='10' or key=='11' :
                if key=='10':
                    label='U_Gate valve secondary pipe_A1'   
                elif key=='11':
                    label='U_Gate valve secondary pipe_A2'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.gvsp
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.gvsp[i]        
            elif key=='12' or key=='13' :
                if key=='12':
                    label='U_T-shaped tube with flange'   
                elif key=='13':
                    label='U_Drainage T-shaped pipe'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                if key=='12':
                    obj.dia=U_Data.ttf
                    i=self.comboBox_2.currentIndex()
                    obj.dia=U_Data.ttf[i]    
                elif key=='13':
                    obj.dia=U_Data.dtp  
                    i=self.comboBox_2.currentIndex()
                    obj.dia=U_Data.dtp[i]  
                     
            elif key=='14':
                label='U_Collar'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.strp 
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.strp[i]             
            elif key=='15':
                label='U_Short tube No.1th'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.strp 
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.strp[i]
            elif key=='16':
                label='U_Short tube No.2th'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=U_Data.strp 
                i=self.comboBox_2.currentIndex()
                obj.dia=U_Data.strp[i]    
            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamUDuctile.u_ductile(obj) 
            obj.ViewObject.Proxy=0                        
        elif type=='UF_type':
            if key=='00' :
                label='UF_Straight tube'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyString", "type",label).type=type    
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.strp[i] 
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)              
            elif key=='01' or key=='02':
                if key=='01':
                    label='UF_Three recieved cross tube'   
                elif key=='02':
                    label='UF_Tee tube'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                if key=='01':
                    obj.dia=UF_Data.trct
                    i=self.comboBox_2.currentIndex()
                    obj.dia=UF_Data.trct[i] 
                elif key=='02':
                    obj.dia=UF_Data.trct2
                    i=self.comboBox_2.currentIndex()
                    obj.dia=UF_Data.trct2[i]    
            elif key=='03' or key=='04':
                label='UF_Reducer'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.trct3
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.trct3[i] 
            elif key=='05' or key=='06' or key=='07' or key=='08' or key=='09':
                if key=='05':
                    label='UF_90Elbow'  
                elif key=='06':
                    label='UF_45Elbow'   
                elif key=='07':
                    label='UF_22Elbow' 
                elif key=='08':
                    label='UF_11Elbow'     
                elif key=='09':
                    label='UF_5Elbow' 
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.strp[i] 
            elif key=='10' or key=='11' or key=='12' or key=='13' or key=='14':
                if key=='10':
                    label='UF_90Elbow'  
                elif key=='11':
                    label='UF_45Elbow'   
                elif key=='12':
                    label='UF_22Elbow' 
                elif key=='13':
                    label='UF_11Elbow'     
                elif key=='14':
                    label='UF_5Elbow' 
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.strp[i]   
            elif key=='15' or key=='16':
                if key=='15':
                    label='UF_Gate valve secondary pipe No.A1'  
                elif key=='16':
                    label='UF_Gate valve secondary pipe No.A2'   
                
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.gvsp
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.gvsp[i]      
            elif key=='17' :
                label='UF_T-shaped tube with flange'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.ttf
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.ttf[i]     
            elif key=='18' :
                label='UF_Drainage T-shaped pipe'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.dtp
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.dtp[i]     
            elif key=='19' :
                label='UF_Short tube No.1th'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.strp[i]
            elif key=='20' :
                label='UF_Short tube No.2th'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=UF_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=UF_Data.strp[i]         
            Fittings=self.comboBox.currentText()
            obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
            ParamUFDuctile.uf_ductile(obj) 
            obj.ViewObject.Proxy=0   
        elif type=='US_type':
            if key=='00' :
                label='US_Straight tube'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyString", "type",label).type=type    
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=US_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=US_Data.strp[i] 
                obj.addProperty("App::PropertyString", "L",label).L=str(L0)     
            elif key=='01' :
                label='US_Coller'   
                try:
                    doc=App.activeDocument() 
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                except:
                    doc=App.newDocument()   
                    obj = App.ActiveDocument.addObject("Part::FeaturePython",label) 
                obj.addProperty("App::PropertyEnumeration", "dia",label)
                obj.dia=US_Data.strp
                i=self.comboBox_2.currentIndex()
                obj.dia=US_Data.strp[i]
                
        obj.ViewObject.Proxy= 0  
        Gui.activateWorkbench("DraftWorkbench")
        Gui.Selection.addSelection(obj)
        
        Gui.runCommand('Draft_Move',0)    

        #    try:
        #        doc=App.activeDocument() 
        #    except:
        #        doc=App.newDocument() 
#
#
        #    Fittings=self.comboBox.currentText()
        #    obj.addProperty("App::PropertyString", "Fittings",label).Fittings=Fittings
        #    ParamUSDuctile.us_ductile(obj) 
        #    obj.ViewObject.Proxy=0  
        #    JPN=self.le_la.text()  
        #    obj.addProperty("App::PropertyString", "JPN",label).JPN=JPN     
        #.ActiveDocument.recompute() 

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show()
        
        


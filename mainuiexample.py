# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QMessageBox
import sys,re
from mainui import Ui_MainWindow
import os,openpyxl,xlrd
import pandas as pd
from child import *
tablepath = os.path.join(os.path.dirname(__file__), "123.xlsx")

class mythread1(QtCore.QThread):
    updatesignal = QtCore.pyqtSignal(str)
    def __init__(self, func):
        super(mythread1, self).__init__()
        self.func = func
        #self.cmd = cmd
    def run(self):
        print("run thread1")
        self.result = self.func()
        self.updatesignal.emit(str(self.result))
    def getresult(self):
        return self.result

def func1():
    list1 = list()
    for i in range(1000):
        list1.append("time is " + str(i))
        print("time is " + str(i))
    return list1

class mychildui(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(mychildui, self).__init__()
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.thread1 = mythread1(func1)
        self.thread1.updatesignal.connect(self.updateUi)
        self.show()
        self.lineresult=""
        self.thread1.start()

    def updateUi(self, str):
        self.textEdit.append(str)
        print(self.thread1.getresult())
        for s in self.thread1.getresult():
            self.textEdit.append(s)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)

    def printsomething(self):
        item1 = self.listWidget.currentItem()
        data1 = item1.data(QtCore.Qt.UserRole)
        print(data1)

    def additemstolist(self):
        a = QtWidgets.QListWidgetItem()
        value1 = (self.lineresult, "sadf")
        a.setText(self.lineresult)
        a.setData(QtCore.Qt.UserRole, value1)
        self.listWidget.addItem(a)

    def updateline(self):
        self.lineresult = self.lineEdit.text()

class myui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myui, self).__init__()
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, True)
        self.newwinlist = list()

        self.UPMacadd = ""
        self.newUPMacadd = ""
        self.newUPIP = ""

        self.CCHPMac = ""
        self.newCCHPMAC = ""
        self.newCCHPIP = ""

        self.CPUAMACadd = ""
        self.newCPUMACadd = ""
        self.newCPUAIP = ""

        self.LteuptrainMac = ""
        self.newLteuptrainMac = ""
        self.newLteuptrainIP = ""

        self.MACflag4 = 0
        self.MACflag3 = 0
        self.MACflag2 = 0
        self.MACflag1 = 0

    def opendir(self):

        file_path = QFileDialog.getSaveFileName(self, "open file", "","sdf(*.txt)",
                                                    options=QFileDialog.DontUseNativeDialog)
        print(file_path)

    def openme(self):
        msgBox = QMessageBox()
        msgBox.setText("sdfdsfsdf")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        #msgBox.(QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        ret = msgBox.exec()
        print("info:",ret)

        if ret == QMessageBox.Save:
            file_save_path = QFileDialog.getSaveFileName(self,"save file","","all file(*.txt)",
                                                         options=QFileDialog.DontUseNativeDialog)
            print(file_save_path)

        elif ret == QMessageBox.Cancel:
            print("cancel")

        else:
            print("discard")

    def inputUPM(self):
        MAC = self.UPMaclineEdit_2.text()
        if MAC != self.UPMacadd:
            self.UPMacadd = MAC
            ret = getMACaddandIP_tocsv(MAC)
            if ret:
                self.newUPMacadd, self.newUPIP = ret, ret[4:]
                self.MACflag1 = True
                print(self.newUPMacadd,"mac",self.newUPIP)
            else:
                self.MACflag1 = False
                QMessageBox.warning(self,"unvalid MAC address","pls check MAC address")

    def inputCCHPM(self):
        MAC = self.CCHPMaclineEdit.text()
        if MAC != self.CCHPMac:
            self.CCHPMac = MAC
            ret = getMACaddandIP_tocsv(MAC)
            if ret:
                self.newCCHPMAC, self.newCCHPIP = ret, ret[4:]
                self.MACflag2 = True
                print(self.newCCHPMAC, "mac", self.newCCHPIP)
            else:
                self.MACflag2 = False
                QMessageBox.warning(self, "unvalid MAC address", "pls check MAC address")

    def input5gM(self):
        MAC = self.MAC5glineEdit_3.text()
        if MAC != self.CPUAMACadd:
            self.CPUAMACadd = MAC
            ret = getMACaddandIP_tocsv(MAC)
            if ret:
                self.newCPUMACadd, self.newCPUAIP = ret, ret[4:]
                self.MACflag3 = True
                print(self.newCPUMACadd, "mac", self.newCPUAIP)
            else:
                self.MACflag3 = False
                QMessageBox.warning(self, "unvalid MAC address", "pls check MAC address")

    def input4gM(self):
        MAC = self.MAC4glineEdit_4.text()
        if MAC != self.LteuptrainMac:
            self.LteuptrainMac = MAC
            ret = getMACaddandIP_tocsv(MAC)
            if ret:
                self.newLteuptrainMac, self.newLteuptrainIP = ret, ret[4:]
                self.MACflag4 = True
                print(self.newLteuptrainMac, "mac", self.newLteuptrainIP)
            else:
                self.MACflag4 = False
                QMessageBox.warning(self, "unvalid MAC address", "pls check MAC address")

    def generatetxt(self):
        #if self.MACflag1 and self.MACflag2 and self.MACflag3 and self.MACflag4:
        if True:
            readtablevalue(tablepath)
            settablevalue(tablepath, self.newCCHPMAC, self.newCCHPIP)
            print("\r\n after modify")
            readtablevalue(tablepath)


            print("pandas read")
            pandasreadtable(tablepath)

            #QMessageBox.information(self, "generate ok","save path")
        else:
            QMessageBox.warning(self, "unvalid MAC address", "pls check MAC address")


    def createnewwindow(self):
        self.newwinlist.append(mychildui())



def isValidMac(mac):
    if re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", mac): return True
    return False

def getMACaddandIP_tocsv(mac):
    result = re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", mac)
    if result:
        s = result.group().replace(":", "")
        return s
    return False

# def readtablevalue(tablepath1):
#     book = xlrd.open_workbook(tablepath1)
#     work_sheet = book.sheet_by_index(0)
#     length0 = work_sheet.nrows
#     for i in work_sheet.col_values(0):
#         print(str(i), "rows:",length0)
    # for j in work_sheet.col_values(6):
    #     print(str(j), "rows:",length0)
#
# def settablevalue(tablepath1, mac):
#     workbook = xlrd.open_workbook(tablepath1)
#     writebook = copy(workbook)
#     writesheet = writebook.get_sheet(0)
#     #writesheet.write(0, 6, mac)
#     writesheet.write(1, 6, mac)
#     writebook.save("table.xls")

def readtablevalue(tablepath1):
    book = openpyxl.load_workbook(tablepath1,read_only=True, data_only=True)
    work_sheet = book["1"]
    print("sheet name", work_sheet)
    length0 = work_sheet.max_row
    a2 = work_sheet["A2"]
    # for i in range(length0):
    #     print(str(work_sheet.cell(i+1,1).value), " rows: ", length0)
    print(a2, a2.value)

def settablevalue(tablepath1, mac, ip):
    workbook = openpyxl.load_workbook(tablepath1)
    #writebook = copy(workbook)
    print(tablepath1)
    #print(mac, ip)
    work_sheet = workbook["1"]
    #writesheet.write(0, 6, mac)
    print(mac, ip)
    work_sheet["G1"] = mac
    work_sheet["G2"] = ip
    #writebook.save("table.xls")


    a2 = work_sheet["A2"]
    print("A2 value:",a2, a2.value)
    workbook.save("123.xlsx")
    workbook = openpyxl.load_workbook(tablepath1)
    workbook.save("123.xlsx")
    # for i in range(length0):
    #     print(str(work_sheet.cell(i+1,1).value), " rows: ", length0)
    #print(a2, a2.value)

def pandasreadtable(tablepath1):
    d = pd.read_excel(tablepath, sheet_name="1",index_col=0)
    print(d)





if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_gui = myui()
    main_gui.show()
    sys.exit(app.exec_())

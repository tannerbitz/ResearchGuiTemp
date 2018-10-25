#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import PyQt5
from PyQt5 import QtCore
import serial.tools.list_ports
import pyqtgraph as pg
import time
import numpy as np
import os
import csv

#pyqtgraph Settings
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')



def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# ------------------------------------------------------------------------- #
#                           Global Variables                                #
# ------------------------------------------------------------------------- #
COM_PORT = "Not Set"
TORQUE_CHANNEL = "Not Set" #channels can only be 0-7
PRBS_CHANNEL = "Not Set" #channels can only be 0-7
PATIENT_NUMBER = "Not Set" #patient number must be between 0 - 99
ZEROTBL = {'PF20': 'Not Set',
           'PF15': 'Not Set',
           'PF10': 'Not Set',
           'PF05': 'Not Set',
           'DF00': 'Not Set',
           'DF05': 'Not Set',
           'DF10': 'Not Set'}

MVCTBL =  {'PF': 'Not Set',
           'DF': 'Not Set'}
READFLAG = 0
SERNUM2TOR = (125.0/2048.0)*(4.44822/1.0)*(0.15) #(125lbs/2048points)*(4.44822N/1lbs)*(0.15m)
tcurr = 0
targetcurr = 0

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def fileExist(filename):
    filepath = os.getcwd() + "/" + filename
    return os.path.isfile(filepath)


def writeToPatientFile(testType, flexion, ankleAngle, zeroVal):
    tempFilename = "p" + str(PATIENT_NUMBER) + "_ZeroValues.csv"
    if not fileExist(tempFilename):
        f = open(tempFilename, "w")
    else:
        f = open(tempFilename, "a")
    csvwrite = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    csvwrite.writerow([testType, flexion, ankleAngle, zeroVal])
    f.close()



def initSerial():
    if COM_PORT == "Not Set" or TORQUE_CHANNEL == "Not Set":
        return -5
    try:
        ser = serial.Serial(COM_PORT, baudrate=115200, timeout=1)
        return ser
    except serial.SerialException:
        return -2

# Global serial object
ser = initSerial()





#Global Fonts
boldFont = PyQt5.QtGui.QFont()
boldFont.setBold(True)
italicFont = PyQt5.QtGui.QFont()
italicFont.setItalic(True)
textboxFont = PyQt5.QtGui.QFont()
textboxFont.setPixelSize(20)


# ------------------------------------------------------------------------- #
#                           Serial Data Functions                           #
# ------------------------------------------------------------------------- #



class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Voluntary Reflex Testing - NMHRL'

        self.width = window_width
        self.height = window_height
        self.left = int((screen_width - window_width)/2)
        self.top = int((screen_height - window_height)/2)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()




class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        self.tabs.blockSignals(True) #just for not showing the initial message
        self.tabs.currentChanged.connect(self.onChange) #changed!


        self.tab1 = SettingsWindow()
        self.tab2 = ZeroWindow()
        # self.tab3 = MVCWindow()
        self.tab4 = VRTWindow()
        self.tabs.resize(window_width, window_height)

        # Add tabs
        self.tabs.addTab(self.tab1, "Settings")
        self.tabs.addTab(self.tab2, "Zero Torque Reading")
        # self.tabs.addTab(self.tab3, "MVC")
        self.tabs.addTab(self.tab4, "Voluntary Reflex Test")


        self.tabs.blockSignals(False)  # now listen the currentChanged signal

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def onChange(self): #changed!
        self.tab4.updateTab()
        # self.tab3.updateTab()
        self.tab2.updateTab()
        self.tab1.updateTab()

class SettingsWindow(QWidget):
    def __init__(self):
        super(SettingsWindow, self).__init__()


        windowLayout = QVBoxLayout()

        # ------------------------------------------------------------ #
        #               Standard Header                                #
        # ------------------------------------------------------------ #
        self.lbl_sheader_pnum = QLabel('Patient No:')
        self.lbl_sheader_com = QLabel('COM Port:')
        self.lbl_sheader_tor = QLabel('Torque Channel:')
        self.lbl_sheader_prbs = QLabel('PRBS Channel:')
        self.lbl_sheader_ser = QLabel('Serial:')
        self.lbl_sheader_pnum.setFont(boldFont)
        self.lbl_sheader_com.setFont(boldFont)
        self.lbl_sheader_tor.setFont(boldFont)
        self.lbl_sheader_prbs.setFont(boldFont)
        self.lbl_sheader_ser.setFont(boldFont)

        self.lbl_pnum = QLabel(str(PATIENT_NUMBER))
        self.lbl_com = QLabel(str(COM_PORT))
        self.lbl_tor = QLabel(str(TORQUE_CHANNEL))
        self.lbl_prbs = QLabel(str(PRBS_CHANNEL))
        self.lbl_ser_status = QLabel("Not Connected")


        sheader_layout = QGridLayout()
        sheader_layout.addWidget(self.lbl_sheader_pnum, 0, 0, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_pnum, 0, 1, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_com, 0, 2, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_com, 0, 3, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_tor, 0, 4, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_tor, 0, 5, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_prbs, 0, 6, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_prbs, 0, 7, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_ser, 0, 8, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_ser_status, 0, 9, 1, 1, Qt.AlignLeft)

        self.sheader_gb = QGroupBox()
        self.sheader_gb.setLayout(sheader_layout)

        self.btn_ser = QPushButton('Reset Serial')
        self.btn_ser.clicked.connect(self.resetSer)
        self.btn_ser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.gb_top = QGroupBox()
        self.gb_top_layout = QGridLayout()
        self.gb_top_layout.addWidget(self.sheader_gb, 0, 0, 1, 1)
        self.gb_top_layout.addWidget(self.btn_ser, 0, 1, 1, 1)
        self.gb_top_layout.setColumnStretch(0, 6)
        self.gb_top_layout.setColumnStretch(1, 1)
        self.gb_top.setLayout(self.gb_top_layout)

        windowLayout.addWidget(self.gb_top)
        # ------------------------------------------------------------ #
        #               Set Patient Number                             #
        # ------------------------------------------------------------ #

        self.pnum_groupbox = QGroupBox('Set Patient Number')

        self.txtbx_pnum = QLineEdit()
        self.txtbx_pnum.setPlaceholderText("Type an integer value between 0 and 99")
        self.txtbx_pnum.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.txtbx_pnum.setFont(textboxFont)
        self.txtbx_pnum.setMinimumHeight(50)
        self.btn_set_pnum = QPushButton('Set Patient Number')
        self.btn_set_pnum.clicked.connect(self.setPatientNumber)
        self.btn_set_pnum.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        pnum_layout = QGridLayout()
        pnum_layout.addWidget(self.txtbx_pnum, 0, 0)
        pnum_layout.addWidget(self.btn_set_pnum, 0, 1)
        pnum_layout.setColumnStretch(0, 7)
        pnum_layout.setColumnStretch(1, 2)

        self.pnum_groupbox.setLayout(pnum_layout)


        # ------------------------------------------------------------ #
        #               Choose COM Port GroupBox                       #
        # ------------------------------------------------------------ #
        self.com_groupbox = QGroupBox('Choose COM Port')

        self.com_lstbox = QListWidget(self);
        self.getCOMPorts() #fills listbox with available COM Ports
        self.com_lstbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.com_selectbtn = QPushButton('Select COM Port')
        self.com_selectbtn.clicked.connect(self.selectCOMPort)
        self.com_selectbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_update_com = QPushButton('Update COM List')
        self.btn_update_com.clicked.connect(self.getCOMPorts)
        self.btn_update_com.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        com_gb_layout = QGridLayout()
        com_gb_layout.addWidget(self.com_lstbox, 0 ,0, 2, 1)
        com_gb_layout.addWidget(self.com_selectbtn, 0, 1, 1, 1)
        com_gb_layout.addWidget(self.btn_update_com, 1, 1, 1, 1)
        com_gb_layout.setColumnStretch(0, 7)
        com_gb_layout.setColumnStretch(1, 2)


        self.com_groupbox.setLayout(com_gb_layout)


        # ------------------------------------------------------------ #
        #               Choose Torque Channel GroupBox                 #
        # ------------------------------------------------------------ #
        self.tor_groupbox = QGroupBox('Choose Torque Channel')

        self.tor_lstbox = QListWidget(self);
        for i in range(0, 8): #fills channel listbox
            self.tor_lstbox.addItem('Channel ' + str(i))
        self.tor_lstbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tor_selectbtn = QPushButton('Select Torque Channel')
        self.tor_selectbtn.clicked.connect(self.selectTorqueChannel)
        self.tor_selectbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



        tor_gb_layout = QGridLayout()
        tor_gb_layout.addWidget(self.tor_lstbox, 0 ,0, 2, 1)
        tor_gb_layout.addWidget(self.tor_selectbtn, 0, 1, 1, 1)
        tor_gb_layout.setColumnStretch(0, 7)
        tor_gb_layout.setColumnStretch(1, 2)
        tor_gb_layout.setRowStretch(0, 1)
        tor_gb_layout.setRowStretch(1, 1)

        self.tor_groupbox.setLayout(tor_gb_layout)

        # ------------------------------------------------------------ #
        #               Choose PRBS Channel GroupBox                 #
        # ------------------------------------------------------------ #
        self.prbs_groupbox = QGroupBox('Choose PRBS Channel')

        self.prbs_lstbox = QListWidget(self);
        for i in range(0, 8): #fills channel listbox
            self.prbs_lstbox.addItem('Channel ' + str(i))
        self.prbs_lstbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.prbs_selectbtn = QPushButton('Select PRBS Channel')
        self.prbs_selectbtn.clicked.connect(self.selectPRBSChannel)
        self.prbs_selectbtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



        prbs_gb_layout = QGridLayout()
        prbs_gb_layout.addWidget(self.prbs_lstbox, 0 ,0, 2, 1)
        prbs_gb_layout.addWidget(self.prbs_selectbtn, 0, 1, 1, 1)
        prbs_gb_layout.setColumnStretch(0, 7)
        prbs_gb_layout.setColumnStretch(1, 2)
        prbs_gb_layout.setRowStretch(0, 1)
        prbs_gb_layout.setRowStretch(1, 1)


        self.prbs_groupbox.setLayout(prbs_gb_layout)



        # ------------------------------------------------------------ #
        #               Put Groupboxes together in Layout              #
        # ------------------------------------------------------------ #
        windowLayout.addWidget(self.pnum_groupbox)
        windowLayout.addWidget(self.com_groupbox)
        windowLayout.addWidget(self.tor_groupbox)
        windowLayout.addWidget(self.prbs_groupbox)
        self.setLayout(windowLayout)

    def updateTab(self):
        self.initSerStatus()

    def resetSer(self):
        global ser
        ser = initSerial()
        self.initSerStatus()

    def initSerStatus(self):
        if ser == -1:
            self.lbl_ser_status.setText('Timeout Occured')
        elif ser == -2:
            self.lbl_ser_status.setText('Not Connected')
        elif ser == -3:
            self.lbl_ser_status.setText('Connected But Not Sending Data')
        elif ser == -4:
            self.lbl_ser_status.setText('All Torque Readings 0')
        elif ser == -5:
            self.lbl_ser_status.setText('Set COM Port')
        else:
            self.lbl_ser_status.setText('Healthy')

    def getCOMPorts(self): #function to fill COM Listbox on Settings page
        ports = serial.tools.list_ports.comports()
        self.com_lstbox.clear()
        if ports:
            for item in ports:
                self.com_lstbox.addItem(str(item))
        else:
            self.com_lstbox.addItem("No COM Ports Available")

    def selectCOMPort(self):
        for item in self.com_lstbox.selectedItems():
            fullComStr = item.text()
            if not fullComStr == "No COM Ports Available":
                global COM_PORT
                COM_PORT = fullComStr[0:fullComStr.find("-")-1]
                self.updateStandardHeader()


    def selectTorqueChannel(self):
        for item in self.tor_lstbox.selectedItems():
            global TORQUE_CHANNEL
            TORQUE_CHANNEL = int(item.text()[-1:])
            self.updateStandardHeader()

    def selectPRBSChannel(self):
        for item in self.prbs_lstbox.selectedItems():
            global PRBS_CHANNEL
            PRBS_CHANNEL = int(item.text()[-1:])
            self.updateStandardHeader()

    def setPatientNumber(self):
        tempPatientNumber = self.txtbx_pnum.text()
        tempPatientNumber = tempPatientNumber.strip()
        if not is_int(tempPatientNumber):
            self.patientNumberMsgbox("You entered the non-integer value: " + tempPatientNumber)
        else:
            tempPatientNumber = int(tempPatientNumber)
            if tempPatientNumber < 0:
                self.patientNumberMsgbox("You entered a negative number")
                return
            elif tempPatientNumber > 99:
                self.patientNumberMsgbox("You entered a number greater than 99")
                return
            else:
                global PATIENT_NUMBER
                PATIENT_NUMBER = "{:02d}".format(tempPatientNumber)
                self.updateStandardHeader()


    def patientNumberMsgbox(self, warning_msg):
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setText("Please enter an integer value between 0 - 99")
        msgbox.setInformativeText(warning_msg)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgbox.exec_()

    def updateStandardHeader(self):
        self.lbl_pnum.setText(str(PATIENT_NUMBER))
        self.lbl_com.setText(str(COM_PORT))
        self.lbl_tor.setText(str(TORQUE_CHANNEL))
        self.lbl_prbs.setText(str(PRBS_CHANNEL))



class VRTWindow(QWidget):
    def __init__(self):
        super(VRTWindow, self).__init__()

        #Trial Variables
        self.ANKLE_ANGLE = "NOT SET"
        self.FLEXION = "NOT SET"


        windowLayout = QVBoxLayout()

        # ------------------------------------------------------------ #
        #               Standard Header                                #
        # ------------------------------------------------------------ #
        self.lbl_sheader_pnum = QLabel('Patient No:')
        self.lbl_sheader_com = QLabel('COM Port:')
        self.lbl_sheader_tor = QLabel('Torque Channel:')
        self.lbl_sheader_prbs = QLabel('PRBS Channel:')
        self.lbl_sheader_ser = QLabel('Serial:')
        self.lbl_sheader_pnum.setFont(boldFont)
        self.lbl_sheader_com.setFont(boldFont)
        self.lbl_sheader_tor.setFont(boldFont)
        self.lbl_sheader_prbs.setFont(boldFont)
        self.lbl_sheader_ser.setFont(boldFont)

        self.lbl_pnum = QLabel(str(PATIENT_NUMBER))
        self.lbl_com = QLabel(str(COM_PORT))
        self.lbl_tor = QLabel(str(TORQUE_CHANNEL))
        self.lbl_prbs = QLabel(str(PRBS_CHANNEL))
        self.lbl_ser_status = QLabel("Not Connected")


        sheader_layout = QGridLayout()
        sheader_layout.addWidget(self.lbl_sheader_pnum, 0, 0, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_pnum, 0, 1, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_com, 0, 2, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_com, 0, 3, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_tor, 0, 4, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_tor, 0, 5, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_prbs, 0, 6, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_prbs, 0, 7, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_ser, 0, 8, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_ser_status, 0, 9, 1, 1, Qt.AlignLeft)

        self.sheader_gb = QGroupBox()
        self.sheader_gb.setLayout(sheader_layout)

        self.btn_ser = QPushButton('Reset Serial')
        self.btn_ser.clicked.connect(self.resetSer)
        self.btn_ser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.gb_top = QGroupBox()
        self.gb_top_layout = QGridLayout()
        self.gb_top_layout.addWidget(self.sheader_gb, 0, 0, 1, 1)
        self.gb_top_layout.addWidget(self.btn_ser, 0, 1, 1, 1)
        self.gb_top_layout.setColumnStretch(0, 6)
        self.gb_top_layout.setColumnStretch(1, 1)
        self.gb_top.setLayout(self.gb_top_layout)

        # windowLayout.addWidget(self.gb_top)

        # ------------------------------------------------------------ #
        #               Choose COM Port GroupBox                       #
        # ------------------------------------------------------------ #
        self.trial_gb = QGroupBox('Trial Settings')

        #Filename Textbox and Label
        self.fout_labelhead = QLabel('Output File: ')
        self.fout_labelhead.setFont(boldFont)
        fname = "Complete Settings"
        self.fout_vrt_label = QLabel(fname)

        #Start Button
        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.startTest)
        self.start_btn.setMaximumWidth(150)

        #Ankle Angle RadioButtons, ButtonGroup
        self.angle_choice = QButtonGroup(self)
        angle0 = QRadioButton(' 5' + chr(176))
        angle0.setObjectName('PF05')
        angle1 = QRadioButton('10' + chr(176))
        angle1.setObjectName('PF10')
        angle2 = QRadioButton('15' + chr(176))
        angle2.setObjectName('PF15')
        angle3 = QRadioButton('20' + chr(176))
        angle3.setObjectName('PF20')
        angle4 = QRadioButton(' 0' + chr(176))
        angle4.setObjectName('DF00')
        angle5 = QRadioButton(' 5' + chr(176))
        angle5.setObjectName('DF05')
        angle6 = QRadioButton('10' + chr(176))
        angle6.setObjectName('DF10')
        self.angle_choice.addButton(angle0)
        self.angle_choice.addButton(angle1)
        self.angle_choice.addButton(angle2)
        self.angle_choice.addButton(angle3)
        self.angle_choice.addButton(angle4)
        self.angle_choice.addButton(angle5)
        self.angle_choice.addButton(angle6)
        self.angle_choice.buttonClicked.connect(self.angleChanged)

        #Ankle Angle Labels, Fonts
        angleLabel = QLabel('Ankle Angle')
        angleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        angleLabel.setFont(boldFont)
        pfLabel = QLabel('Plantarflexion')
        pfLabel.setFont(italicFont)
        dfLabel = QLabel('Dorsiflexion')
        dfLabel.setFont(italicFont)

        angle_gb = QGroupBox()
        angle_layout = QGridLayout()

        angle_layout.addWidget(angleLabel, 0, 0, 1, 2)
        angle_layout.addWidget(pfLabel, 1, 0)
        angle_layout.addWidget(dfLabel, 1, 1)
        angle_layout.addWidget(angle0, 2, 0)
        angle_layout.addWidget(angle1, 3, 0)
        angle_layout.addWidget(angle2, 4, 0)
        angle_layout.addWidget(angle3, 5, 0)
        angle_layout.addWidget(angle4, 2, 1)
        angle_layout.addWidget(angle5, 3, 1)
        angle_layout.addWidget(angle6, 4, 1)
        angle_layout.setHorizontalSpacing(40)
        angle_gb.setLayout(angle_layout)

        self.flexion_gb = QGroupBox()
        self.flexion_bgroup = QButtonGroup()
        self.flexion_bgroup.buttonClicked.connect(self.flexionChanged)
        self.flexion_rb_pf = QRadioButton("Plantarflexion")
        self.flexion_rb_pf.setObjectName('PF')
        self.flexion_rb_df = QRadioButton("Dorsiflexion")
        self.flexion_rb_df.setObjectName('DF')
        self.flexion_rb_dp = QRadioButton('Dorsiflexion - Plantarflexion')
        self.flexion_rb_dp.setObjectName('DP')

        self.flexion_bgroup.addButton(self.flexion_rb_df)
        self.flexion_bgroup.addButton(self.flexion_rb_pf)
        self.flexion_bgroup.addButton(self.flexion_rb_dp)
        self.flexion_gb_layout = QGridLayout()
        self.flexion_lbl = QLabel('Flexion Direction')
        self.flexion_lbl.setFont(boldFont)


        self.flexion_gb_layout.addWidget(self.flexion_lbl, 0, 0, 1, 1, Qt.AlignHCenter)
        self.flexion_gb_layout.addWidget(self.flexion_rb_df, 1, 0, 1, 1)
        self.flexion_gb_layout.addWidget(self.flexion_rb_pf, 2, 0, 1, 1)
        self.flexion_gb_layout.addWidget(self.flexion_rb_dp, 3, 0, 3, 1, Qt.AlignTop)
        self.flexion_gb.setLayout(self.flexion_gb_layout)


        settings_layout = QGridLayout()
        settings_layout.setVerticalSpacing(2)
        settings_layout.addWidget(angle_gb, 0, 0, 1, 1)
        settings_layout.addWidget(self.flexion_gb, 1, 0, 1, 1)
        settings_layout.addWidget(self.start_btn, 3, 0, 1, 1, Qt.AlignHCenter)
        settings_layout.addWidget(self.fout_labelhead, 4 ,0, 1, 1, Qt.AlignHCenter)
        settings_layout.addWidget(self.fout_vrt_label, 5, 0, 1, 1, Qt.AlignHCenter)
        settings_layout.setRowStretch(0, 8)
        settings_layout.setRowStretch(1, 8)
        settings_layout.setRowStretch(2, 1)
        settings_layout.setRowStretch(3, 1)
        settings_layout.setRowStretch(4, 1)
        settings_layout.setRowStretch(5, 1)



        self.trial_gb.setLayout(settings_layout)


        #Plot Stuff
        xAxisItem = pg.AxisItem(orientation='bottom', showValues=False)
        xAxisItem.showLabel(False)
        yAxisItem = pg.AxisItem(orientation='left', showValues=True)
        yAxisItem.showLabel(False)

        self.plotWin = pg.GraphicsLayoutWidget()
        self.plt = self.plotWin.addPlot(row=0, col=0, rowspan=1, colspan=1,
                                        axisItems={'left': yAxisItem, 'bottom': xAxisItem})
        self.plt.setRange(xRange=(0, 1), yRange=(-1, 1), padding=0.0)
        pen_target = pg.mkPen(color='c', width=30, style=QtCore.Qt.SolidLine)
        self.target_line = pg.PlotCurveItem()
        self.target_line.setPen(pen_target)
        xdata = np.array([0, 1])
        ydata = np.array([0, 0])
        self.curr_tor_line = pg.PlotCurveItem()
        curr_tor_pen = pg.mkPen(color='r', width=10, style=QtCore.Qt.SolidLine)
        self.curr_tor_line.setPen(curr_tor_pen)
        self.zero_line = pg.PlotCurveItem()
        zero_line_pen = pg.mkPen(color='k', width=5, style=QtCore.Qt.DashLine)
        self.zero_line.setPen(zero_line_pen)



        self.target_line.setData(x=xdata, y=ydata)
        self.curr_tor_line.setData(x=xdata, y=ydata)
        self.zero_line.setData(x=xdata, y=ydata)

        self.plt.addItem(self.target_line)
        self.plt.addItem(self.curr_tor_line)
        self.plt.addItem(self.zero_line)

        self.prg_vrt = QProgressBar()
        self.prg_vrt.setMaximum(100)
        self.prg_vrt.setMinimum(0)
        self.prg_vrt.setValue(0)

        self.bottom_gb = QGroupBox()
        self.bottom_gb_layout = QGridLayout()
        self.bottom_gb_layout.addWidget(self.trial_gb, 0, 0, 1, 1)
        self.bottom_gb_layout.addWidget(self.plotWin, 0, 1, 1, 1)
        self.bottom_gb_layout.addWidget(self.prg_vrt, 1, 0, 1, 2)
        self.bottom_gb_layout.setColumnStretch(0, 1)
        self.bottom_gb_layout.setColumnStretch(1, 4)
        self.bottom_gb_layout.setRowStretch(0, 10)
        self.bottom_gb_layout.setRowStretch(1, 1)

        self.bottom_gb.setLayout(self.bottom_gb_layout)

        overall_window_layout = QGridLayout()
        overall_window_layout.addWidget(self.gb_top, 0, 0, 1, 1)
        overall_window_layout.addWidget(self.bottom_gb, 1, 0, 1, 1)
        overall_window_layout.setRowStretch(0, 1)
        overall_window_layout.setRowStretch(1, 9)

        self.setLayout(overall_window_layout)



    def updatePrint(self, q):
        mytimer = QTimer()

        while True:
            if not q.empty():
                item = q.get()

                self.updateTarget(item)
            # item = tcurr
            # self.updateTarget(item)

    def getTestInfo(self):
        ankle_angle = 0
        zero_val = ZEROTBL[ankle_angle]


    def flexionButtonChecked(self):
        for i in range(0, len(self.flexion_bgroup.buttons())):
            if self.flexion_bgroup.buttons()[i].isChecked():
                return True
        return False

    def ankleAngleButtonChecked(self):
        for i in range(0, len(self.angle_choice.buttons())):
            if self.angle_choice.buttons()[i].isChecked():
                return True
        return False

    def makeMsgbox(self, warning_msg):
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setText(warning_msg)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgbox.exec_()


    def startTest(self):

        #Exit if Flexion is not selected
        if self.flexionButtonChecked() == False:
            self.makeMsgbox("Please Select Flexion Direction")
            return

        #Exit if Ankle Angle is not selected
        if self.ankleAngleButtonChecked() == False:
            self.makeMsgbox("Please Select Ankle Angle")
            return

        #Set Plot Ranges for Test
        percentMvc = 0.2
        if self.FLEXION == "DF":
            toptarget = percentMvc*MVCTBL["DF"]
            bottomtarget = 0
            topborder = 1.6*toptarget
            bottomborder = -0.3*toptarget
        elif self.FLEXION == "PF":
            toptarget = 0
            bottomtarget = percentMvc*MVCTBL["PF"]
            topborder = -0.3*bottomtarget
            bottomborder = 1.6*bottomtarget
        elif self.FLEXION == "DP":
            toptarget = percentMvc*MVCTBL["DF"]
            bottomtarget = percentMvc*MVCTBL["PF"]
            topborder = 1.6*toptarget
            bottomborder = 1.6*bottomtarget

        self.plt.setRange(xRange=(0,1), yRange=(bottomborder, topborder), padding=0.0)

        #Run 5 second routine to get new zero
        runTime = 5
        startTime = time.time()
        endTime = startTime + runTime
        zero_lst = []


        while (time.time() < endTime):
            zero_lst.append(tcurr)

            delT = time.time() - startTime
            progress = 100*delT/runTime
            self.prg_vrt.setValue(progress)

        self.prg_vrt.setValue(0)
        zero_lst_np = np.array(zero_lst)
        self.ZERO_VAL = np.mean(zero_lst_np)
        print("Zero Value: {}".format(self.ZERO_VAL))




        # Send Command To DAQ to Start Logging to SD Card
        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(b'S')


        # Expecting 'ENTER FILENAME' string from DAQ
        s = ser.readline()
        t = s.decode('ascii')
        while (t.find("ENTER FILENAME") != -1):
            s = ser.readline()
            t = s.decode('ascii')

        # Send filename to DAQ
        vrt_fname = self.fout_vrt_label.text()
        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(bytes(vrt_fname, 'utf-8'))


        #start running test
        startTime = time.time()
        runTime = 60                   #Test runtime: 180s
        endTime = startTime + runTime


        while (time.time()<endTime):
            # Update plot with new live PRBS and live torque values
            mag = tcurr-self.ZERO_VAL
            self.updateLiveTor(mag, bottomborder, topborder)
            if targetcurr == 0:
                self.updateTarget(bottomtarget)
            elif targetcurr == 1:
                self.updateTarget(toptarget)
            app.processEvents()

            #Update the Voluntary Response Test Progressbar
            delT = time.time() - startTime
            progress = 100*delT/runTime
            self.prg_vrt.setValue(progress)

        # Set Voluntary Response Test Progressbar to 0 (Test Finished)
        self.prg_vrt.setValue(0)


        #Send Command To DAQ to Stop Logging to SD Card
        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(b'Q')


        print('Started writing to file:' + str(vrt_fname))

        #Write Zero Data to file.
        writeToPatientFile('VRT', self.FLEXION, self.ANKLE_ANGLE, self.ZERO_VAL)



    def updateTarget(self, mag):
        xdata = np.array([0, 1])
        ydata = np.array([mag, mag])
        self.target_line.setData(x=xdata, y=ydata)


    def updateLiveTor(self, mag, bborder, tborder):
        xdata = np.array([0, 1])
        if mag > tborder:
            pltmag = tborder
        elif mag < bborder:
            pltmag = bborder
        else:
            pltmag = mag
        ydata = np.array([pltmag, pltmag])
        self.curr_tor_line.setData(x=xdata, y=ydata)

    def resetSer(self):
        global ser
        ser = initSerial()
        self.initSerStatus() #update serial status on standard header

    def initSerStatus(self):
        if ser == -1:
            self.lbl_ser_status.setText('Timeout Occured')
        elif ser == -2:
            self.lbl_ser_status.setText('Not Connected')
        elif ser == -3:
            self.lbl_ser_status.setText('Connected But Not Sending Data')
        elif ser == -4:
            self.lbl_ser_status.setText('All Torque Readings 0')
        elif ser == -5:
            self.lbl_ser_status.setText('Set COM Port')
        else:
            self.lbl_ser_status.setText('Healthy')

    def updateTab(self):
        self.updateStandardHeader()
        self.updateOutputFilename()
        if self.flexionButtonChecked():
            flexButton = self.getCheckedRadioButton(self.flexion_bgroup)
            self.flexionChanged(flexButton)
        if self.ankleAngleButtonChecked():
            angleButton = self.getCheckedRadioButton(self.angle_choice)
            self.angleChanged(angleButton)

    def updateStandardHeader(self):
        self.lbl_pnum.setText(str(PATIENT_NUMBER))
        self.lbl_com.setText(str(COM_PORT))
        self.lbl_tor.setText(str(TORQUE_CHANNEL))
        self.lbl_prbs.setText(str(PRBS_CHANNEL))
        self.initSerStatus()



    def updateOutputFilename(self):
        if "Not Set" in [COM_PORT, TORQUE_CHANNEL, PRBS_CHANNEL, PATIENT_NUMBER]:
            self.fout_vrt_label.setText("Complete Settings")
        else:
            if 'NOT SET' in [self.ANKLE_ANGLE, self.FLEXION]:
                self.fout_vrt_label.setText('Choose Trial Settings')
            else:
                fname = "p" + PATIENT_NUMBER + "_VRT_" + self.ANKLE_ANGLE + "_" + self.FLEXION + ".txt"
                self.fout_vrt_label.setText(fname)

    def getCheckedRadioButton(self, button_group):
        for i in range(0, len(button_group.buttons())):
            if button_group.buttons()[i].isChecked():
                return button_group.buttons()[i]

    def angleChanged(self, i):
        self.ANKLE_ANGLE = i.objectName()
        self.updateOutputFilename()

    def flexionChanged(self, i):
        self.FLEXION = i.objectName()
        self.updateOutputFilename()



class ZeroWindow(QWidget):
    def __init__(self):
        super(ZeroWindow, self).__init__()

        #Trial Variables
        self.ANKLE_ANGLE = "NOT SET"
        self.FLEXION = "NOT SET"



        zerowindowLayout = QVBoxLayout()

        # ------------------------------------------------------------ #
        #               Standard Header                                #
        # ------------------------------------------------------------ #
        self.lbl_sheader_pnum = QLabel('Patient No:')
        self.lbl_sheader_com = QLabel('COM Port:')
        self.lbl_sheader_tor = QLabel('Torque Channel:')
        self.lbl_sheader_prbs = QLabel('PRBS Channel:')
        self.lbl_sheader_ser = QLabel('Serial:')
        self.lbl_sheader_pnum.setFont(boldFont)
        self.lbl_sheader_com.setFont(boldFont)
        self.lbl_sheader_tor.setFont(boldFont)
        self.lbl_sheader_prbs.setFont(boldFont)
        self.lbl_sheader_ser.setFont(boldFont)

        self.lbl_pnum = QLabel(str(PATIENT_NUMBER))
        self.lbl_com = QLabel(str(COM_PORT))
        self.lbl_tor = QLabel(str(TORQUE_CHANNEL))
        self.lbl_prbs = QLabel(str(PRBS_CHANNEL))
        self.lbl_ser_status = QLabel("Not Connected")


        sheader_layout = QGridLayout()
        sheader_layout.addWidget(self.lbl_sheader_pnum, 0, 0, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_pnum, 0, 1, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_com, 0, 2, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_com, 0, 3, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_tor, 0, 4, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_tor, 0, 5, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_prbs, 0, 6, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_prbs, 0, 7, 1, 1, Qt.AlignLeft)
        sheader_layout.addWidget(self.lbl_sheader_ser, 0, 8, 1, 1, Qt.AlignRight)
        sheader_layout.addWidget(self.lbl_ser_status, 0, 9, 1, 1, Qt.AlignLeft)

        self.sheader_gb = QGroupBox()
        self.sheader_gb.setLayout(sheader_layout)
        self.sheader_gb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.btn_ser = QPushButton('Reset Serial')
        self.btn_ser.clicked.connect(self.resetSer)
        self.btn_ser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.gb_top = QGroupBox()
        self.gb_top_layout = QGridLayout()
        self.gb_top_layout.addWidget(self.sheader_gb, 0, 0, 1, 1)
        self.gb_top_layout.addWidget(self.btn_ser, 0, 1, 1, 1)
        self.gb_top_layout.setColumnStretch(0, 6)
        self.gb_top_layout.setColumnStretch(1, 1)
        self.gb_top.setLayout(self.gb_top_layout)

        zerowindowLayout.addWidget(self.gb_top)
        # ------------------------------------------------------------ #
        #               Choose COM Port GroupBox                       #
        # ------------------------------------------------------------ #
        self.trial_gb = QGroupBox('Zero')

        #Filename Textbox and Label
        self.fout_labelhead = QLabel('Output File: ')
        self.fout_labelhead.setFont(boldFont)
        fname = "Complete Settings"
        self.fout_vrt_label = QLabel(fname)

        #Start Button
        self.start_btn = QPushButton('Start Zero')
        self.start_btn.clicked.connect(self.startTest)
        self.start_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #Ankle Angle RadioButtons, ButtonGroup
        self.angle_choice = QButtonGroup(self)
        angle0 = QRadioButton(' 5' + chr(176))
        angle0.setObjectName('PF05')
        angle1 = QRadioButton('10' + chr(176))
        angle1.setObjectName('PF10')
        angle2 = QRadioButton('15' + chr(176))
        angle2.setObjectName('PF15')
        angle3 = QRadioButton('20' + chr(176))
        angle3.setObjectName('PF20')
        angle4 = QRadioButton(' 0' + chr(176))
        angle4.setObjectName('DF00')
        angle5 = QRadioButton(' 5' + chr(176))
        angle5.setObjectName('DF05')
        angle6 = QRadioButton('10' + chr(176))
        angle6.setObjectName('DF10')
        self.angle_choice.addButton(angle0)
        self.angle_choice.addButton(angle1)
        self.angle_choice.addButton(angle2)
        self.angle_choice.addButton(angle3)
        self.angle_choice.addButton(angle4)
        self.angle_choice.addButton(angle5)
        self.angle_choice.addButton(angle6)
        self.angle_choice.buttonClicked.connect(self.angleChanged)

        #Ankle Angle Labels, Fonts
        angleLabel = QLabel('Ankle Angle')
        angleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        angleLabel.setFont(boldFont)
        pfLabel = QLabel('Plantarflexion')
        pfLabel.setFont(italicFont)
        dfLabel = QLabel('Dorsiflexion')
        dfLabel.setFont(italicFont)

        angle_gb = QGroupBox()
        angle_layout = QGridLayout()

        angle_layout.addWidget(angleLabel, 0, 0, 1, 2)
        angle_layout.addWidget(pfLabel, 1, 0, 1, 1, Qt.AlignHCenter)
        angle_layout.addWidget(dfLabel, 1, 1, 1, 1, Qt.AlignHCenter)
        angle_layout.addWidget(angle0, 2, 0, 1, 1, Qt.AlignHCenter)
        angle_layout.addWidget(angle1, 3, 0, 1, 1, Qt.AlignHCenter)
        angle_layout.addWidget(angle2, 4, 0, 1, 1, Qt.AlignHCenter)
        angle_layout.addWidget(angle3, 5, 0, 1, 1, Qt.AlignHCenter)
        angle_layout.addWidget(angle4, 2, 1, 1, 1, Qt.AlignHCenter)
        angle_layout.addWidget(angle5, 3, 1, 1, 1, Qt.AlignHCenter)
        angle_layout.addWidget(angle6, 4, 1, 1, 1, Qt.AlignHCenter)
        angle_layout.setHorizontalSpacing(40)
        angle_gb.setLayout(angle_layout)

        self.lbl_zero_prog = QLabel('Zero Test Progress')

        self.test_prg = QProgressBar()
        self.test_prg.setMinimum(0)
        self.test_prg.setMaximum(100)
        self.test_prg.setValue(0)
        # self.test_prg.hide()


        settings_layout = QGridLayout()
        settings_layout.setHorizontalSpacing(10)
        settings_layout.setVerticalSpacing(2)
        settings_layout.addWidget(angle_gb, 0, 0, 1, 4)
        settings_layout.addWidget(self.start_btn, 1, 0, 1, 1)
        settings_layout.addWidget(self.fout_labelhead, 1 ,1, 1, 1, Qt.AlignRight)
        settings_layout.addWidget(self.fout_vrt_label, 1, 2, 1, 2, Qt.AlignLeft)
        settings_layout.addWidget(self.lbl_zero_prog, 2, 0, 1, 4, Qt.AlignHCenter)
        settings_layout.addWidget(self.test_prg, 3, 0, 1, 4)
        settings_layout.setColumnStretch(0, 1)
        settings_layout.setColumnStretch(1, 1)
        settings_layout.setColumnStretch(2, 1)
        settings_layout.setColumnStretch(3, 1)
        settings_layout.setRowStretch(0, 1)
        settings_layout.setRowStretch(1, 4)
        settings_layout.setRowStretch(2, 1)
        settings_layout.setRowStretch(3, 1)
        settings_layout.setVerticalSpacing(7)

        self.trial_gb.setLayout(settings_layout)


        self.flexion_gb = QGroupBox()
        self.flexion_bgroup = QButtonGroup()
        self.flexion_rb_pf = QRadioButton("Plantarflexion")
        self.flexion_rb_pf.setObjectName('PF')
        self.flexion_rb_df = QRadioButton("Dorsiflexion")
        self.flexion_rb_df.setObjectName('DF')
        self.flexion_bgroup.addButton(self.flexion_rb_df)
        self.flexion_bgroup.addButton(self.flexion_rb_pf)
        self.flexion_gb_layout = QGridLayout()
        self.flexion_lbl = QLabel('Flexion Direction')
        self.flexion_lbl.setFont(boldFont)
        self.flexion_gb_layout.addWidget(self.flexion_lbl, 0, 0, 1, 1, Qt.AlignHCenter)
        self.flexion_gb_layout.addWidget(self.flexion_rb_df, 1, 0, 1, 1)
        self.flexion_gb_layout.addWidget(self.flexion_rb_pf, 2, 0, 4, 1, Qt.AlignTop)
        self.flexion_gb.setLayout(self.flexion_gb_layout)
        self.flexion_bgroup.buttonClicked.connect(self.flexionChanged)

        self.btn_mvc_start = QPushButton('Start MVC')
        self.btn_mvc_start.clicked.connect(self.startMvc)

        self.lbl_fouthead_mvc = QLabel('Output File:')
        self.lbl_fouthead_mvc.setFont(boldFont)

        self.lbl_fout_mvc = QLabel('Complete Settings')

        self.lbl_mvc_prog = QLabel('MVC Test Progress')

        self.btn_man_zero = QPushButton('Manually Set DF00 Zero')
        self.btn_man_zero.clicked.connect(self.setManZero)
        self.txt_man_zero = QLineEdit()


        self.pbar_mvc_test = QProgressBar()
        self.pbar_mvc_test.setMinimum(0)
        self.pbar_mvc_test.setMaximum(100)
        self.pbar_mvc_test.setValue(0)

        self.mvc_gb = QGroupBox('MVC')
        self.mvc_gb_layout = QGridLayout()
        self.mvc_gb_layout.addWidget(self.flexion_gb, 0, 0, 1, 4)
        self.mvc_gb_layout.addWidget(self.btn_mvc_start, 1, 0, 1, 1)
        self.mvc_gb_layout.addWidget(self.lbl_fouthead_mvc, 1, 1, 1, 1, Qt.AlignRight)
        self.mvc_gb_layout.addWidget(self.lbl_fout_mvc, 1, 2, 1, 2, Qt.AlignLeft)
        self.mvc_gb_layout.addWidget(self.lbl_mvc_prog, 2, 0, 1, 4, Qt.AlignHCenter)
        self.mvc_gb_layout.addWidget(self.pbar_mvc_test, 3, 0, 1, 4)
        self.mvc_gb_layout.setColumnStretch(0, 1)
        self.mvc_gb_layout.setColumnStretch(1, 1)
        self.mvc_gb_layout.setColumnStretch(2, 1)
        self.mvc_gb_layout.setColumnStretch(3, 1)
        self.mvc_gb_layout.setRowStretch(0, 12)
        self.mvc_gb_layout.setRowStretch(1, 1)
        self.mvc_gb_layout.setRowStretch(2, 1)
        self.mvc_gb_layout.setRowStretch(3, 1)
        self.mvc_gb.setLayout(self.mvc_gb_layout)

        self.central_gb = QGroupBox()
        self.central_gb_layout = QGridLayout()
        self.central_gb_layout.addWidget(self.trial_gb, 0, 0, 1, 1)
        self.central_gb_layout.addWidget(self.mvc_gb, 0, 1, 1, 1)
        self.central_gb_layout.setColumnStretch(0, 1)
        self.central_gb_layout.setColumnStretch(1, 1)
        self.central_gb.setLayout(self.central_gb_layout)



        zerowindowLayout.addWidget(self.central_gb)


        #Lower Part of Zero Window
        self.zero_lower_gb = QGroupBox()
        self.zero_lower_layout = QGridLayout()
        self.btn_getFiles = QPushButton('Get Zero Files')
        self.btn_getFiles.clicked.connect(self.getZeroFiles)

        self.btn_getFiles_mvc = QPushButton("Get MVC Files")
        self.btn_getFiles_mvc.clicked.connect(self.getMvcFiles)

        self.zero_table = QTableWidget()
        self.zero_table.setColumnCount(2)
        self.zero_table.setRowCount(len(ZEROTBL))
        headerLabel = ('Ankle Angle', 'Zero Offset (N-m)')
        self.zero_table.setHorizontalHeaderLabels(headerLabel)
        self.populateZeroTable()
        self.zero_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.zero_table.horizontalHeader().setFont(boldFont)

        self.tbl_mvc = QTableWidget()
        self.tbl_mvc.setColumnCount(2)
        self.tbl_mvc.setRowCount(2)
        mvcHeaderLabel = ('Flexion', 'MVC (N-m)')
        self.tbl_mvc.setHorizontalHeaderLabels(mvcHeaderLabel)
        self.tbl_mvc.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_mvc.horizontalHeader().setFont(boldFont)
        self.populateMVCTable()

        self.zero_lower_layout.addWidget(self.btn_getFiles, 0, 0, 1, 1)
        self.zero_lower_layout.addWidget(self.btn_getFiles_mvc, 0, 4, 1, 1)
        self.zero_lower_layout.addWidget(self.btn_man_zero, 0, 6, 1, 1)
        self.zero_lower_layout.addWidget(self.txt_man_zero, 0, 7, 1, 1)
        self.zero_lower_layout.addWidget(self.zero_table, 1, 0, 1, 4)
        self.zero_lower_layout.addWidget(self.tbl_mvc, 1, 4, 1, 4)
        for i in range(0, 8):
            self.zero_lower_layout.setColumnStretch(i, 1)

        self.zero_lower_gb.setLayout(self.zero_lower_layout)





        zerowindowLayout.addWidget(self.zero_lower_gb)
        zerowindowLayout.setStretch(2,2)

        self.setLayout(zerowindowLayout)

    def setManZero(self):
        tempZero = self.txt_man_zero.text()
        if is_number(tempZero):
            ZEROTBL['DF00'] = float(tempZero)
        self.populateZeroTable()

    def resetSer(self):
        global ser
        ser = initSerial()
        self.initSerStatus()

    def initSerStatus(self):
        if ser == -1:
            self.lbl_ser_status.setText('Timeout Occured')
        elif ser == -2:
            self.lbl_ser_status.setText('Not Connected')
        elif ser == -3:
            self.lbl_ser_status.setText('Connected But Not Sending Data')
        elif ser == -4:
            self.lbl_ser_status.setText('All Torque Readings 0')
        elif ser == -5:
            self.lbl_ser_status.setText('Set COM Port')
        else:
            self.lbl_ser_status.setText('Healthy')


    def startMvc(self):
        # Run 5 second zero routine before MVC Test
        global ser
        runTime = 5
        startTime = time.time()
        endTime = startTime + runTime
        zero_lst = []
        while (time.time() < endTime):
            zero_lst.append(tcurr)
            # Updates Progressbar
            delT = time.time() - startTime
            progress = 100*delT/runTime
            self.pbar_mvc_test.setValue(progress)

        #Set progressbar = 0 when zero routine is done.
        self.pbar_mvc_test.setValue(0)

        zero_lst_np = np.array(zero_lst)
        self.ZERO_VAL = np.mean(zero_lst_np)
        ZEROTBL['DF00'] = self.ZERO_VAL
        print("Zero Value: {}".format(self.ZERO_VAL))


        #Send command to DAQ to start writing MVC file
        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(b'S')

        #Expecting 'ENTER FILENAME' from DAQ
        s = ser.readline()
        t = s.decode('ascii')
        while (t.find("ENTER FILENAME") != -1):
            s = ser.readline()
            t = s.decode('ascii')
            print(t)

        #Send filename to DAQ
        mvc_fname = self.lbl_fout_mvc.text()
        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(bytes(mvc_fname, 'utf-8'))

        # Start MVC Test
        init_time = time.time()
        del_t = time.time() - init_time

        while (del_t < 3):
            #Update Progressbar while test is running
            self.pbar_mvc_test.setValue(del_t/3*100)
            del_t = time.time()-init_time

        # Set progressbar = 0 when test is done
        self.pbar_mvc_test.setValue(0)

        # Send command to DAQ to stop writing file to SD card
        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(b'Q')


        #Update tables and write to patient file
        self.populateZeroTable()
        writeToPatientFile('MVC', self.FLEXION, self.ANKLE_ANGLE, self.ZERO_VAL)


    def getZeroFiles(self):
        #Open filedialog box
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "Text Files (*.txt)", options=options)
        if files:
            for f in files:
                #Zero Files Operations
                tempData = self.parseFilename(f, 'ZERTST')
                if tempData != -1:
                    temp_aa = tempData[1]
                    temp_data = np.loadtxt(f, dtype = float, delimiter=',')
                    temp_data = temp_data[:,TORQUE_CHANNEL]
                    ZEROTBL[temp_aa] = np.mean(temp_data)

            #Populate Tables With New Data
            self.populateZeroTable()


    def getMvcFiles(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "Text Files (*.txt)", options=options)
        if files:
            for f in files:
                #MVC File Operations
                tempData = self.parseFilename(f, 'MaxVolCo')
                if tempData != -1:
                    temp_flexion = tempData[1]
                    temp_data = np.loadtxt(f, dtype=float, delimiter=',')
                    temp_data = temp_data[:, TORQUE_CHANNEL]
                    temp_zero = ZEROTBL['DF00']
                    if temp_zero == "Not Set":
                        self.filenameMsgbox("Set 'DF00' Zero")
                        return
                    if temp_flexion == "DF":
                        MVCTBL[temp_flexion] = np.amax(temp_data)-temp_zero
                    elif temp_flexion == "PF":
                        MVCTBL[temp_flexion] = np.amin(temp_data)-temp_zero

            #Populate Tables With New Data
            self.populateMVCTable()


    def parseFilename(self, fname, tsttype):
        #fpath = fname[0:fname.rfind('/')+1]  ---------- useless for now
        fname = fname[fname.rfind('/')+1:]
        [fname, ext] = fname.split('.')
        if ext != 'txt':
            self.filenameMsgbox("Data must come from text files (i.e. have .txt extension)\n\n" + fname + '.' + ext + "is not a valid data file")
            return -1
        else:
            fnameparts = fname.split('_')
            temp_pnum = fnameparts[0].strip('p')
            if temp_pnum != PATIENT_NUMBER:
                self.filenameMsgbox("Data file did not match patient number.")
                return -1
            temp_testtype = fnameparts[1]
            temp_aa = fnameparts[2]
            if temp_testtype == "MaxVolCo":
                temp_fl = fnameparts[2]
                return [temp_testtype, temp_fl]
            elif temp_testtype == "ZERTST":
                return [temp_testtype, temp_aa]

    def filenameMsgbox(self, warning_msg):
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setText(warning_msg)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgbox.exec_()


    def populateMVCTable(self):
        ind = 0
        for col in MVCTBL:
            fl = col
            if type(MVCTBL[col]) not in [int, float]:
                val = MVCTBL[col]
            else:
                val = MVCTBL[col]#*SERNUM2TOR
            self.tbl_mvc.setItem(ind, 0, QTableWidgetItem(fl))
            self.tbl_mvc.setItem(ind, 1, QTableWidgetItem(str(val)))
            ind = ind + 1



    def populateZeroTable(self):
        ind = 0
        self.zero_table.setRowCount(0)
        self.zero_table.setRowCount(len(ZEROTBL))
        for col in ZEROTBL:
            aa = col
            if type(ZEROTBL[col]) not in [int, float]:
                val = ZEROTBL[col]
            else:
                val = ZEROTBL[col]#*SERNUM2TOR
            self.zero_table.setItem(ind, 0, QTableWidgetItem(aa))
            self.zero_table.setItem(ind, 1, QTableWidgetItem(str(val)))
            ind = ind + 1


    def updateTab(self):
        self.updateStandardHeader()
        self.updateOutputFilename()


    def updateStandardHeader(self):
        self.lbl_pnum.setText(str(PATIENT_NUMBER))
        self.lbl_com.setText(str(COM_PORT))
        self.lbl_tor.setText(str(TORQUE_CHANNEL))
        self.lbl_prbs.setText(str(PRBS_CHANNEL))
        self.initSerStatus()



    def updateOutputFilename(self):
        if "Not Set" in [COM_PORT, TORQUE_CHANNEL, PRBS_CHANNEL, PATIENT_NUMBER]:
            self.fout_vrt_label.setText("Complete Settings")
        else:
            if 'NOT SET' in [self.ANKLE_ANGLE]:
                self.fout_vrt_label.setText('Choose Trial Settings')
            else:
                fname = "p" + PATIENT_NUMBER + "_ZERTST_" + self.ANKLE_ANGLE + ".txt"
                self.fout_vrt_label.setText(fname)

    def updateOutputMVCFilename(self):
        if "Not Set" in [COM_PORT, TORQUE_CHANNEL, PRBS_CHANNEL, PATIENT_NUMBER]:
            self.lbl_fout_mvc.setText("Complete Settings")
        else:
            if "NOT SET" in [self.FLEXION]:
                self.lbl_fout_mvc.setText('Choose Trial Settings')
            else:
                fname = "p" + PATIENT_NUMBER + "_MaxVolCo_" + self.FLEXION + ".txt"
                self.lbl_fout_mvc.setText(fname)

    def angleChanged(self, i):
        self.ANKLE_ANGLE = i.objectName()
        self.updateOutputFilename()

    def flexionChanged(self, i):
        self.FLEXION = i.objectName()
        self.updateOutputMVCFilename()

    def startTest(self):

        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(b'S')
        s = ser.readline()
        t = s.decode('ascii')
        while (t.find("ENTER FILENAME") != -1):
            s = ser.readline()
            t = s.decode('ascii')
        zero_fname = self.fout_vrt_label.text()

        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(bytes(zero_fname, 'utf-8'))



        self.test_prg.setValue(0)
        init_time = time.time()
        del_t = time.time() - init_time
        while (del_t < 3):
            self.test_prg.setValue(del_t/3*100)
            del_t = time.time()-init_time
        self.test_prg.setValue(0)

        ser.flush()
        ser.flushInput()
        ser.flushOutput()
        ser.write(b'Q')








if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
    window_width = screen_width * 0.75
    window_height = screen_height * 0.75
    writeToPatientFile('test1', 'test2', 'test3', 'test4')

    ex = App()
    sys.exit(app.exec_())

from PyQt5 import QtWidgets, uic, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import sys
from pyqt_realtime_log_widget import LogWidget
import serial
import threading
import re
import time

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GUI.ui", self)
        self.tb = self.ui.textBrowser
        self.GraphWidget = PlotWidget()
        self.GraphWidget.setXRange(0,10,padding=0)
        self.ui.frame_21.layout().addWidget(self.GraphWidget)
        self.ser = serial.Serial('COM5',timeout=1)
        self.data = []
        self.indices = []
        self.data_line = self.GraphWidget.plot(pen='r',name='temperature')
        self.index = 0

        self.ui.pushButton.clicked.connect(self.ClearTB)

        threading.Thread(target=self.ReadData).start()

    def ReadData(self):
        while True:
            self.tb.verticalScrollBar().setValue(self.tb.verticalScrollBar().maximum())
            data = str(self.ser.readline().decode('ascii'))
            data = data.replace('\r\n','')
            if data != '':
                self.data.append(float(data))
                self.index += 1
                self.indices.append(self.index)
                self.tb.verticalScrollBar().setValue(self.tb.verticalScrollBar().maximum())
                self.data_line.setData(self.indices,self.data)
                self.UpdateViewBox()
                if float(data)>70:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    warn = '[' + str(current_time) + ']: ' + 'Abnormal temperature(%.2f)' %float(data) 
                    self.tb.append(warn)

    def UpdateViewBox(self):
        if self.index > 10:
            self.GraphWidget.setXRange(self.index-10,self.index)

    def ClearTB(self):
        self.tb.clear()
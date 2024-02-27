from PyQt5 import QtWidgets, uic, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import sys
import serial
import threading
import time

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GUI.ui", self)
        self.tb = self.ui.textBrowser
        self.GraphWidget = PlotWidget()
        self.GraphWidget.setXRange(0,10,padding=0)
        self.ui.frame_21.layout().addWidget(self.GraphWidget)
        self.legend = self.GraphWidget.addLegend()
        self.ser = serial.Serial('COM5',timeout=1)
        self.Tdata = []
        self.Hdata = []
        self.times = []
        self.data_line_t = self.GraphWidget.plot(pen='r',name='temperature')
        self.data_line_h = self.GraphWidget.plot(pen='g',name='humidity')
        self.second = 0
        self.ispaused = False

        self.ui.pushButton.clicked.connect(self.ClearTB)
        self.ui.actionPlay.triggered.connect(self.PlayPause)

        threading.Thread(target=self.ReadData).start()

    def ReadData(self):
        start = time.time()
        while True:
            self.tb.verticalScrollBar().setValue(self.tb.verticalScrollBar().maximum())
            data = str(self.ser.readline().decode('ascii'))
            data = data.replace('\r\n','')
            if data != '':
                data = data.split('/')
                Tdata = data[0]
                Hdata = data[1]
            else:
                Tdata = Hdata = ''

            seconds = time.time()
            if Tdata != '' and Hdata != '' and self.ispaused == False:
                self.Tdata.append(float(Tdata))
                self.Hdata.append(float(Hdata))
                self.second = seconds - start
                self.times.append(self.second)
                self.tb.verticalScrollBar().setValue(self.tb.verticalScrollBar().maximum())
                self.data_line_t.setData(self.times, self.Tdata)
                self.data_line_h.setData(self.times, self.Hdata)
                self.UpdateViewBox()
                if float(Tdata)>25 or float(Tdata)<20:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    warn = '[' + str(current_time) + ']: ' + 'Abnormal temperature(%.2f °C)' %float(Tdata)
                    self.tb.append(warn)
                if  float(Hdata)>60:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    warn = '[' + str(current_time) + ']: ' + 'Humidity(%.2f °C)' %float(Hdata)
                    self.tb.append(warn)
                
    def UpdateViewBox(self):
        if self.second > 10:
            self.GraphWidget.setXRange(self.second-10,self.second)

    def ClearTB(self):
        self.tb.clear()

    def PlayPause(self):
        if self.ispaused == False:
            self.ispaused = True
        else:
            self.ispaused = False
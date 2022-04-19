import sys,os
import math

# load UI libraries
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#load main window
from MainWindow import Ui_MainWindow
from PyQt5 import QtGui
import numpy as np
import pandas as pd
import utils
import fft

import pyqtgraph as pg
from pyqtgraph import PlotWidget
import random

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        # inherit (QMainWindow, Ui_MainWindow) properties of the parent class

        super(MainWindow,self).__init__()
        # Initialize interface components
        self.setupUi(self)
        self.label.setScaledContents(True)
        self.loadButton.clicked.connect(self.load)
        self.plotButton.clicked.connect(self.test)
        layout = QVBoxLayout(self.widget)

        self.plotWidget_ted = PlotWidget(self)
        label_style = {"font-family": "System", "font-size": "12pt"}

        self.plotWidget_ted.setLabel('bottom', "Time (us)")
        self.plotWidget_ted.setLabel('left', "Voltage (V)")
        self.plotWidget_ted.getAxis('bottom').setLabel('Time (us)', **label_style)
        self.plotWidget_ted.getAxis('left').setLabel('Voltage (V)', **label_style)
        self.plotWidget_ted.setBackground('w')
        self.plotWidget_ted.showGrid(x=True, y=True)


        layout.addWidget(self.plotWidget_ted)

        self.plotWidget_ted.plotItem.setAutoVisible(y=True)
        self.vertical_line0 = pg.InfiniteLine(angle=90)
        self.horizontal_line0 = pg.InfiniteLine(angle=0, movable=False)
        self.crosshair_color0 = (196, 220, 255)
        self.vertical_line0.setPen(self.crosshair_color0)
        self.horizontal_line0.setPen(self.crosshair_color0)
        self.plotWidget_ted.setAutoVisible(y=True)
        self.plotWidget_ted.addItem(self.vertical_line0, ignoreBounds=True)
        self.plotWidget_ted.addItem(self.horizontal_line0, ignoreBounds=True)

        self.crosshair_update0 = pg.SignalProxy(self.plotWidget_ted.scene().sigMouseMoved, rateLimit=60,
                                               slot=self.update_crosshair0)
        layout = QVBoxLayout(self.widget_2)

        self.plotWidget_ted1 = PlotWidget(self)
        self.plotWidget_ted1.setLabel('bottom', "Frequency (MHz)")
        self.plotWidget_ted1.setLabel('left', "Amplitude (dBFS)")
        self.plotWidget_ted1.getAxis('bottom').setLabel('Frequency (MHz)', **label_style)
        self.plotWidget_ted1.getAxis('left').setLabel('Amplitude (dBFS)', **label_style)
        self.plotWidget_ted1.setBackground('w')
        self.plotWidget_ted1.showGrid(x=True, y=True)
        layout.addWidget(self.plotWidget_ted1)

        #self.crosshair_plot_widget.plotItem.setAutoVisible(y=True)
        self.plotWidget_ted1.plotItem.setAutoVisible(y=True)
        self.vertical_line1= pg.InfiniteLine(angle=90)
        self.horizontal_line1 = pg.InfiniteLine(angle=0, movable=False)
        self.crosshair_color = (196, 220, 255)
        self.vertical_line1.setPen(self.crosshair_color)
        self.horizontal_line1.setPen(self.crosshair_color)
        self.plotWidget_ted1.setAutoVisible(y=True)
        self.plotWidget_ted1.addItem(self.vertical_line1, ignoreBounds=True)
        self.plotWidget_ted1.addItem(self.horizontal_line1, ignoreBounds=True)

        self.crosshair_update1 = pg.SignalProxy(self.plotWidget_ted1.scene().sigMouseMoved, rateLimit=60,
                                               slot=self.update_crosshair1)

    def update_crosshair0(self, event):
        """Paint crosshair on mouse"""

        coordinates = event[0]
        if self.plotWidget_ted.sceneBoundingRect().contains(coordinates):
            mouse_point = self.plotWidget_ted.plotItem.vb.mapSceneToView(coordinates)
            index = mouse_point.x()
            if(10**-6<abs(mouse_point.x())<10**-5):
                x_col = (mouse_point.x())* 10 ** 6
            elif(10**-9<abs(mouse_point.x())<10**-6):
                x_col = (mouse_point.x()) * 10 ** 9
            else:
                x_col = (mouse_point.x())

            self.plotWidget_ted.setTitle(
                    "<span style='font-size: 12pt'>Time=%0.5f,   <span style='color: red'>Voltage=%0.3f</span>" % (
                        ( x_col ), mouse_point.y())) #x in nano sec
            self.vertical_line0.setPos(mouse_point.x())
            self.horizontal_line0.setPos(mouse_point.y())

    def update_crosshair1(self, event):
        """Paint crosshair on mouse"""

        coordinates = event[0]
        if self.plotWidget_ted1.sceneBoundingRect().contains(coordinates):
            mouse_point = self.plotWidget_ted1.plotItem.vb.mapSceneToView(coordinates)
            index = mouse_point.x()
            self.plotWidget_ted1.setTitle(
                    "<span style='font-size: 12pt'>Frequecny=%0.1f,   <span style='color: red'>Amplitude=%0.3f</span>" % (
                        (mouse_point.x()), mouse_point.y())) #x in Ghz
            self.vertical_line1.setPos(mouse_point.x())
            self.horizontal_line1.setPos(mouse_point.y())



    def get_crosshair_plot_layout(self):
        return self.layout

    def load(self):

        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "choose file",
                                                                "./",
                                                                "Excel File (*.csv)")  # set file name filter
        if fileName_choose != "":
            self.lineEdit.setText(fileName_choose)
            # QMessageBox.information(self, "file select", "successful", QMessageBox.Close)

    def test(self):

        path = self.lineEdit.text()
        if path != "":

            data = pd.read_csv(path)

            sampled_data = data[0:]['Amplitude (LSB) - Signal']
            time = data[0:]['Time (us)']

            sampled_data_volts = np.zeros(len(sampled_data))
            no_att_data_volts = np.zeros(len(sampled_data))

            for j in range(len(sampled_data)):
                sampled_data_volts[j] = utils.lsb_to_volt(sampled_data[j])

            re_time = np.zeros(len(sampled_data))

            for i in range(len(sampled_data)):
               # re_time[i] = utils.ready_time(re_time[i-1]+(1/(1024*10**9)))
               re_time[i] = re_time[i - 1] + (1 / (1024 * 10**6))
            #Ts = re_time.max() / len(re_time)  # sampling interval in time

            # self.plotWidget_ted.plot(re_time, sampled_data_volts,pen='green')


            #xf, yf, freq = fft.GetFFT(sampled_data,re_time)

            xf, yf, freq = fft.GetFFTdB(sampled_data, time)
            for k in range(len(sampled_data)):
                no_att_data_volts[k] = utils.attenuation(sampled_data_volts[k], freq)
            self.plotWidget_ted.clear()
            self.plotWidget_ted1.clear()
            self.plotWidget_ted.plot(time, sampled_data_volts, pen=pg.mkPen(width=2, color='r'))
            self.plotWidget_ted1.plot(xf, yf,  pen=pg.mkPen(width=2, color='g'))

            # QMessageBox.information(self, "plot", "successful", QMessageBox.Close)



        else:
            QMessageBox.information(self, "reminder", "file not select", QMessageBox.Close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
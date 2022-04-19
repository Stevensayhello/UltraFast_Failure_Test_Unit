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
from scipy.fft import fft, fftfreq
from pyqtgraph import PlotWidget

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        # inherit (QMainWindow, Ui_MainWindow) properties of the parent class

        super(MainWindow,self).__init__()
        # Initialize interface components
        self.setupUi(self)
        self.label.setScaledContents(True)
        self.pushButton.clicked.connect(self.load)
        self.pushButton_2.clicked.connect(self.test)
        layout = QVBoxLayout(self.widget)

        self.plotWidget_ted = PlotWidget(self)
        font = QtGui.QFont()
        font.setFamily("System")
        #fontCss = {'font-family': "System New Roman", 'font-size': '15pt', "color": "black"}


        self.plotWidget_ted.setLabel('bottom', "TIME(s)", size='24pt')
        self.plotWidget_ted.setLabel('left', "Voltage(V)", size='24pt')
        #self.plotWidget_ted.getAxis('bottom').setLabel(**fontCss)
        self.plotWidget_ted.setBackground('w')
        self.plotWidget_ted.showGrid(x=True, y=True)
        layout.addWidget(self.plotWidget_ted)
        layout = QVBoxLayout(self.widget_2)

        self.plotWidget_ted1 = PlotWidget(self)
        self.plotWidget_ted1.setLabel('bottom', "Frequency(Hz)", size='24pt')
        self.plotWidget_ted1.setLabel('left', "Amplitude", size='24pt')
        self.plotWidget_ted1.setBackground('w')
        self.plotWidget_ted1.showGrid(x=True, y=True)
        layout.addWidget(self.plotWidget_ted1)

    def load(self):

        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "choose file",
                                                                "./",
                                                                "Excel File (*.csv)")  # set file name filter
        if fileName_choose != "":
            self.lineEdit.setText(fileName_choose)
            QMessageBox.information(self, "file select", "successful", QMessageBox.Close)

    def test(self):
        path = self.lineEdit.text()
        if path != "":
            data = pd.read_csv(path)
            time = data[0:]['Time (s) - Signal']

            re_time = np.zeros(len(time))
            for i in range(len(time)):
                re_time[i] = utils.ready_time(time[i])

            sampled_data = data[0:]['Amplitude (LSB) - Signal']

            sampled_data_volts = np.zeros(len(sampled_data))
            no_att_data_volts = np.zeros(len(sampled_data))

            for j in range(len(sampled_data)):
                sampled_data_volts[j] = utils.lsb_to_volt(sampled_data[j])
                no_att_data_volts[j] = utils.attenuation(sampled_data_volts[j], freq=20 * 10 ** 6)


            # self.plotWidget_ted.plot(re_time, sampled_data_volts,pen='green')
            self.plotWidget_ted.plot(re_time, no_att_data_volts,pen='red')
            # plt.plot(re_time, sampled_data_volts, color='green')
            # plt.plot(re_time, no_att_data_volts, color='red')
            # plt.show()
            #
            # FFT
            # normalization
            normalized_data = np.int16((no_att_data_volts / no_att_data_volts.max()) * 32767)
            period = re_time.max()/len(re_time)
            # Number of samples in normalized_tone
            N = len(sampled_data)

            yf = fft(normalized_data)

            xf = fftfreq(N, period)

            # plt.plot(xf, np.abs(yf))
            self.plotWidget_ted1.plot(xf, np.abs(yf), pen='green', width = '10')
            QMessageBox.information(self, "plot", "successful", QMessageBox.Close)



        else:
            QMessageBox.information(self, "reminder", "file not select", QMessageBox.Close)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
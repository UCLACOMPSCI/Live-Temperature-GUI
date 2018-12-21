#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 22:07:15 2018

@author: David
"""

import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
import serial # import Serial library
import numpy # import Numpy
import matplotlib.pyplot as plt # import matplotlib library
from drawnow import * # import everything from drawnow


tempF1 = []
tempF2 = []
tempF3 = []
tempF4 = []
pressure1 = []
pressure2 = []

arduinoData = serial.Serial('/dev/cu.usbmodem1411', 9600) # Creating serial object
plt.ion() # tell matplotlib you want interactive mode to plot live data
count = 0

class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle('pyqt5 Tut')
        # self.setWindowIcon(QIcon('pic.png'))
        self.home()
        
    def makeFigure(): # Create function that makes desired plot
        plt.xlim(1,50)
        plt.ylim(35,100) # set range for y axis so graph doesn't rescale
        plt.title('Live Data') # Title of plot
        plt.grid(True) # Displays grid
        plt.ylabel('Temp (Farenheit)') # y axis label
        plt.plot(tempF1, 'ro-', label='Probe 1') # plots each probe
        plt.plot(tempF2, 'go-', label='Probe 2')
        plt.plot(tempF3, 'mo-', label='Probe 3')
        plt.plot(tempF4, 'co-', label='Probe 4')
        plt.legend(loc='upper left') # legend for probes
        plt2=plt.twinx() # making 2nd y axis for pressure
        plt.ylim(1,10) # range for 2nd y axis
        plt2.plot(pressure1, 'b^-', label='Photovoltage (V)')
        plt2.set_ylabel('Photovoltage (V)') # label 2nd y axis
            # different syntax than previously
        plt2.legend(loc='upper right')

    def home(self):
        btn = QPushButton('quit', self)
        btn.clicked.connect(self.close_application)

        btn.resize(btn.sizeHint())  #set to acceptable size automatic
        btn.move(0, 0)
        self.show()

    def close_application(self):
        print('whooo so custom')
        sys.exit()

def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())

run()
while True: # running continuously
    while (arduinoData.inWaiting()==0): # Wait here until there's data
        pass #do nothing
    arduinoString = arduinoData.readline() # read from arduino as a string
    dataArray = arduinoString.split(',') # split into strings
    temp1 = float(dataArray[0]) # turned into decimals 
    temp2 = float(dataArray[1])
    temp3 = float(dataArray[2])
    temp4 = float(dataArray[3])
    P1 = float(dataArray[4])
    P2 = float(dataArray[5])
    
    # need to create arrays in order to graph
    tempF1.append(temp1) # building temperature array
    tempF2.append(temp2)
    tempF3.append(temp3)
    tempF4.append(temp4)
    pressure1.append(P1) # building pressure array
    pressure2.append(P2)
    
    drawnow(makeFigure) # call drawnow to update live graph
    plt.pause(.0000001) # needed for things to run smoothly
    count = count + 1
    
    if (count > 50):
        tempF1.pop(0) # making sure only 50 data points plotted
        tempF2.pop(0) # at all times
        tempF3.pop(0)
        tempF4.pop(0)
        pressure1.pop(0)
        pressure2.pop(0)
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.Qt import *
import random
import threading 
import time
import numpy as np
import pandas as pd
from scipy import signal
import serial
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


global minDisparity
minDisparity = 0;
global numDisparities
numDisparities = 32;
global blockSize
blockSize = 1;
global disp12MaxDiff;
disp12MaxDiff = 2;
global uniquenessRatio
uniquenessRatio= 15;
global speckleWindowSize
speckleWindowSize = 100;
global speckleRange
speckleRange = 5;

#2 программа pqyt для создания интерфейса    
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
               
        self.setMinimumSize(QSize(300, 200))    
        self.setWindowTitle("BCI") 
        pybutton = QPushButton('Click me', self)        
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 50)        
    def clickMethod(self):
        print('Clicked Pyqt button.')

        seconWin.show()
        mainWin.close()

class second_window(QWidget):

    def __init__(self):
        print ("start")       
        QWidget.__init__(self)

        self.setMinimumSize(QSize(600, 500))    
        self.setWindowTitle("Iron_BCI") 
        self.figure = plt.figure(figsize=(0,2,),facecolor='y',  edgecolor='r') #  color only                     
        self.canvas = FigureCanvas(self.figure)
        self.figure.subplots_adjust(0.2, 0.4, 0.8, 1)      
        pybutton = QPushButton('graph', self)        
        global axis_x
        axis_x=0
        pybutton.clicked.connect(self.clickMethod)
        pybutton.move(50, 10)
        pybutton.resize(100,32)        
        layout = QVBoxLayout()
        layout.setContentsMargins(50,100,0,11) # move background
        layout.setGeometry(QRect(0, 0, 80, 68))# nothing  
        layout.addWidget(self.canvas)
        
      # input dataufoff value  
        self.le_num1 = QLineEdit()
        self.le_num1.setFixedSize(50, 20) # size
        self.le_num1.move(100, 110)  
        self.pb_num1 = QPushButton('minDisparity')
        self.pb_num1.setFixedSize(150, 60) # size
        self.pb_num1.clicked.connect(self.show_dialog_num1)
        self.pb_num1.move(100, 110)   
    #    layout.addWidget(self.le_num1)            
        layout.addWidget(self.pb_num1)
        self.setLayout(layout)
        
        # stop input data
        # start input data fps
        self.le_num2 = QLineEdit()
        self.le_num2.setFixedSize(50, 20) # size                        
        self.pb_num2 = QPushButton('numDisparities')
        self.pb_num2.setFixedSize(150, 60) # size
        self.pb_num2.clicked.connect(self.show_dialog_num2)
      # layout.addWidget(self.le_num2)       
        self.pb_num2.move(90, 100)        
        layout.addWidget(self.pb_num2)
        self.setLayout(layout)
        # stop input data fps
        # start input data low filter
        self.le_num3 = QLineEdit()
        self.le_num3.setFixedSize(50, 20) # size                        
        self.pb_num3 = QPushButton('blockSize')
        self.pb_num3.setFixedSize(150, 60) # size
        self.pb_num3.clicked.connect(self.show_dialog_num3)     
       #  layout.addWidget(self.le_num3)       
        self.pb_num3.move(190, 100)        
        layout.addWidget(self.pb_num3)
        self.setLayout(layout)
        # stop input data filter
        #disp12MaxDiff
        self.le_num4 = QLineEdit()
        self.le_num4.setFixedSize(50, 20) # size                        
        self.pb_num4 = QPushButton('disp12MaxDiff')
        self.pb_num4.setFixedSize(150, 60) # size
        self.pb_num4.clicked.connect(self.show_dialog_num4)     
      #   layout.addWidget(self.le_num4)       
        self.pb_num4.move(90, 200)        
        layout.addWidget(self.pb_num4)
        self.setLayout(layout)           
        #uniquenessRatio
        self.le_num5 = QLineEdit()
        self.le_num5.setFixedSize(50, 20) # size                        
        self.pb_num5 = QPushButton('uniquenessRatio')
        self.pb_num5.setFixedSize(150, 60) # size
        self.pb_num5.clicked.connect(self.show_dialog_num5)     
        # layout.addWidget(self.le_num5)       
        self.pb_num5.move(190, 200)        
        layout.addWidget(self.pb_num5)
        self.setLayout(layout)        
        #speckleWindowSize
        self.le_num6 = QLineEdit()
        self.le_num6.setFixedSize(50, 20) # size                        
        self.pb_num6 = QPushButton('speckleWindowSize')
        self.pb_num6.setFixedSize(150, 60) # size
        self.pb_num6.clicked.connect(self.show_dialog_num6)     
      #   layout.addWidget(self.le_num6)       
        self.pb_num6.move(290, 200)        
        layout.addWidget(self.pb_num6)
        self.setLayout(layout)
        #speckleRange
        self.le_num7 = QLineEdit()
        self.le_num7.setFixedSize(50, 20) # size                        
        self.pb_num7 = QPushButton('speckleRange')
        self.pb_num7.setFixedSize(150, 60) # size
        self.pb_num7.clicked.connect(self.show_dialog_num7)     
     #    layout.addWidget(self.le_num7)       
        self.pb_num7.move(390, 200)        
        layout.addWidget(self.pb_num7)
        self.setLayout(layout)

    def clickMethod(self):
         print ("ok1")
         camera1 = cv2.VideoCapture(1)
         camera2 = cv2.VideoCapture(2)

         while 1:                    
          stereo = cv2.StereoSGBM_create(minDisparity, numDisparities, blockSize, disp12MaxDiff,
                                         uniquenessRatio, speckleWindowSize, speckleRange)
          (grabbed, frame1) = camera1.read()
          (grabbed, frame2) = camera2.read()
          disp = stereo.compute(frame1, frame2).astype(np.float32)
          cv2.imshow("disparity", disp)
          cv2.waitKey(1)        
# прогать тута
         thread=threading.Thread(target=self.clickMethod, args=())
         thread.start()    
# input data
    def show_dialog_num1(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'minDisparity:')
        global minDisparity
        minDisparity = value
        print ("minDisparity", minDisparity)
        
    def show_dialog_num2(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'numDisparities:')
        global numDisparities
        numDisparities = value
        print ("numDisparities", numDisparities)
        
    def show_dialog_num3(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'blockSize:')
        global blockSize
        blockSize = value
        print ("blockSize", blockSize)        
    def show_dialog_num4(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'disp12MaxDiff:')
        global disp12MaxDiff
        disp12MaxDiff = value
        print ("disp12MaxDiff", disp12MaxDiff)

    def show_dialog_num5(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'uniquenessRatio:')
        global uniquenessRatio
        uniquenessRatio = value
        print ("uniquenessRatio", uniquenessRatio)

    def show_dialog_num6(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'speckleWindowSize:')
        global speckleWindowSize
        speckleWindowSize = value
        print ("speckleWindowSize", speckleWindowSize)

    def show_dialog_num7(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'speckleRange:')
        global speckleRange
        speckleRange = value
        print ("speckleWindowSize", speckleRange)
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    seconWin = second_window()    
    sys.exit(app.exec_())

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
from tqdm import tqdm
from PyQt5 import QtGui, QtCore

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

#calibration proccess
img_1 =  cv2.imread("C:/Users/rakhmatulin/Desktop/jre_new/2021/4.Stereo_vision/programme/left/img0.png",0)
img_2 = cv2.imread("C:/Users/rakhmatulin/Desktop/jre_new/2021/4.Stereo_vision/programme/right/img0.png",0)

h,w = img_2.shape[:2]
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

pathR= "C:/Users/rakhmatulin/Desktop/jre_new/2021/4.Stereo_vision/programme/left/"
pathL = "C:/Users/rakhmatulin/Desktop/jre_new/2021/4.Stereo_vision/programme/right/"
obj_pts = []
img_ptsL = []
img_ptsR = []

for i in tqdm(range(0,20)):      
 imgR = cv2.imread(pathR+"img%d.png"%i)
 imgL_gray = cv2.imread(pathL+"img%d.png"%i,0)
 imgR_gray = cv2.imread(pathR+"img%d.png"%i,0)
 imgL = cv2.imread(pathL+"img%d.png"%i)
 outputL = imgL.copy()
 outputR = imgR.copy()
 retR, cornersR =  cv2.findChessboardCorners(outputR,(9,6),None)
 retL, cornersL = cv2.findChessboardCorners(outputL,(9,6),None)
 if retR and retL:
  obj_pts.append(objp)
  cv2.cornerSubPix(imgR_gray,cornersR,(11,11),(-1,-1),criteria)
  cv2.cornerSubPix(imgL_gray,cornersL,(11,11),(-1,-1),criteria)
  cv2.drawChessboardCorners(outputR,(9,6),cornersR,retR)
  cv2.drawChessboardCorners(outputL,(9,6),cornersL,retL)
#  cv2.imshow('cornersR',outputR)
#  cv2.imshow('cornersL',outputL)
		#cv2.waitKey(0)
  img_ptsL.append(cornersL)
  img_ptsR.append(cornersR)
  
# Calibrating left camera

global mapxL
global mapyL
global mtxL
global new_mtxL


#global w 
#global h
global mapxR
global mapxR
global mapyR
global mtxR
global distR
global new_mtxR

retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts,img_ptsL,imgL_gray.shape[::-1],None,None) 
hL,wL= imgL_gray.shape[:2]
new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))

roi_x, roi_y, roi_w, roi_h = roiL
#cropped_frame = undistorted_frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]


# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_gray.shape[::-1],None,None)
KR=mtxR
hR,wR= imgR_gray.shape[:2]

new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))
print ("ok",retR, mtxR, distR, rvecsR, tvecsR )


#Get optimal camera matrix for better undistortion 
#new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(K,dist,(w,h),1,(w,h))

#Undistort images
img_1_undistorted = cv2.undistort(img_1, mtxL, distL, None, new_mtxL)
img_2_undistorted = cv2.undistort(img_2, mtxR, distR, None, new_mtxR)
#Downsample each image 3 times (because they're too big)


#2 ?????????????????? pqyt ?????? ???????????????? ????????????????????    
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
    print ("second_window")   
    def __init__ (self):
        print ("start")       
        QWidget.__init__(self)

        self.setMinimumSize(QSize(600, 500))    
        self.setWindowTitle("Stereo_vision") 
        self.figure = plt.figure(figsize=(0,2,),facecolor='y',  edgecolor='r') #  color only                     
        self.canvas = FigureCanvas(self.figure)
        self.figure.subplots_adjust(0.2, 0.4, 0.8, 1)      
        pybutton = QPushButton('graph', self)        

        pybutton_data = QPushButton('print_settings', self) 

        global axis_x
        axis_x=0
        pybutton.clicked.connect(self.clickMethod)
        pybutton.move(50, 10)
        pybutton.resize(100,32)        
        layout = QVBoxLayout()
        layout.setContentsMargins(50,100,0,11) # move background
        layout.setGeometry(QRect(0, 0, 80, 68))# nothing  
        layout.addWidget(self.canvas)        

        pybutton_data.clicked.connect(self.settings)
        pybutton_data.move(50, 50)
        pybutton_data.resize(100,32)        
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
        #layout.addWidget(self.le_num6)       
        self.pb_num6.move(290, 200)        
        layout.addWidget(self.pb_num6)
        self.setLayout(layout)
        #speckleRange
        self.le_num7 = QLineEdit()
        self.le_num7.setFixedSize(50, 20) # size                        
        self.pb_num7 = QPushButton('speckleRange')
        self.pb_num7.setFixedSize(150, 60) # size
        self.pb_num7.clicked.connect(self.show_dialog_num7)     
        #layout.addWidget(self.le_num7)       
        self.pb_num7.move(390, 200)        
        layout.addWidget(self.pb_num7)
        self.setLayout(layout)
    def settings(self):
         print ("minDisparity", minDisparity)    
         print ("numDisparities",numDisparities)
         print ("blockSize", blockSize)
         print ("disp12MaxDiff", disp12MaxDiff)
         print ("uniquenessRatio", uniquenessRatio)
         print ("speckleWindowSize", speckleWindowSize)
         print ("speckleWindowSize", speckleRange)    
    def clickMethod(self):              
         camera1 = cv2.VideoCapture(1)
         camera2 = cv2.VideoCapture(2)         
         win_size = 5
         dim =(200,200)         
         while 1:                   
          #stereo = cv2.StereoSGBM_create(minDisparity, numDisparities, blockSize, disp12MaxDiff,
          #                           uniquenessRatio, speckleWindowSize, speckleRange)
          stereo = cv2.StereoSGBM_create(minDisparity, numDisparities, blockSize, uniquenessRatio, speckleWindowSize, speckleRange, disp12MaxDiff)#,
#                                         P1 = 8*3*win_size**2, P2 =32*3*win_size**2)
          (grabbed, frame1) = camera1.read()
          (grabbed, frame2) = camera2.read()
          img_1_undistorted = cv2.undistort(frame1, mtxL, distL, None, new_mtxL)  #frame1
          img_2_undistorted = cv2.undistort(frame2, mtxR, distR, None, new_mtxR)   #frame2 
          
         # disp = stereo.compute(frame1, frame2).astype(np.float32)
          mapxL,mapyL = cv2.initUndistortRectifyMap(mtxL,distL,None,new_mtxL,(w,h),5)
          mapxR,mapyR = cv2.initUndistortRectifyMap(mtxR,distR,None,new_mtxR,(w,h),5)
          img_1_undistorted = cv2.remap(img_1_undistorted,mapxL,mapyL,cv2.INTER_LINEAR)
          img_2_undistorted = cv2.remap(img_2_undistorted,mapxR,mapyR,cv2.INTER_LINEAR)

          img_1_undistorted = cv2.undistort(frame1, mtxL, distL, None, new_mtxL)
          img_2_undistorted = cv2.undistort(frame2, mtxR, distR, None, new_mtxR)

          disp = stereo.compute(img_1_undistorted, img_2_undistorted)
          disp = cv2.resize(disp, dim)

          disp = cv2.erode(disp, None, iterations=1)
          disp = cv2.dilate(disp, None, iterations=1)

          #ROI
          disp_roi=disp[0:50,0:50]

          #calculate dominant color
          disp_roi = np.average(disp_roi, axis=0)
          disp_roi = np.average(disp_roi, axis=0)
          disp_avr = np.array(disp_roi, dtype=np.uint8)          

          print("disp_avr", disp_avr)        

          cv2.imshow("disparity", disp)





          
          #plt.imshow(disp,'gray')
          #plt.ion()
          #plt.pause(.0001)
          #plt.show()
       #   cv2.waitKey(1)
          x1=000
          y1=100
          x2=900
          y2=100
          line_thickness = 2
          cv2.line(frame1, (x1, y1+50), (x2, y2+50), (10, 155, 10), thickness=line_thickness)
          cv2.line(frame1, (x1, y1-50), (x2, y2-50), (90, 55, 60), thickness=line_thickness)
          cv2.line(frame1, (x1, y1+150), (x2, y2+150), (90, 55, 60), thickness=line_thickness)
          cv2.line(frame1, (x1, y1), (x2, y2), (60, 70, 100), thickness=line_thickness)

          cv2.line(frame1, (x1, y1+450), (x2, y2+450), (10, 155, 10), thickness=line_thickness)
          cv2.line(frame1, (x1, y1+300), (x2, y2+300), (5, 15, 60), thickness=line_thickness)
          cv2.line(frame1, (x1, y1+100), (x2, y2+100), (67, 45, 60), thickness=line_thickness)
          cv2.line(frame1, (x1, y1+200), (x2, y2+200), (167, 145, 160), thickness=line_thickness)
          cv2.line(frame1, (x1, y1+250), (x2, y2+250), (160, 170, 10), thickness=line_thickness)

          cv2.line(frame2, (x1, y1+50), (x2, y2+50), (10, 155, 10), thickness=line_thickness)
          cv2.line(frame2, (x1, y1-50), (x2, y2-50), (90, 55, 60), thickness=line_thickness)
          cv2.line(frame2, (x1, y1+150), (x2, y2+150), (90, 55, 60), thickness=line_thickness)
          cv2.line(frame2, (x1, y1), (x2, y2), (60, 70, 100), thickness=line_thickness)

          cv2.line(frame2, (x1, y1+450), (x2, y2+450), (10, 155, 10), thickness=line_thickness)
          cv2.line(frame2, (x1, y1+300), (x2, y2+300), (5, 15, 60), thickness=line_thickness)
          cv2.line(frame2, (x1, y1+100), (x2, y2+100), (67, 45, 60), thickness=line_thickness)
          cv2.line(frame2, (x1, y1+200), (x2, y2+200), (167, 145, 160), thickness=line_thickness)
          cv2.line(frame2, (x1, y1+250), (x2, y2+250), (160, 170, 10), thickness=line_thickness)


          frame1 = cv2.resize(frame1, dim)
          frame2 = cv2.resize(frame2, dim)
          both = np.concatenate((frame1, frame2), axis=1)
          cv2.imshow('frame diff ',both)      

          if cv2.waitKey(1) & 0xFF == ord('q'):
           break
          
# ?????????????? ????????
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
        if value in [32,64,128,256,512,1024,2048]:
         numDisparities = value
         print ("numDisparities", numDisparities)
        else:
         print ("not correct value, should be divided to 32")         
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

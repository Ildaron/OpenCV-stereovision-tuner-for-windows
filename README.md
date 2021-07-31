Rakhmatulin, I.; Pomazov, E. Low-Cost Stereovision System (Disparity Map) For Few Dollars. Preprints 2021, 2021040282 (doi: 10.20944/preprints202104.0282.v1).
https://www.preprints.org/manuscript/202104.0282/v1


OpenCV stereovision tuner for windows   

# OpenCV stereovision tuner for windows
### 1.GUI without calibration process - "GUI_Real_time_without_calibration.py" 
Check number of your cameras:  
camera1 = cv2.VideoCapture(1)  
and  
camera2 = cv2.VideoCapture(2)  
  
### 2. GUI withcalibration process 
In the first need prepare  image with a chessboard for calibration process and put these images in the folders "left" and "rights" - please change the code in the file, write your path for folders. Make images from 2 cameras by code - "1.Make_images.py"

After that run the code - "GUI_Real_time.py"

At the expense of computer vision, the position of the object in the X, Y plane is determined - based on which its ROI area is taken. Then we use stereo vision to compile a depth map and for a given ROI with the NumPy library tool - np.average we calculated the average value for the pixels of this area, which will allow us to calculate the distance to the object. 


#### Example of chessboard process
![alt tag](https://github.com/Ildaron/OpenCV-stereovision-tuner-for-windows/blob/master/pic.1.bmp "Example of result for Fast Fourier  transform")​


#### Example of GUI
![alt tag](https://github.com/Ildaron/OpenCV-stereovision-tuner-for-windows/blob/master/pic.2.bmp "Example of result for Fast Fourier  transform")​


#### Device, but can be used any cameras 
![alt tag](https://github.com/Ildaron/OpenCV-stereovision-tuner-for-windows/blob/master/pic.3.bmp "Example of result for Fast Fourier  transform")​





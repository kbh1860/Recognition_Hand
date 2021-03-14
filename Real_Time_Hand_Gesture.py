import cv2
import numpy as np
import sys
from pwn import *

cap = cv2.VideoCapture(0)

if cap.isOpened() == False:
    print("Cant Open The Camera")
    sys.exit()

lower = np.array([0, 48, 80], dtype="uint8") # Skin Range 1
upper = np.array([20, 255, 255], dtype="uint8") #Skin Range 2
    
while True:
    ret, frame = cap.read()

    if ret == False:
        print("Cant Load The Camera")
        break
    
    hsvim = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convert The Color -> HSV

    skinRecognitionHSV = cv2.inRange(hsvim, lower, upper) # Change The Pixel 0 & 1

    kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (3, 3)) # Make The Morphology Kernel
    skinRecognitionHSV = cv2.dilate(skinRecognitionHSV, kernel, iterations=1) # dilation to margin of hand

    skinRecognitionHSV = cv2.GaussianBlur(skinRecognitionHSV, (3, 3), 0) #Blurring

    contours = cv2.findContours(skinRecognitionHSV, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Find Contours
    

    log.info("Contours Type : " + str(type(contours)))

    cv2.drawContours(frame, [contours], -1, (0, 255, 0), 3)
    # cv2.imshow("Frame", frame)
    # cv2.imshow("HSV", hsvim)
    cv2.imshow("frame", frame)
    cv2.imshow("Hand", skinRecognitionHSV)
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
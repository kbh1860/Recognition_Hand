import cv2
import numpy as np
import argparse
import math
import imutils
import sys
import copy

from pwn import *

ap = argparse.ArgumentParser()

ap.add_argument("--bounding-box", required=True, help="Where Do You Want ROI Area?")

cap = cv2.VideoCapture(0)

mouse_is_pressing = False
start_x, end_x, start_y, end_y = 0, 0, 0, 0

step = 0
temp = 0

lower =  np.array([0, 48, 80], dtype="uint8")
upper = np.array([20, 255, 255], dtype="uint8")

def swap(v1, v2):
    global temp
    temp = v1
    v1 = v2
    v2 = temp

def Mouse_Callback(event, x, y, flags, param):
    global step , start_x, end_x, start_y, end_y, mouse_is_pressing

    if event == cv2.EVENT_LBUTTONDOWN:
        step = 1
        
        mouse_is_pressing = True;
        start_x = x
        start_y = y
    
    elif event == cv2.EVENT_MOUSEMOVE:

        if mouse_is_pressing:
            end_x = x
            end_y = y
            step = 2
    
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_is_pressing = False

        end_x = x
        end_y = y

        step = 3

if cap.isOpened() == False:
    print("Cant Open The Camera")
    sys.exit()

if cap.isOpened():
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cv2.namedWindow("Original")
cv2.setMouseCallback("Original", Mouse_Callback)

print("[INFO] Loading The Camera...")

while True:
    ret, frame = cap.read()
    # ROI = cap.read()

    frame = cv2.flip(frame, 1)

    if ret == False:
        print("Cant Load The Camera")
        break

    # cv2.rectangle(frame, (sys_Parameter[0], sys_Parameter[1]), (sys_Parameter[2] , sys_Parameter[3]), (0, 0, 255), 1)

    if step == 1:
        cv2.circle(frame, (start_x, start_y), 10, (0, 255, 0), -1)
    
    elif step == 2:
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 3)

    elif step == 3:
        if start_x > start_y:
            swap(start_x, end_x)
            swap(start_y, end_y)

        Middle1 = [end_x, start_y]
        Middle2 = [start_x, end_y]

        Cropped_Width = int(math.floor(int(start_x) - int(Middle1[0])))
        Cropped_Height = int(math.floor(int(start_y) - int(Middle2[1])))

        print(end_y != start_y + Cropped_Height)
        print(end_x != start_x + Cropped_Width)

        ROI = frame[start_y: end_y, start_x: end_x]
        # ROI = cv2.cvtColor(ROI, cv2.COLOR_RGB2BGR)
        
        roi_copy = copy.deepcopy(ROI)

        hsv = cv2.cvtColor(roi_copy, cv2.COLOR_BGR2HSV)

        skinRecognitionHSV = cv2.inRange(hsv, lower, upper)
        
        blurred = cv2.GaussianBlur(skinRecognitionHSV, (5, 5), 0)

        contours, hierarchy = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        length = len(contours)
        print(contours)

        if length > 2:
            cv2.drawContours(roi_copy, contours, -1, (255, 255, 0), 2)
        
        else:
            print("Re-Select The ROI Area")

        frame[start_y: end_y, start_x: end_x] = roi_copy
        # cv2.imshow("ROI", ROI)
        cv2.imshow("HSV", skinRecognitionHSV)
        # cv2.imshow("blur", blurred)

        # cv2.imshow("DrawContours", Original_Frame_Contours)
        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 3)

    # log.info("ROI_Position (Start_x): " + str(start_x))
    # log.info("ROI_Position (Start_y): " + str(start_y))
    # log.info("ROI_Position (End_x): " + str(end_x))
    # log.info("ROI_Position (End_y): " + str(end_y))

    # ROI = frame[int(start_y) : int(end_y) , int(start_x) : int(end_y)]    
    cv2.imshow("Original", frame)
    # cv2.imshow("ROI Cropped", ROI)

    key = cv2.waitKey(1)

    if key == 27:
        break
    

cv2.destroyAllWindows()
cap.release()

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

lower =  np.array([0, 48, 80], dtype="uint8")
upper = np.array([20, 255, 255], dtype="uint8")

while (cap.isOpened()):
    ret, frame = cap.read()

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    skin = cv2.inRange(hsv, lower, upper)
    
    cv2.imshow("hsv", hsv)
    cv2.imshow("frame", skin)

    key = cv2.waitKey(1)

    if key == 27:
        break

cv2.destroyAllWindows()
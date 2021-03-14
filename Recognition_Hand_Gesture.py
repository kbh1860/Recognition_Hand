import cv2
import numpy as np 
from pwn import *

img_path = "data/palm_image.jpeg"
img = cv2.imread(img_path)

hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 48, 80], dtype="uint8")
upper = np.array([20, 255, 255], dtype="uint8")

log.info("Lower Case : " + str(lower))
log.info("Upper Case : " + str(upper))

skinRecognitionHSV = cv2.inRange(hsvim, lower, upper)
blurred = cv2.blur(skinRecognitionHSV, (2, 2))

ret, thresh = cv2.threshold(blurred, 0, 255 , cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

contours = max(contours, key=lambda x: cv2.contourArea(x))

Original_Image_Contours = img.copy()

cv2.drawContours(Original_Image_Contours, [contours], -1, (255, 255, 0), 2)

# merged = np.hstack(((img, skinRecognitionHSV, Original_Image_Contours)))

Original_Image_Draw_Contours = Original_Image_Contours.copy()

hull = cv2.convexHull(contours)
cv2.drawContours(Original_Image_Draw_Contours, [hull], -1, (0, 255, 255), 2)

cv2.imshow("Original", img)
cv2.imshow("HSV_Image", skinRecognitionHSV)
cv2.imshow("Contours_Image", Original_Image_Contours)
cv2.imshow("Draw_Line", Original_Image_Draw_Contours)
# cv2.imshow("merged", merged)

hull = cv2.convexHull(contours, returnPoints=False)
defects = cv2.convexityDefects(contours, hull)

log.info("Defects : " + str(defects))
log.info("Pi Value: " + str(np.pi))

Original_Image_Point_Contours = Original_Image_Draw_Contours.copy()

if defects is not None:
    cnt = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i][0]

        start = tuple(contours[s][0])
        end = tuple(contours[e][0])
        far = tuple(contours[f][0])

        a = np.sqrt( (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = np.sqrt( (far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = np.sqrt( (end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

        angle = np.arccos( (b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

        if angle <= np.pi / 2:
            cnt += 1
            cv2.circle(Original_Image_Point_Contours, far, 4, [0, 0, 255], -1)
        
    if cnt > 0:
        cnt = cnt + 1
    
    cv2.putText(Original_Image_Point_Contours, str(cnt), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow("Point_Contours", Original_Image_Point_Contours)

cv2.waitKey(0)
cv2.destroyAllWindows()
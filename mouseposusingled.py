"""
@author: HIMANSHU
"""

import cv2
import numpy as np
import pyautogui
def nothing(x):
    pass

cap = cv2.VideoCapture(1)
while True:
    _, im = cap.read()
    im = cv2.resize(im, (1920, 1080))
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    #lower_red = np.array([0,34, 250])       #0,0,255
    #upper_red = np.array([18, 220, 255])       #108,10,255
    #lower_red = np.array([170,50,50])
    #upper_red = np.array([180,255,255])
    #lower_red = np.array([0,0,255])
    #upper_red = np.array([108,10,255])
    
    
    ### Improved Red Contor
    
    
    lower_red = np.array([160,100,50])
    upper_red = np.array([180,255,255])
    
    
    lower_white = np.array([159, 50, 70])#28,0,255
    upper_white = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask1 = cv2.inRange(hsv, lower_white, upper_white)
    result=cv2.bitwise_not(mask1)
    result = cv2.bitwise_and(result, result, mask=mask)
    
    
    ### Improved Red contor finish
    
    ###
        
    #lower_white = np.array([0,0,0])
    #upper_white = np.array([0,0,255])
    
    #mask1= cv2.inRange(hsv , lower_white , upper_white)
    ######
    
    
    #mask = cv2.inRange(hsv, lower_red, upper_red)
    
    #result = cv2.bitwise_and(im, im, mask=mask)
    #-cv2.bitwise_not(im,im,mask=mask1)
    
    ######
    #result= cv2.bitwise_not(im,im,mask1) ####EEEEEEEEE
    
    #######
    
    contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    #contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours)>0:
        contours=contours[0][0]
        pyautogui.moveTo(contours[0][0],contours[0][1])
    cv2.imshow("result", result)    
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()
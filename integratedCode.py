import cv2
import numpy as np
import pyautogui
class cnt:
   cnt=4
def mouse_drawing(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
       cnt.cnt-=1
       print("Remanng Clcks - ",cnt.cnt)
       circles.append((x, y))
cap = cv2.VideoCapture(1)
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)
circles = []
x1=0
y1=0
var =5
while len(circles)!=4:
   _, frame = cap.read()
   for center_position in circles:
       cv2.circle(frame, center_position, 5, (0, 0, 255), -1)
   cv2.imshow("Frame", frame)
   key = cv2.waitKey(1)
   if key == 27:
       exit(0)
print("goto",circles)
while True:
   _, frame = cap.read()
   pts1 = np.float32([list(circles[0]),list(circles[1]),list(circles[2]),list(circles[3])])
   pts2 = np.float32([[0,0],[1920, 0],[0, 1080],[1920, 1080]])
   matrix = cv2.getPerspectiveTransform(pts1,pts2)
   result = cv2.warpPerspective(frame, matrix, (1920, 1080))
   #cv2.imshow("Perspective transformation", result)
   m = cv2.resize(result, (1920, 1080))
   hsv = cv2.cvtColor(m, cv2.COLOR_BGR2HSV)
   lower_blue = np.array([0,34,250])#28,0,255
   upper_blue = np.array([18,220,255])#37,161,255
   #lower_blue = np.array([129,115,165])#28,0,255
   #upper_blue = np.array([179,255,255])#37,161,255
   mask = cv2.inRange(hsv, lower_blue, upper_blue)
   result1 = cv2.bitwise_and(m, m, mask=mask)
   #contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
   contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
   cv2.imshow("Perspective transformation", result1)
   if len(contours)>0:
       contours=contours[0][0]
       #print(contours[0][0],contours[0][1])   
       #pyautogui.click(contours[0][0],contours[0][1])
       #print(contours[len(contours)-1])
       var=1
       pyautogui.moveTo(x=contours[0][0],y=contours[0][1])
       #pyautogui.click(button='left',x=contours[0][0],y=contours[0][1])
       #pyautogui.mouseDown(button='left',x=contours[0][0],y=contours[0][1]) 
       x1=contours[0][0]
       y1=contours[0][1]
   else:
       if var==1:
           pyautogui.mouseUp(button='left', x=x1,y=y1)
           var=2
   #cv2.imshow("result", result1)    
   key = cv2.waitKey(1)
   if key == 27:
       break
cap.release()
cv2.destroyAllWindows()
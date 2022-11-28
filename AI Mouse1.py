import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
# import HandTrack as ht
import pyautogui as autopy
# import autopy
import time
autopy.FAILSAFE = False
wCam, hCam = 640, 480
frameR = 100 #frame reduction
smooth = 3
plocX, plocY = 0,0
clocX, clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = HandDetector( maxHands=1)
wScr, hScr = autopy.size()
print("Width = ",wScr," Height",hScr)
#print(wScr,hScr)

# def convertCord(fingerCord,oldSize,targetSize):
#     #one finger coordinate (x,y) from camera
#     fingerX = fingerCord[0]
#     fingerY = fingerCord[1]
#
#     # camera size 600 x 480
#     oldW = oldSize[0]
#     oldH = oldSize[1]
#
#     # screen size auto size
#     newW = targetSize[0]
#     newH = targetSize[1]
#
#     # calculate how much ratio to be multiples to scale the finger co-ordinates
#     x_scale = newW/oldW
#     y_scale = newH/oldH
#
#     # finger new coordinates according to monitor screen after scaling
#     newX = int(x_scale*fingerX)
#     newY = int(y_scale*fingerY)
#
#     print(newX,newY)
#     return [newX,newY]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    if hands: # hands is an array in which there are multiple hand if we show multiple hands
        # Hand 1
        hand1 = hands[0] # we are taking the first hand
        lmList = hand1["lmList"]  # List of 21 Landmark points
        # print(lmList)
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        handType1 = hand1["type"]  # Handtype Left or Right
        #print(bbox1)


        if(len(lmList)!=0):
            print("Position of Index Finger = ",lmList[8])
            # print(lmList[8][1:])
            x1,y1 = lmList[8][0],lmList[8][1]
            x2,y2 = lmList[12][0],lmList[8][1]

            #rint(x1,y1,x2,y2)

        # Stwp 3: which finger is up
        fingers1 = detector.fingersUp(hand1) # return array of 5 fingers as bool [1 0 0 1 0] 1 - up 0 - down
        #print(fingers1)
        cv2.rectangle(img,(frameR, frameR),(wCam-frameR, hCam-frameR),(255,0,255),2)

        #step 4: Only index finger: Moving mode
        if fingers1[1]==1 and fingers1[2] == 0:

        #5. Convert Coordinates
            #cv2.rectangle(img, (frame))
            print("Finger Coordinates = (",x1,",",y1,")")
            ## x3,y3 are screen coordinates from big rectangle coordinates
            x3 = np.interp(x1,(frameR,wCam-frameR),(0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR),(0, hScr))
            print("Mouse Coordinates = (",x3,",",y3,")")
            if(x3 <= 0):
                x3 = 0
            if(x3 >= wScr):
                x3 = wScr
            if(y3 <= 0):
                y3 = 0
            if(y3 >= hScr):
                y3 = hScr

        #6. Smooth Values
            clocX= plocX + (x3 - plocX)/smooth
            clocY= plocY + (y3 - plocY)/smooth

            print("clocX = ",clocX," ,clocY = ",clocY)

            if(clocX <= 0):
            	clocX = 0
            if(clocY <= 0):
            	clocY = 0
            if(clocX >= wScr):
            	clocX = wScr
            if(clocY >= hScr):
            	clocY = hScr
        #7. move mouse

            
            autopy.moveTo(x3,y3)

            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED) # x1,y1 are index finger coordinates on big rectangle

            plocX,plocY = clocX, clocY

        #8.Both index ad middle fingers are up: left clicking mode
        if fingers1[1] == 1 and fingers1[2] == 1:
            print("YES")
        #9. Find distance between fingers
            length,lineinfo,img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
            print("Distance between Two Fingers = ",length)
        #10.Click mouse if distance short
            if length <30:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.click(button = "left")

     #11. frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == 27:
        break

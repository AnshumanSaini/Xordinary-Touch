import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
# import HandTrack as ht
import autopy
import time

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
wScr, hScr = autopy.screen.size()
#print(wScr,hScr)

def convertCord(fingerCord,oldSize,targetSize):
    fingerX = fingerCord[0]
    fingerY = fingerCord[1]

    oldW = oldSize[0]
    oldH = oldSize[1]

    newW = targetSize[0]
    newH = targetSize[1]

    x_scale = newW/oldW
    y_scale = newH/oldH

    newX = int(x_scale*fingerX)
    newY = int(y_scale*fingerY)
    print(newX,newY)
    return [newX,newY]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList = hand1["lmList"]  # List of 21 Landmark points
        # print(lmList)
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right
        #print(bbox1)


        if(len(lmList)!=0):
            print(lmList[8])
            print(lmList[8][1:])
            x1,y1 = lmList[8][0],lmList[8][1]
            x2,y2 = lmList[12][0],lmList[8][1]

            #rint(x1,y1,x2,y2)

        # Stwp 3: which finger is up
        fingers1 = detector.fingersUp(hand1)
        # print(fingers1)
        cv2.rectangle(img,(frameR, frameR),(wCam-frameR, hCam-frameR),(255,0,255),2)

        #step 4: Only index finger: Moving mode
        if fingers1[1]==1 and fingers1[2] == 0:

        #5. Convert Coordinates
            #cv2.rectangle(img, (frame))
            x3 = np.interp(x1,(frameR,wCam-frameR),(0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            # x3,y3 = convertCord([x1,y1],[480,220],[wScr,hScr])
            if(x3 <= 0 or x3 >= wScr):
                x3 = 0
            if(y3 <= 0 or y3 >= hScr):
                y3 = 0
            # print(x1,y1)
            # print(x3,y3)
        #6. Smooth Values
            clocX= plocX + (x3 - plocX)/smooth
            clocY= plocY + (y3 - plocY)/smooth
        #7. move mouse
            autopy.mouse.move(clocX,clocY)
            cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            plocX,plocY = clocX, clocY

        #8.Both index ad middle fingers are up: clicking mode
        if fingers1[1] == 1 and fingers1[2] == 1:
            print("YES")
        #9. Find distance between fingers
            length,lineinfo,img = detector.findDistance(lmList[8][0:2], lmList[12][0:2], img)
            print(length)
        #10.Click mouse if distance short
            if length <30:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()





     #11. frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
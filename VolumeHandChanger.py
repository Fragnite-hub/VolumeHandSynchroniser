import cmath

import cv2 as cv
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackingModule as htm

wCam, hCam = 640, 480
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4,hCam)
pTime = 0
detector = htm.handDetector()
volBar = 400
volPer = 0
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minVol = volume[0]
maxVol = volume[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if(len(lmList) != 0):
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x2+x1)//2, (y2+y1)//2



        cv.circle(img, (x1, y1), 12, (0,0,255), cv.FILLED)
        cv.circle(img, (x2, y2), 12, (0, 0, 255), cv.FILLED)
        cv.line(img, (x1, y1), (x2,y2), (255,0,255),3, cv.FILLED)
        cv.circle(img, (cx, cy), 12, (0,0,255), cv.FILLED)

        length = int(math.hypot(x2-x1, y2-y1))
        xn1, yn1 = lmList[5][1], lmList[5][2]
        xn2, yn2 = lmList[17][1], lmList[17][2]
        lenCalc = int(math.hypot(xn2-xn1, yn2-yn1))
        a, b, c = coff
        distCM = a * lenCalc**2 + b*lenCalc + c
        print(distCM)
        cv.putText(img, f'Distance : {int(distCM)}cm', (750, 80), cv.FONT_HERSHEY_PLAIN, 3,
                   (250, 0, 0), 3)
        if  distCM < 30:
            cv.putText(img, f'Note : Too Close.', (900, 480), cv.FONT_HERSHEY_PLAIN, 2,
                       (0, 0, 255), 3)
        if  distCM > 60:
            cv.putText(img, f'Note : Too Far.', (900, 480), cv.FONT_HERSHEY_PLAIN, 2,
                       (0, 0, 255), 3)
        if length < 47:
            cv.circle(img, (cx, cy), 12, (0, 255, 0), cv.FILLED)

        #Hand Range 50 to 300
        #Volume Range -65 to 0

        vol = np.interp(length, [50, 300], [minVol,maxVol])
        volBar = np.interp(length, [50,250], [430, 180])
        volPer = np.interp(length, [50,250], [0, 100])

        volume.GetMasterVolumeLevel(vol, None)
        cv.rectangle(img, (50, 180), (85, 430), (250, 0, 0), 3)
        cv.rectangle(img, (50, int(volBar)), (85, 430), (250, 0, 0), cv.FILLED)
        cv.putText(img, f'{int(volPer)}%', (25, 480), cv.FONT_HERSHEY_PLAIN, 3,
                   (250, 0, 0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img,f'FPS :{int(fps)}', (40,60), cv.FONT_HERSHEY_PLAIN, 3,
               (0,255,0), 3)
    cv.imshow("Image", img)
    cv.waitKey(1)

import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

comment = "comment"
cap = cv2.VideoCapture(0)
detector = htm.handDetector(maxHands=1)
flag = True
hold_flag = False
length = 0
y = 100
x = 0
z = 0
font_size = 3
cx = 0
cy = 0

def step(size):
    if size < 2:
        return 2
    else:
        return size

while True:
    succes, img = cap.read()
    w,h,c = img.shape
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        length, img, xy_list = detector.findDistance(4, 8, img)
        cx = xy_list[6]
        cy = xy_list[7]
        z = xy_list[2]
    
    if (x+font_size*60 > cx and x-font_size*10 < cx) and (y+font_size*10 > cy and y-font_size*10 < cy):
        hold_flag = True
    else:
        hold_flag = False

    if length < 25 and len(lmList) != 0 and hold_flag:
        x = cx
        y = cy
        font_size = step(abs(z * 14))
        cv2.putText(img, comment, (x, y), cv2.FONT_HERSHEY_PLAIN, font_size, (255,200,220), 3)
    
    else:
        if flag:
            x = w + 100
            flag = False
        else:
            cv2.putText(img, comment, (x, y), cv2.FONT_HERSHEY_PLAIN, font_size, (255,255,255), 3)
            x -= 6
            if x < -300:
                flag = True

    cv2.imshow("image", img)
    cv2.waitKey(1)
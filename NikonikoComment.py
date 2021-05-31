import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
comment = "comment"
x = 0
flag = True
y = np.random.randint(20, 200)

while True:
    succes, img = cap.read()
    w,h,c = img.shape
    if flag:
        x = w + 100
        flag = False
    else:
        cv2.putText(img, comment, (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0))
        x -= 3
        if x < -200:
            flag = True

    cv2.imshow("image", img)
    cv2.waitKey(1)
import cv2
import mediapipe as mp
import time
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = 2
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms)
        return img
    
    def findPosition(self, img, handNo=0, draw=True):

        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand =  self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy, lm.z])
                if draw:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
        
        return self.lmList
    
    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1, z1= self.lmList[p1][1:]
        x2, y2, z2= self.lmList[p2][1:]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2

        length = math.hypot(x2-x1, y2-y1)

        return length, img, [x1, y1, z1, x2, y2, z2, cx, cy]
            





def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        succes, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()
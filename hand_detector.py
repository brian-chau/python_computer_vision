import mediapipe as mp
import time
import cv2 as camera

from constants import *

class hand_detector():
    def __init__(self, mode = False, max_hands = 2, detection_confidence = 0.5, track_confidence = 0.5):
        self.mode                 = mode
        self.max_hands            = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence     = track_confidence

        self.mpHands              = mp.solutions.hands
        self.hands                = self.mpHands.Hands(self.mode,self.max_hands, self.detection_confidence, self.track_confidence)
        self.mpDraw               = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB       = camera.cvtColor(img, camera.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h,w,c  = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    camera.circle(img, (cx, cy), 15, VIOLET, camera.FILLED)
        return lmList
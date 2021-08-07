import mediapipe as mp
import time
import cv2 as camera
import math

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

    def find_hands(self, img, draw=True):
        imgRGB       = camera.cvtColor(img, camera.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_positions(self, img, handNo=0, draw=True):
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

    def get_joint_position(self, positions, joint):
        return positions[joint][X_POSITION], positions[joint][Y_POSITION]

    def are_two_fingers_touching(self, positions, finger_tip_1, finger_tip_2):
        # Get the positions of the fingers I want to track
        tip_1_x, tip_1_y         = self.get_joint_position(positions, finger_tip_1)
        tip_2_x, tip_2_y         = self.get_joint_position(positions, finger_tip_2)
        dist_cent_x, dist_cent_y = (tip_1_x + tip_2_x) // 2, (tip_1_y + tip_2_y) // 2

        # Find the distance between the fingers
        length = math.hypot(tip_2_x - tip_1_x, tip_2_y - tip_1_y)
        if length < FINGER_TOUCH_THRESHOLD:
            return (True, dist_cent_x, dist_cent_y)
        return (False, 0, 0)

    def check_any_finger_tips_touching(self, camera, img, positions):
        tips = [
                (HAND_THUMB_TIP, HAND_INDEX_FINGER_TIP),
                (HAND_THUMB_TIP, HAND_MIDDLE_FINGER_TIP),
                (HAND_THUMB_TIP, HAND_RING_FINGER_TIP),
                (HAND_THUMB_TIP, HAND_PINKY_TIP)
               ]

        list_of_touching_fingers = [self.are_two_fingers_touching(positions, tip[0], tip[1]) for tip in tips]

        for pair in list_of_touching_fingers:
            is_touching, center_x, center_y = pair
            if is_touching:
                camera.circle(img, (center_x, center_y), 15, SILVER, camera.FILLED)

                # TODO: Check when fingers are held together, then do something
                # Highlight the finger tips
                # camera.circle(img, (tip_1_x, tip_1_y), 15, VIOLET, camera.FILLED)
                # camera.circle(img, (tip_2_x, tip_2_y), 15, VIOLET, camera.FILLED)
                # camera.circle(img, (dist_cent_x, dist_cent_y), 15, VIOLET, camera.FILLED)
                # camera.line(  img, (tip_1_x, tip_1_y), (tip_2_x, tip_2_y), VIOLET, 3)

    def check_hand_closed(self, camera, img, positions):
        joints = [(HAND_INDEX_FINGER_TIP,  HAND_INDEX_FINGER_PIP),
                  (HAND_MIDDLE_FINGER_TIP, HAND_MIDDLE_FINGER_PIP),
                  (HAND_RING_FINGER_TIP,   HAND_RING_FINGER_PIP),
                  (HAND_PINKY_TIP,         HAND_PINKY_PIP)
                 ]

        is_hand_closed = True
        for joint in joints:
            tip_x, tip_y = self.get_joint_position(positions, joint[0])
            pip_x, pip_y = self.get_joint_position(positions, joint[1])
            
            if tip_y < pip_y:
                is_hand_closed = False

        if is_hand_closed:
            pos_x, pos_y = self.get_joint_position(positions, HAND_THUMB_TIP)

            camera.circle(img, (pos_x, pos_y), 15, VIOLET, camera.FILLED)

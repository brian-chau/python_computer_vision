from hand import *
import cv2
from typing import Final
import math

def main():
    ####################################
    ## CONSTANTS                      ##
    ####################################

    ####################################
    ## Camera
    CAMERA_NUMBER:          Final = 0
    CAMERA_WIDTH_PROPERTY:  Final = 3
    CAMERA_HEIGHT_PROPERTY: Final = 4

    CAMERA_WIDTH:           Final = 640
    CAMERA_HEIGHT:          Final = 480


    ####################################
    ## Hand Points
    HAND_WRIST:             Final = 0

    HAND_THUMB_CMC:         Final = 1
    HAND_THUMB_MPC:         Final = 2
    HAND_THUMB_IP:          Final = 3
    HAND_THUMB_TIP:         Final = 4

    HAND_INDEX_FINGER_MCP:  Final = 5
    HAND_INDEX_FINGER_PIP:  Final = 6
    HAND_INDEX_FINGER_DIP:  Final = 7
    HAND_INDEX_FINGER_TIP:  Final = 8

    HAND_MIDDLE_FINGER_MCP: Final = 9
    HAND_MIDDLE_FINGER_PIP: Final = 10
    HAND_MIDDLE_FINGER_DIP: Final = 11
    HAND_MIDDLE_FINGER_TIP: Final = 12

    HAND_RING_FINGER_MCP:   Final = 13
    HAND_RING_FINGER_PIP:   Final = 14
    HAND_RING_FINGER_DIP:   Final = 15
    HAND_RING_FINGER_TIP:   Final = 16

    HAND_PINKY_MCP:         Final = 17
    HAND_PINKY_PIP:         Final = 18
    HAND_PINKY_DIP:         Final = 19
    HAND_PINKY_TIP:         Final = 20


    ####################################
    ## X- and Y- Coordinates
    X_POSITION:             Final = 1
    Y_POSITION:             Final = 2

    ####################################
    ## Colors
    RED:                    Final = (255,0,0)
    GREEN:                  Final = (0,255,0)
    BLUE:                   Final = (0,0,255)
    VIOLET:                 Final = (255,0,255)

    ####################################
    ## END CONSTANTS                  ##
    ####################################

    # Configure camera
    cap = cv2.VideoCapture(CAMERA_NUMBER)
    cap.set(CAMERA_WIDTH_PROPERTY,  CAMERA_WIDTH)
    cap.set(CAMERA_HEIGHT_PROPERTY, CAMERA_HEIGHT)

    pTime, cTime = 0, 0

    # Set up hand tracker
    detector = handDetector(detectionConfidence = 0.7)
    while True:
        success, img = cap.read()
        # Detect hand and draw hand tracker
        img    = detector.findHands(img)

        # Detect positions of hand and fetch collection of points as a list
        lmList = detector.findPosition(img, draw=False)

        if lmList != None and len(lmList) > 0:
            # Get the positions of the fingers I want to track
            thumb_tip_x, thumb_tip_y             = lmList[HAND_THUMB_TIP][X_POSITION],        lmList[HAND_THUMB_TIP][Y_POSITION]
            index_tip_x, index_tip_y             = lmList[HAND_INDEX_FINGER_TIP][X_POSITION], lmList[HAND_INDEX_FINGER_TIP][Y_POSITION]
            distance_center_x, distance_center_y = (thumb_tip_x + index_tip_x) // 2, (thumb_tip_y + index_tip_y) // 2 

            # Highlight the finger tips
            cv2.circle(img, (thumb_tip_x, thumb_tip_y), 15, VIOLET, cv2.FILLED)
            cv2.circle(img, (index_tip_x, index_tip_y), 15, VIOLET, cv2.FILLED)
            cv2.circle(img, (distance_center_x, distance_center_y), 15, VIOLET, cv2.FILLED)
            cv2.line(  img, (thumb_tip_x, thumb_tip_y), (index_tip_x, index_tip_y), VIOLET, 3)

            # Find the distance between the fingers
            length = math.hypot(index_tip_x - thumb_tip_x, index_tip_y - thumb_tip_y)
            if length < 30:
                cv2.circle(img, (distance_center_x, distance_center_y), 15, GREEN, cv2.FILLED)
        # Calculate and display the FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10,70), cv2.FONT_HERSHEY_PLAIN, 3, VIOLET, 3)

        # Draw the screen
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
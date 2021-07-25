import cv2 as camera
import math
import sys

from constants      import *
from hand_detector  import *
from hand_positions import *

def display_screen(img, cTime = 0, pTime = 0):
    # Calculate and display the FPS
    cTime = time.time()
    fps   = 1 / (cTime - pTime)
    pTime = cTime
    camera.putText(img, f'FPS: {int(fps)}', (10,70), camera.FONT_HERSHEY_PLAIN, 3, VIOLET, 3)

    # Draw the screen
    camera.imshow("Image", img)
    camera.waitKey(1)
    return cTime, pTime

def main():
    detection_confidence = 0.7
    display_camera       = True

    if len(sys.argv) > 2:
        detection_confidence = int(sys.argv[1])
    if len(sys.argv) == 3:
        display_camera       = bool(sys.argv[2])

    # Configure camera
    cap = camera.VideoCapture(CAMERA_NUMBER)
    cap.set(CAMERA_WIDTH_PROPERTY,  CAMERA_WIDTH)
    cap.set(CAMERA_HEIGHT_PROPERTY, CAMERA_HEIGHT)

    cTime = pTime = 0

    # Set up hand tracker
    detector = hand_detector(detection_confidence = detection_confidence)
    while True:
        success, img = cap.read()

        # Detect hand and draw hand tracker
        img          = detector.findHands(img, draw=False)

        # Detect positions of hand and fetch collection of points as a list
        positions    = detector.findPosition(img, draw=False)

        # Check if thumb is touching any finger tip
        if positions != None and len(positions) > 0:
            check_any_finger_tips_touching(camera, img, positions)
            check_hand_closed(camera, img, positions)

        if display_camera:
            cTime, pTime = display_screen(img, cTime, pTime)

if __name__ == '__main__':
    main()
# Generic Python imports
import math
import sys
import ctypes

# External libraries
import cv2 as camera                 # For capturing the camera feed
# from scipy.signal import lfilter     # For smoothing the x- and y-coordinates of the finger position

# Program-specific imports
from constants              import *
from hand_detector          import *

def clean_x_y_pos(previous_positions: list, pos: tuple):
    if len(pos) != 2:
        return None

    x,y = pos

    previous_positions.append(pos)

    aver_x, aver_y = 0,0
    for position in previous_positions:
        aver_x += position[0]
        aver_y += position[1]

    new_x = aver_x // len(previous_positions)
    new_y = aver_y // len(previous_positions)

    # If there are more than 5 data points, return just the latest 5
    if len(previous_positions) >= 5:
        return previous_positions[1:], new_x, new_y

    return previous_positions, new_x, new_y

def display_screen(img, cTime = 0, pTime = 0, display_fps=True):
    # Calculate and display the FPS
    if display_fps:
        cTime = time.time()
        fps   = 1 / (cTime - pTime)
        pTime = cTime
        camera.putText(img, f'FPS: {int(fps)}', (10,70), camera.FONT_HERSHEY_PLAIN, 3, VIOLET, 3)

    # Draw the screen
    camera.imshow("Image", img)
    camera.waitKey(1)
    return cTime, pTime

def handle_cmd_line_params(args):
    if len(args) not in [2,3]:
        print("Invalid number of arguments")
        sys.exit(0)

    if len(args) > 2:
        detection_confidence = float(args[1])
    if len(args) == 3:
        display_camera       = bool(args[2])

    return detection_confidence, display_camera

def main():
    # Specific to windows
    cursor, screen = [ctypes.windll.user32] * 2

    # Default values
    detection_confidence, display_camera = 0.5, True
    detection_confidence, display_camera = handle_cmd_line_params(sys.argv)

    # Configure camera
    cap = camera.VideoCapture(CAMERA_NUMBER)
    cap.set(CAMERA_WIDTH_PROPERTY,  CAMERA_WIDTH)
    cap.set(CAMERA_HEIGHT_PROPERTY, CAMERA_HEIGHT)

    # Monitor dimensions, so we know where to put the cursor
    screen_width, screen_height = screen.GetSystemMetrics(SCREEN_SIZE_WIDTH), screen.GetSystemMetrics(SCREEN_SIZE_HEIGHT)
    scale_x_pos,  scale_y_pos   = screen_width // CAMERA_WIDTH,               screen_height // CAMERA_HEIGHT

    # Time variables used for FPS display
    cTime = pTime = 0

    # Set up hand tracker
    detector           = hand_detector(detection_confidence = detection_confidence)
    previous_positions = []
    while True:
        success, img   = cap.read()

        # Rotate image horizontally, so the left side of the screen matches the left side of the camera
        img            = camera.flip(img, CAMERA_FLIP_HORIZONTAL)

        # Detect hand and draw hand tracker
        img            = detector.find_hands(img, draw=True)

        # Detect positions of hand and fetch collection of points as a list
        positions      = detector.find_positions(img, draw=False)

        # Check if thumb is touching any finger tip
        if positions != None and len(positions) > 0:
            # Track the pointer finger
            pos_x, pos_y = detector.get_joint_position(positions, HAND_INDEX_FINGER_TIP)

            # Average the positions to get rid of noise
            previous_positions, pos_x, pos_y = clean_x_y_pos(previous_positions, (pos_x, pos_y))

            # Display the smoothed cursor to the screen
            camera.circle(img, (pos_x, pos_y), 15, RED, camera.FILLED)

            cursor.SetCursorPos(pos_x * scale_x_pos, pos_y * scale_y_pos)

        if display_camera:
            cTime, pTime = display_screen(img, cTime, pTime, display_fps = True)

if __name__ == '__main__':
    main()
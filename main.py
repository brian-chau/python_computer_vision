from hand import *
import cv2
def main():
    pTime, cTime = 0, 0

    detector = handDetector()

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if lmList != None and len(lmList) > 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
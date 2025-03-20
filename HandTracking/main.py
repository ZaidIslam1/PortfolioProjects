import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm


def main():
    camera = cv2.VideoCapture(0)
    detector = htm.HandDetector(detectionConf=0.7)
    startTime = time.time()
    
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            break
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame,draw=False)
        if len(lmList)!=0:
            print(lmList)
        
        currentTime = time.time()
        fps = 1 / (currentTime - startTime)
        startTime = currentTime
        
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 150, 255), 3)
        cv2.imshow("Camera", frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

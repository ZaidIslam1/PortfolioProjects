import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import subprocess

W_CAM, H_CAM = 1280, 720  # Camera resolution

def run_osascript(command):
    process = subprocess.Popen(["osascript", "-e", command], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print("Error:", error)
    return output.strip()

def get_volume():
    return int(run_osascript('output volume of (get volume settings)'))

def set_volume(level):
    run_osascript(f'set volume output volume {level}')

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def main():
    startTime = 0
    currentTime = 0
    vol = 0
    volBarLength = 0  # This will be the dynamic length of the volume bar
    last_volume = None
    element_color = (255, 255, 255)
    
    cap = cv2.VideoCapture(0)
    cap.set(3, W_CAM), cap.set(4, H_CAM)
    
    detector = htm.HandDetector(maxHands=1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame, draw=False)
        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            
            length = calculate_distance(x1, y1, x2, y2)
            vol = np.interp(length, [50, 300], [0, 100])
            volBarLength = np.interp(vol, [0, 100], [0, 250])  # Adjust 250 to the desired length of the volume bar
            
            if last_volume is None or abs(vol - last_volume) > 5:
                set_volume(vol)
                last_volume = vol
                
            if vol == 0:
                element_color = (0, 0, 255)  # Red
            elif vol == 100:
                element_color = (0, 255, 0)  # Green
            else:
                element_color = (255, 255, 255)  # White
            
            # Use the determined color for all elements
            cv2.circle(frame, (x1, y1), 15, element_color, cv2.FILLED)
            cv2.circle(frame, (x2, y2), 15, element_color, cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), element_color, 3)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(frame, (cx, cy), 15, element_color, cv2.FILLED)
        
        # Draw the volume bar horizontally at the bottom right
        cv2.rectangle(frame, (W_CAM - 300, H_CAM - 50), (W_CAM - 50, H_CAM - 30), (255, 255, 255), 3)
        cv2.rectangle(frame, (W_CAM - 300, H_CAM - 50), (W_CAM - 300 + int(volBarLength), H_CAM - 30), (0, 255, 0), -1)
        cv2.putText(frame, f'Vol: {int(vol)}%', (W_CAM - 400, H_CAM - 35), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 255, 255), 2)
        
        currentTime = time.time()
        fps = 1 / (currentTime - startTime)
        startTime = currentTime
        cv2.putText(frame, "FPS: " + str(int(fps)), (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 150, 255), 3)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
  
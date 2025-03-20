import cv2
import mediapipe as mp
import time



class HandDetector():
    
    def __init__(self, mode=False,maxHands=2,detectionConf=0.5,trackConf=0.5):
        
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detectionConf
        self.trackConf = trackConf
        self.mpHands = mp.solutions.hands
        # self.hands = self.mpHands.Hands()
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands, min_detection_confidence=self.detectionConf, min_tracking_confidence= self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, frame, draw=True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)
        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return frame
    
    def findPosition(self, img, handNo=0, draw=True):
        
        lmList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for i, lm in enumerate (hand.landmark) :
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((i,cx,cy))
                if draw:
                    cv2. circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList
    
def main():
    pass

if __name__ == '__main__':
    main()

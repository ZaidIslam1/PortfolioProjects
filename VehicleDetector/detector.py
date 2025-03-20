import cv2
import numpy as np

# Configuration variables for the video processing
VIDEO_PATH = 'video.mp4'
V_NAME = ''
COUNT_LINE_POS = 0        # Line position
MIN_WIDTH_RECT = 0
MIN_HEIGHT_RECT = 0
OFFSET = 0                # Pixel OFFSET for counting line
LINE_PT1 = 0
LINE_PT2 = 0
PURPLE = (138, 0, 158)    # Line color
DETECTED = []             # List to keep track of detected vehicles
COUNTER = 0               # Vehicle Detection Counter

# Video settings based on the video path
if VIDEO_PATH == 'video1.mp4':
    COUNT_LINE_POS = 580
    MIN_WIDTH_RECT = 71
    MIN_HEIGHT_RECT = 71
    OFFSET = 2
    LINE_PT1 = 480
    LINE_PT2 = 750
    V_NAME = 'Bridge Video'
    
elif VIDEO_PATH == 'video.mp4':
    COUNT_LINE_POS = 583
    MIN_WIDTH_RECT = 85
    MIN_HEIGHT_RECT = 85
    OFFSET = 8
    LINE_PT1 = 65
    LINE_PT2 = 1140 
    V_NAME = 'Highway Video'

# Initialize the background subtractor and video capture
backSub = cv2.bgsegm.createBackgroundSubtractorMOG()

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    exit()

# Helper function to calculate the center of a rectangle
def center_rect(x1, y1, width, height):
    center_x = x1 + int(width / 2)
    center_y = y1 + int(height / 2)    
    return center_x, center_y

# Main video processing loop
while True:  
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting ...")
        break
    
    # Image preprocessing
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    fgMask = backSub.apply(blur)
    
    # Morphological operations to clean up the foreground mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilate = cv2.dilate(fgMask, np.ones((5, 5)))
    morphed = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    morphed = cv2.morphologyEx(morphed, cv2.MORPH_CLOSE, kernel)
    
    # Find contours and draw the counting line
    contours, _ = cv2.findContours(morphed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame, (LINE_PT1, COUNT_LINE_POS), (LINE_PT2, COUNT_LINE_POS), color=PURPLE, thickness=2) 
    
    # Process each contour detected
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        if width >= MIN_WIDTH_RECT and height >= MIN_HEIGHT_RECT:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            cv2.putText(frame, "Vehicle", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (80, 150, 255), 2)
            
            center = center_rect(x, y, width, height)
            DETECTED.append(center)
            cv2.circle(frame, center, 4, (0, 0, 255), -1)
            
            for (center_x,center_y) in DETECTED:
                if (COUNT_LINE_POS - OFFSET) < center_y and center_y < (COUNT_LINE_POS + OFFSET):
                    COUNTER += 1
                    cv2.line(frame, (LINE_PT1, COUNT_LINE_POS), (LINE_PT2, COUNT_LINE_POS), color=(0, 127, 255), thickness=2)
                    DETECTED.remove(center)
                    print(f"Vehicle Counter: {COUNTER}")

    # Display the vehicle count
    cv2.putText(frame, f"VEHICLE COUNTER: {COUNTER}", (500, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow(V_NAME, frame)
    
    # Exit condition: break on any key press
    if cv2.waitKey(1) != -1:
        break

# Clean up: release video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()

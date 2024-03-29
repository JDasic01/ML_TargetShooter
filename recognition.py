import cv2
import numpy as np

# Load pre-trained face and mouth cascade classifiers
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier('./haarcascade_mcs_mouth.xml')

# Function to detect face and mouth
def detect_face_and_mouth(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray_image[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]

        # Detect mouth within the face ROI
        mouths = mouth_cascade.detectMultiScale(gray_image, 1.5, 11)
        for(mx, my, mw, mh) in mouths:
            cv2.rectangle(image, (mx, my), (mx+mw, my+mh), (255, 0, 0), 2)
        
    return image

# Test the function with a video stream
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = detect_face_and_mouth(frame)

    cv2.imshow('Mouth Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

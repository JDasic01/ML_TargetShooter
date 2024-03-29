import cv2
import time

# LED colors
LED_RED = (0, 0, 255)
LED_YELLOW = (0, 255, 255)
LED_GREEN = (0, 255, 0)

# Class for face and mouth detection
class FaceDetector:
    def __init__(self, face_cascade_path, mouth_cascade_path):
        self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
        self.mouth_cascade = cv2.CascadeClassifier(mouth_cascade_path)

    def detect_mouth(self, img):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_image, 1.3, 5)
        
        for (x, y, w, h) in faces:
            roi_gray = gray_image[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            # Detect mouth within the face ROI
            mouths = self.mouth_cascade.detectMultiScale(roi_gray, 1.5, 11)
            for (mx, my, mw, mh) in mouths:
                cv2.rectangle(roi_color, (mx, my), (mx + mw, my + mh), (255, 0, 0), 2)
        
        return img

# Class for hand detection
class HandDetector:
    def __init__(self, cascade_path):
        self.hand_cascade = cv2.CascadeClassifier(cascade_path)
        
    def find_hands(self, img, draw=True):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hands = self.hand_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if draw:
            for (x, y, w, h) in hands:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
        return img

    def find_hand_positions(self, img, draw=True):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hands = self.hand_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        hand_positions = []
        for (x, y, w, h) in hands:
            cx, cy = x + w // 2, y + h // 2
            hand_positions.append([cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                
        return hand_positions

# Function to check if LED is supported and set its color
def set_led_color(color):
    # Here you can add code to control the LED color
    # This function is a placeholder to illustrate the concept
    print(f"LED color set to: {color}")

# Main function
def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    # Initialize face and hand detectors
    face_detector = FaceDetector('./haarcascade_frontalface_default.xml', './haarcascade_mcs_mouth.xml')
    hand_detector = HandDetector('./hand.xml')
    # Set LED color to red (indicating startup)
    set_led_color(LED_RED)
    # Variable to track if hand is found
    hand_found = False

    while True:
        success, img = cap.read()

        # If hand is not found yet, search for hands
        if not hand_found:
            img = hand_detector.find_hands(img, draw=False)
            hand_positions = hand_detector.find_hand_positions(img, draw=False)
            if len(hand_positions) > 0:
                # Hand is found, set LED color to yellow
                set_led_color(LED_YELLOW)
                hand_found = True
        
        # If hand is found, start mouth detection
        if hand_found:
            img = face_detector.detect_mouth(img)
            # If mouth is detected, set LED color to green
            set_led_color(LED_GREEN)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

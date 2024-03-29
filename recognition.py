import cv2

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

def main():
    cap = cv2.VideoCapture(0)
    face_detector = FaceDetector('./haarcascade_frontalface_default.xml', './haarcascade_mcs_mouth.xml')
    hand_detector = HandDetector('./hand.xml')
    mouth_found = False

    while True:
        success, img = cap.read()

        if not mouth_found:
            img = hand_detector.find_hands(img, draw=False)
            hand_positions = hand_detector.find_hand_positions(img, draw=False)
            if len(hand_positions) > 0:
                mouth_found = True
        
        if mouth_found:
            img = face_detector.detect_mouth(img)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

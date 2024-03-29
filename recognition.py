import cv2
import math

# Load pre-trained face and hand cascade classifiers
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")
hand_cascade = cv2.CascadeClassifier("hand.xml")

# Known distance from camera to face (in centimeters)
known_distance_cm = 76.2

# Width of the face in the real world (in centimeters)
known_width_cm = 14.3

# Function to calculate focal length
def calculate_focal_length(measured_distance, real_width, width_in_image):
    focal_length = (width_in_image * measured_distance) / real_width
    return focal_length

# Function to calculate distance from camera to object
def calculate_distance(focal_length, real_width, width_in_image):
    distance = (real_width * focal_length) / width_in_image
    return distance

# Function to detect face and calculate distance
def detect_face_and_calculate_distance(image, focal_length):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)

    for (x, y, w, h) in faces:
        # Draw rectangle only around the mouth
        mouth_gray = gray_image[y:y+h, x:x+w]
        mouths = mouth_cascade.detectMultiScale(mouth_gray, 1.5, 11)
        for (mx, my, mw, mh) in mouths:
            cv2.rectangle(image, (x + mx, y + my), (x + mx + mw, y + my + mh), (0, 255, 0), 2)
            # Calculate distance to face
            face_width_in_image = w
            distance_cm = calculate_distance(focal_length, known_width_cm, face_width_in_image)
            # Display distance on the image
            cv2.putText(image, f"Face Distance: {round(distance_cm, 2)} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            # Print mouth coordinates
            mouth_x, mouth_y = x + mx + mw // 2, y + my + mh // 2
            cv2.putText(image, f"Mouth: ({mouth_x}, {mouth_y})", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
    return image

# Function to detect hands and draw rectangles
def detect_hands(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, w, h) in hands:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    return image

# Read reference image to calculate focal length
ref_image = cv2.imread("Ref_image.png")
ref_image_gray = cv2.cvtColor(ref_image, cv2.COLOR_BGR2GRAY)
ref_faces = face_cascade.detectMultiScale(ref_image_gray, 1.3, 5)
if len(ref_faces) > 0:
    ref_face_width = ref_faces[0][2]
    focal_length_found = calculate_focal_length(known_distance_cm, known_width_cm, ref_face_width)
else:
    focal_length_found = None

# Initialize video capture
cap = cv2.VideoCapture(0)
hand_detected = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if focal_length_found is not None:
        if not hand_detected:
            frame = detect_hands(frame)
            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            hands = hand_cascade.detectMultiScale(gray_image, 1.3, 5)
            if len(hands) > 0:
                hand_detected = True

        if hand_detected:
            frame = detect_face_and_calculate_distance(frame, focal_length_found)

    cv2.imshow("Distance and Hand Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

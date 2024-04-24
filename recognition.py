import cv2
import math
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Load pre-trained face and hand cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_mcs_mouth.xml")
hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "hand.xml")

# Known distance from camera to face (in centimeters)
KNOWN_DISTANCE_CM = 76.2

# Width of the face in the real world (in centimeters)
KNOWN_WIDTH_CM = 14.3

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
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 5)

    for (x, y, w, h) in faces:
        # Draw rectangle only around the mouth
        mouth_gray = gray_image[y:y+h, x:x+w]
        mouths = mouth_cascade.detectMultiScale(mouth_gray, 1.1, 11)
        for (mx, my, mw, mh) in mouths:
            cv2.rectangle(image, (x + mx, y + my), (x + mx + mw, y + my + mh), (0, 255, 0), 2)
            # Calculate distance to face
            face_width_in_image = w
            distance_cm = calculate_distance(focal_length, KNOWN_WIDTH_CM, face_width_in_image)
            # Display distance on the image
            cv2.putText(image, f"Face Distance: {round(distance_cm, 2)} cm", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            # Print mouth coordinates
            mouth_x, mouth_y = x + mx + mw // 2, y + my + mh // 2
            cv2.putText(image, f"Mouth: ({mouth_x}, {mouth_y})", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
    return image

# Function to detect hands and draw rectangles
def detect_hands(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(gray_image, 1.1, 5)
    for (x, y, w, h) in hands:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    return image

# Initialize PiCamera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
raw_capture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warm up
time.sleep(0.1)

# Read reference image to calculate focal length
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ref_faces = face_cascade.detectMultiScale(gray_image, 1.1, 5)
    if len(ref_faces) > 0:
        ref_face_width = ref_faces[0][2]
        focal_length_found = calculate_focal_length(KNOWN_DISTANCE_CM, KNOWN_WIDTH_CM, ref_face_width)
        break
    raw_capture.truncate(0)

# Main loop for real-time detection
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array

    if focal_length_found is not None:
        image = detect_face_and_calculate_distance(image, focal_length_found)

    image = detect_hands(image)

    cv2.imshow("Distance and Hand Detection", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    raw_capture.truncate(0)

cv2.destroyAllWindows()
camera.close()

import cv2
import serial

# Open serial port
ser = serial.Serial('COM3', 9600)  # Adjust 'COM3' to match your Arduino's serial port

# Initialize face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Loop through detected faces
    for (x, y, w, h) in faces:
        # Send coordinates of the face to Arduino
        face_center_x = x + w // 2
        face_center_y = y + h // 2
        ser.write(f"{face_center_x},{face_center_y}\n".encode())
        
        # Display rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Display the frame
    cv2.imshow('Face Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close serial port
cap.release()
cv2.destroyAllWindows()
ser.close()

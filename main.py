from recognition import *
import cv2

if __name__ == "__main__":
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
                distances, mouth_coordinates = detect_face_and_calculate_distance(frame, focal_length_found)
                for distance, (mouth_x, mouth_y) in zip(distances, mouth_coordinates):
                    cv2.putText(frame, f"Mouth: ({mouth_x}, {mouth_y})", (mouth_x, mouth_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.putText(frame, f"Distance: {round(distance, 2)} cm", (mouth_x, mouth_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Distance and Hand Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

import RPi.GPIO as GPIO
import time

# Define GPIO pins for servo motors
SERVO_UP_DOWN_PIN = 18
SERVO_LEFT_RIGHT_PIN = 17

# Set the GPIO mode and pin numbering
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for servo motors
GPIO.setup(SERVO_UP_DOWN_PIN, GPIO.OUT)
GPIO.setup(SERVO_LEFT_RIGHT_PIN, GPIO.OUT)

# Set up PWM for servo motors
servo_up_down = GPIO.PWM(SERVO_UP_DOWN_PIN, 50)  # 50 Hz frequency
servo_left_right = GPIO.PWM(SERVO_LEFT_RIGHT_PIN, 50)

# Start PWM with 0% duty cycle
servo_up_down.start(0)
servo_left_right.start(0)

# Function to move servo motors based on mouth coordinates
def move_servos(mouth_x, mouth_y):
    # Convert mouth coordinates to servo angles
    up_down_angle = 90 - (mouth_y * 90 / 500)  # Adjust as needed
    left_right_angle = 90 + (mouth_x * 90 / 500)  # Adjust as needed
    
    # Map angles to duty cycles
    up_down_duty = (up_down_angle / 180.0) * 10 + 2.5
    left_right_duty = (left_right_angle / 180.0) * 10 + 2.5
    
    # Change PWM duty cycles to move servos
    servo_up_down.ChangeDutyCycle(up_down_duty)
    servo_left_right.ChangeDutyCycle(left_right_duty)
    
    time.sleep(0.5)  # Adjust as needed to control the speed of movement

# Function to clean up GPIO
def cleanup():
    servo_up_down.stop()
    servo_left_right.stop()
    GPIO.cleanup()

# Example usage:
if __name__ == "__main__":
    try:
        # Move servo motors to initial position (90 degrees)
        move_servos(90, 90)
        time.sleep(1)  # Wait for servos to move
        
        # Move servo motors based on mouth coordinates (example)
        # Replace these values with the actual mouth coordinates
        mouth_x = 50
        mouth_y = 50
        
        # Move servo motors to track mouth coordinates
        move_servos(mouth_x, mouth_y)
        
        # Wait for user to press Enter before cleaning up GPIO
        input("Press Enter to exit...")
        
    except KeyboardInterrupt:
        pass

    finally:
        cleanup()

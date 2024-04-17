import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set pin numbers for controlling the DC motor
left_pin = 17  # Pin to turn the motor left
right_pin = 27 # Pin to turn the motor right

# Setup DC motor pins
GPIO.setup(left_pin, GPIO.OUT)
GPIO.setup(right_pin, GPIO.OUT)

# Function to turn the motor left for a specified duration
def turn_left(duration):
    GPIO.output(left_pin, GPIO.HIGH)  # Turn left pin on
    time.sleep(duration)              # Wait for the specified duration
    GPIO.output(left_pin, GPIO.LOW)   # Turn left pin off

# Function to turn the motor right for a specified duration
def turn_right(duration):
    GPIO.output(right_pin, GPIO.HIGH) # Turn right pin on
    time.sleep(duration)               # Wait for the specified duration
    GPIO.output(right_pin, GPIO.LOW)  # Turn right pin off

try:
    while True:
        # Turn the motor left for 1 second
        turn_left(1)
        
        # Turn the motor right for 1 second
        turn_right(1)

except KeyboardInterrupt:
    GPIO.cleanup()

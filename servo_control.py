from gpiozero import Servo
from time import sleep
import RPi.GPIO as GPIO

# Servo setup
servo = Servo(12)

# Define GPIO pins for stepper motor
motorPin1 = 8  # Blue - 28BYJ48 pin 1
motorPin2 = 7  # Pink - 28BYJ48 pin 2
motorPin3 = 25  # Yellow - 28BYJ48 pin 3
motorPin4 = 1  # Orange - 28BYJ48 pin 4

# Define motor speed and other variables
motorSpeed = 0.0012  # variable to set stepper speed in seconds (equivalent to 1200 microseconds)
count = 0  # count of steps made
countsperrev = 512  # number of steps per full revolution
lookup = [0b01000, 0b01100, 0b00100, 0b00110, 0b00010, 0b00011, 0b00001, 0b01001]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)
GPIO.setup(motorPin3, GPIO.OUT)
GPIO.setup(motorPin4, GPIO.OUT)

def setOutput(out):
    GPIO.output(motorPin1, (lookup[out] & 0b0001) > 0)
    GPIO.output(motorPin2, (lookup[out] & 0b0010) > 0)
    GPIO.output(motorPin3, (lookup[out] & 0b0100) > 0)
    GPIO.output(motorPin4, (lookup[out] & 0b1000) > 0)

def anticlockwise():
    for i in range(8):
        setOutput(i)
        sleep(motorSpeed)

def clockwise():
    for i in range(7, -1, -1):
        setOutput(i)
        sleep(motorSpeed)

try:
    while True:
        for _ in range(countsperrev):
            for angle in range(-90, 91, 10):
                servo.value = angle / 90
                sleep(0.1)
            for angle in range(91, -90, 10):
                servo.value = angle / 90
                sleep(0.1)    
            clockwise()
        
        for _ in range(countsperrev):
            for angle in range(-90, 91, 10):
                servo.value = angle / 90
                sleep(0.1)
            for angle in range(91, -90, 10):
                servo.value = angle / 90
                sleep(0.1)    
            anticlockwise()
        
        count += 1
        
except KeyboardInterrupt:
    GPIO.cleanup()

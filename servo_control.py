from gpiozero import Servo
from time import sleep

servo = Servo(12)

print("middle")
servo.mid()
sleep(5)
print("max")
servo.max()
sleep(5)
print("min")
servo.min()
sleep(5)
print("middle")
servo.mid()
sleep(5)
servo.value = None;
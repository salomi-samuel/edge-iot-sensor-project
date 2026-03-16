import RPi.GPIO as GPIO
import time

PIR = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)

print("Testing PIR...")

while True:
    motion = GPIO.input(PIR)
    print("Motion:", motion)
    time.sleep(1)

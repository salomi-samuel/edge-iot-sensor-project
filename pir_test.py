import RPi.GPIO as GPIO
import time

PIR = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)

print("PIR Sensor Test Started")

try:
    while True:
        if GPIO.input(PIR):
            print("Motion Detected!")
        else:
            print("No Motion")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

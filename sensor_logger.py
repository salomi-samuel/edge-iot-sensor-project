import RPi.GPIO as GPIO
import time
import csv
import requests
from datetime import datetime

# Sensor pins
PIR = 17
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIR, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

print("Edge filtering active...")

url = "https://edge-iot-sensor-project.onrender.com/upload"

try:
    while True:

        motion = GPIO.input(PIR)

        GPIO.output(TRIG, False)
        time.sleep(0.2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        start = time.time()
        stop = time.time()

        while GPIO.input(ECHO) == 0:
            start = time.time()

        while GPIO.input(ECHO) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = elapsed * 17150
        distance = round(distance, 2)

        now = datetime.now()

        # Send data to cloud
        data = {
            "time": str(now),
            "motion": motion,
            "distance": distance
        }

        try:
            requests.post(url, data=data)
            print("DATA SENT →", now, motion, distance)
        except:
            print("Server not reachable")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()

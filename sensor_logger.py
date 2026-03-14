import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime

PIR = 17
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PIR, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

print("Edge filtering active...")

with open("sensor_data.csv", "a", newline="") as f:
    writer = csv.writer(f)

    while True:
        motion = GPIO.input(PIR)

        GPIO.output(TRIG, False)
        time.sleep(0.2)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            start = time.time()

        while GPIO.input(ECHO) == 1:
            stop = time.time()

        distance = (stop - start) * 17150
        distance = round(distance, 2)

        now = datetime.now()

        # EDGE FILTERING
        if motion == 1 or distance < 20:

            writer.writerow([now, motion, distance])
            f.flush()

            print("EVENT SENT →", now, motion, distance)

        else:
            print("Ignored (edge filtering)")

        time.sleep(1)

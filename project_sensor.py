import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24
PIR = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(PIR, GPIO.IN)

print("System Ready...")

try:
    while True:
        if GPIO.input(PIR):
            print("Motion Detected!")

            GPIO.output(TRIG, False)
            time.sleep(0.5)

            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150

            print("Distance:", round(distance,2), "cm")

        else:
            print("No motion")

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

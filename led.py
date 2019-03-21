import RPi.GPIO as GPIO
import time

pins = [12,32,33,35]

GPIO.setmode(GPIO.BOARD)
try:
    for i in pins:
        print(i)
        GPIO.setup(i, GPIO.OUT)
        p = GPIO.PWM(i,50)
        p.start(33)
        time.sleep(1)
        p.ChangeDutyCycle(66)
        time.sleep(1)
        p.ChangeDutyCycle(100)
        p.stop()
finally:
    GPIO.cleanup()

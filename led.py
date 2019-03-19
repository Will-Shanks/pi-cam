"""Everything to do with lighting up LEDs"""

import RPi.GPIO as GPIO
import time

# hardware pwm on gpio12,13,18,19

LOW = 25
MED = 50
HIGH = 75
FULL = 100

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)
p.start(1)
for i in (MED, HIGH, FULL):
    time.sleep(15)
    p.ChangeDutyCycle(i)


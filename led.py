"""LED test script"""

import RPi.GPIO as GPIO
import time

#pins = [12,13,18,19]
pins = [12,32,33,35]

GPIO.setmode(GPIO.BOARD)
try:
    for i in pins:
        print("gpio pin " + str(i))
        GPIO.setup(i, GPIO.OUT)
        p = GPIO.PWM(i,100)
        p.start(0)
        for i in range(101):
            time.sleep(0.01)
            p.ChangeDutyCycle(i)
            if(i%10 == 0):
                print("\t power: "+str(i))
        p.stop()
finally:
    GPIO.cleanup()

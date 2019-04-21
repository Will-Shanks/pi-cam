"""LED test script"""

import RPi.GPIO as GPIO


class LED:
    """Wrapper class for LEDs"""

    def __init__(self):
        self.pins = [12, 32, 33, 35]
        GPIO.setmode(GPIO.BOARD)
        for i in self.pins:
            GPIO.setup(i, GPIO.OUT)
        self.p = [GPIO.PWM(i,100) for i in self.pins]
        self.cur_level = 0

    def __del__(self):
        try:
            for i in self.p:
                i.stop()
        finally:
            GPIO.cleanup()

    def set_level(self, level):
        """Set LED pwm duty cycle, 0 to 100%"""
        if level < 0:
            level = 0
        if level > 100:
            level = 100
        if self.cur_level == 0 and level != 0:
            print("Turning LEDs on!")
            for i in self.p:
                i.start(level)
        elif self.cur_level != 0 and level == 0:
            print("Turning LEDs off!")
            for i in self.p:
                i.stop()
        elif level != 0:
            for i in self.p:
                i.ChangeDutyCycle(level)
        self.cur_level = level


if __name__ == '__main__':
    import time
    l = LED()
    for i in range(101):
        if i%10 == 0:
            print("power: %d" %(i))
        l.set_level(i)
        time.sleep(.1)
    print("turning off")
    l.set_level(0)
    time.sleep(1)
    for i in reversed(range(101)):
        if i%10 == 0:
            print("power: %d" %(i))
        l.set_level(i)
        time.sleep(.1)
    print("off")
    time.sleep(1)

"""Main control loop"""

import socket
import struct
from subprocess import call

import cam
import led
from options import C_PORT, IP, LEDS, OPS

# encoding >B
sock = socket.socket()
sock.bind((IP, C_PORT))
c = cam.Camera()
l = led.LED()
try:
    while True:
        sock.listen(0)
        con = sock.accept()[0]
        op = struct.unpack('>B', con.recv(1))[0]

        if op == OPS.PI_OFF:
            c.stop()
            l.set_level(0)
            print("Turning off")
            break
            #call("shutdown --poweroff", shell=True)
        elif op == OPS.CAM_OFF:
            c.stop()
        elif op == OPS.CAM_ON:
            c.start()
        elif op == OPS.LED_OFF:
            l.set_level(0)
        elif op == OPS.LED_LOW:
            l.set_level(LEDS.LOW)
        elif op == OPS.LED_MED:
            l.set_level(LEDS.MED)
        elif op == OPS.LED_HIGH:
            l.set_level(LEDS.HIGH)

        con.close()
finally:
    sock.close()
    c.stop()
    l.set_level(0)
    print("Something Bad happened!")
    #call("reboot", shell=True)

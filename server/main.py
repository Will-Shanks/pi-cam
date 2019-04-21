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
#try:
while True:
    sock.listen(0)
    con = sock.accept()[0]
    op = int(struct.unpack('>B', con.recv(1))[0])
    print("OP: "+ OPS(op).name)
    if op == OPS.PI_OFF.value:
        c.stop()
        l.set_level(0)
        print("Turning off")
        break
        #call("shutdown --poweroff", shell=True)
    elif op == OPS.CAM_OFF.value:
        c.stop()
        l.set_level(0)
    elif op == OPS.CAM_ON.value:
        c.start()
    elif op == OPS.LED_OFF.value:
        l.set_level(0)
    elif op == OPS.LED_LOW.value:
        l.set_level(LEDS.LOW.value)
    elif op == OPS.LED_MED.value:
        l.set_level(LEDS.MED.value)
    elif op == OPS.LED_HIGH.value:
        l.set_level(LEDS.HIGH.value)

    con.close()
#finally:
sock.close()
c.stop()
del l
del c
del sock
print("Something Bad happened!")
#call("reboot", shell=True)

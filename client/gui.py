import socket
import struct
import tkinter

from options import C_PORT, IP, OPS

window = tkinter.Tk()
window.title("A Basic GUI")
window.geometry('400x200')


def send_cmd(op):
    sock = socket.socket()
    sock.connect((IP, C_PORT))
    sock.send(struct.pack('>B', int(op.value)))
    sock.close()
    window.mainloop()


def l_off_c():
    send_cmd(OPS.LED_OFF)


def l_low_c():
    send_cmd(OPS.LED_LOW)


def l_med_c():
    send_cmd(OPS.LED_MED)


def l_high_c():
    send_cmd(OPS.LED_HIGH)


def cam_off():
    send_cmd(OPS.CAM_OFF)


def cam_on():
    send_cmd(OPS.CAM_ON)


def pi_off():
    send_cmd(OPS.PI_OFF)


send_cmd(OPS.PI_OFF)

led_off = tkinter.Button(window, text="LEDs off", command=l_off_c)
led_off.grid(column=0, row=0)
led_low = tkinter.Button(window, text="LEDs low", command=l_low_c)
led_low.grid(column=1, row=0)
led_med = tkinter.Button(window, text="LEDs med", command=l_med_c)
led_med.grid(column=2, row=0)
led_high = tkinter.Button(window, text="LEDs high", command=l_high_c)
led_high.grid(column=3, row=0)
cam_off = tkinter.Button(window, text="Camera Off", command=cam_off)
cam_off.grid(column=0, row=1)
cam_on = tkinter.Button(window, text="Camera On", command=cam_on)
cam_on.grid(column=1, row=1)
pi_off = tkinter.Button(window, text="Pi Off", command=pi_off)
pi_off.grid(column=0, row=2)
window.mainloop()

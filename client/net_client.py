import socket
import struct

from options import C_PORT, IP

#encoding >B
while True:
    a = input("enter number 0-255\n")

    sock = socket.socket()
    sock.connect((IP, C_PORT))
    sock.send(struct.pack('>B', int(a)))
    sock.close()

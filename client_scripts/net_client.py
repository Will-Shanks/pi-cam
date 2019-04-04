import socket
import struct

#encoding >B
while True:
    a = input("enter number 0-255\n")

    sock = socket.socket()
    sock.connect(('127.0.0.1', 8000))
    sock.send(struct.pack('>B', int(a) % 255))
    sock.close()

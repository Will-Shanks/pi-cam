import socket
import struct

from options import C_PORT, IP, OPS

# encoding >B
while True:
    a = input("enter desired option " + str([i.name for i in OPS]) + '\n')

    if not OPS[a]:
        continue

    sock = socket.socket()
    sock.connect((IP, C_PORT))
    sock.send(struct.pack('>B', int(OPS[a].value)))
    sock.close()

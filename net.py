import socket
import struct

# encoding >B
sock = socket.socket()
sock.bind(('127.0.0.1', 8000))
try:
    while True:
        sock.listen(0)
        con = sock.accept()[0]
        print(struct.unpack('>B', con.recv(1))[0])
        con.close()
finally:
    sock.close()

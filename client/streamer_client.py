import socket
import struct
import subprocess

from options import FPS, IP, S_PORT

sock = socket.socket()
sock.connect((IP, S_PORT))
con = sock.makefile('rb')

cmdline = ['cvlc', '--demux', 'h264', '--h264-fps', str(FPS), '-']
player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
fh = open('test.h264', 'wb')
try:
    while True:
        data = con.read(1024)
        if not data:
            break
        for b in data:
            byte = struct.unpack('>c', b)
            fh.write(byte)
            player.stdin.write(byte)

except KeyboardInterrupt:
    pass

finally:
    fh.close()
    con.close()
    sock.close()
    player.terminate()

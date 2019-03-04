import socket
import subprocess

from options import FPS, IP, S_PORT

import time

sock = socket.socket()
sock.connect((IP, S_PORT))
con = sock.makefile('rb')


cmdline = ['vlc', '--demux', 'h264', '--h264-fps', str(FPS), '-']
player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
try:
    while True:
        data = con.read(1024)
        if not data:
            break
        player.stdin.write(data)

finally:
    con.close()
    sock.close()
    player.terminate()

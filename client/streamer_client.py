import socket
import subprocess
import time

from options import FPS, IP, S_PORT

cmdline = [
    'cvlc', '--demux', 'h264', '--h264-fps',
    str(FPS), 'tcp/h264://' + IP + ':' + str(S_PORT)
]
try:
    player = subprocess.Popen(cmdline)
    while True:
        time.sleep(10)

finally:
    player.terminate()

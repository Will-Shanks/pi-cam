import socket
import subprocess
import time

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
sock = socket.socket(socket.AF_NET, socket.SOCK_DGRAM)
connection = sock.connect(('192.168.0.10',8000))
time.sleep(10)

try:
   # Run a viewer with an appropriate command line. Uncomment the mplayer
   # version if you would prefer to use mplayer instead of VLC
   cmdline = ['vlc', '--demux', 'h264', '-']
   #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
   player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
   while True:
       # Repeatedly read 1k of data from the connection and write it to
       # the media player's stdin
       data = connection.read(1024)
#       if not data:
#           break
       player.stdin.write(data)
finally:
    sock.close()
#   connection.close()
#   server_socket.close()
 #  player.terminate()

import socket
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
#client_socket = socket.socket()
#client_socket.connect(('192.168.0.15',8000))
client_socket = socket.create_connection(('192.168.0.11', 8000))

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)
#(William, the two lines of code above was not included in the website. Without these 2 lines of code, the stream would only work the 1st time, not a second time. Without the code, we had to restart both pis for it to work.)

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)
    # Start recording, sending the output to the connection for 60
    # seconds, then stop
    camera.start_recording(connection, format='h264')
    camera.wait_recording(60)
    camera.stop_recording()
finally:
    connection.close()
    client_socket.close()

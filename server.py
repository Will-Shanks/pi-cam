import picamera
import os
import threading
import time
import socket
import shutil

RECORD_DIR='/home/pi/pi-cam/recordings' # save recordings in this dir
STREAM_IP = ('192.168.0.10',8000) # stream recording out this socket
SEC_PER_RECORDING = 60 #save recordings in 60 sec segments
RECORDING_RES = (1920,1080)#(640, 480)
RECORDING_FPS = 30#24
MIN_FREE_SPACE = int(2e9) #minimum free space in fs, 2GiB


class OutputStream(object):
    def __init__(self, filedir, ip_sock):
        '''
        filedir: string path to dir to save video to
        ip_sock: ('eth0 ip', socket) tuple for socket to stream out of
        '''
        print("initializing streaming obj")
        self._dir = filedir
        self._filename = str(int(time.time()/SEC_PER_RECORDING))
        self._fh = open(filedir+"/"+self._filename + '.h264', 'wb')
        #TODO: UDP socket
        #TODO add locking for thread
        #TODO debug network problem
        self._sock = socket.socket()#socket.AF_INET, socket.SOCK_DGRAM) #ipv4 udp socket
        self._sock.bind(ip_sock)
        self._is_connected = False
        self._connection = None
        self._listen()

    def _listen(self):
        #TODO: Handle connection termination (listen for a new connection)
        try:
            t = threading.Thread(name='sock_listener', target=self._get_connection)
            t.setDaemon(True)
            t.start()
        except:
            print("unable to start listening thread")

    def _get_connection(self):
        print("listening for incoming connection")
        self._sock.listen(0)
        self._connection = self._sock.accept()[0].makefile('wb')
        self._is_connected = True
        print("found connection")

    def write(self, s):
        # Write to current file, or open new one if has been sec_per_recording
        fn = str(int(time.time()/SEC_PER_RECORDING))
        if fn != self._filename:
            self._fh.close()
            self._filename = fn
            self._fh = open(self._dir+"/"+fn + '.h264', 'wb')
            print("changing file")
        self._fh.write(s)
        #if socket bound, stream out of it
        if self._connection:
            print("writing to socket")
            bytes_sent = self._connection.write(s)
            return bytes_sent

    def close(self):
        # Gracefully close everything at end of stream
        self._fh.close()
        if self._is_connected:
            self._is_connected = False
            self._connection.close()
            self._connection = None
            self._sock.close()


def garbage_collection():
    while(1):
        if(shutil.disk_usage(RECORD_DIR).free <= MIN_FREE_SPACE):
            #delete oldest recording
            oldest = min(os.listdir(RECORD_DIR), key=lambda x: int(x[:-5]))
            print("garbage collector: deleting oldest recording %s" %oldest)
            os.remove(RECORD_DIR+"/"+oldest)
        print("garbage collector: sleeping")
        time.sleep(SEC_PER_RECORDING/2)

def ensure_dir(d):
    '''make sure dir exists'''
    if not os.path.isdir(d):
        os.makedirs(d)
    print("made sure %s exists" %d)

def main():
    print("starting")
    ensure_dir(RECORD_DIR)
    # start garbage collection
    print("starting garbage collection thread")
    t = threading.Thread(name='garbage_collection', target=garbage_collection)
    t.setDaemon(True)
    t.start()
    # record forever
    print("starting camera")
    stream = OutputStream(RECORD_DIR, STREAM_IP)
    with picamera.PiCamera() as camera:
        camera.resolution = RECORDING_RES
        camera.framerate = RECORDING_FPS
        while True:
            camera.start_recording(stream, format='h264')
            camera.wait_recording(30)
            camera.stop_recording()
            print("recorded another 30sec")
    stream.close()
if __name__ == '__main__':
    main()


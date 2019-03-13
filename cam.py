"""
All code that deals directly with the picamera
"""
import os
import socket
import threading
import time

import picamera
from memoryManager import MemoryManager
from options import FPS, IP, R_FILE_DIR, R_INTERVAL, R_RES, S_PORT, S_RES


class Saver:
    "write stream into files in chunkcs of R_INTERVAL secs"

    def __init__(self):
        self._fn = None
        self._fh = None
        if not os.path.isdir(R_FILE_DIR):
            os.makedirs(R_FILE_DIR)

    def write(self, s):
        """
        writes s to a file named  '<epoch time / R_INTERVAL>.h264'
        """
        fn = str(int(time.time() / R_INTERVAL))
        # if fn != current fn, then in next R_INTERVAL
        if fn != self._fn:
            # could be no open file (if just started) so try closing file
            # try:
            self._fh.close()
            # except <error?>:
            #   pass
            self._fh = None
            self._fn = fn
            self._fh = open(R_FILE_DIR + "/" + fn + ".h264", 'wb')
        self._fh.write(s)
        # always writes all of s so return len(s)
        return len(s)

    def close(self):
        "cleans up any open files"
        # try:
        self._fh.close()
        # catch <same error?>:
        # pass
        self._fh = None
        self._fn = None


class Camera:
    "Object for recording and streaming video in a background thread"

    def __init__(self):
        self._sock = socket.socket()
        self._sock.bind(IP, S_PORT)
        self._con = None
        self._c = threading.Event()
        self._lT = None
        self._S = Saver()
        self._T = None
        self._M = MemoryManager()
        self._d = threading.Event()
        self.start()

    def start(self):
        "Starts recording video and listening for streaming client"
        if self._T is not None and self._T.is_alive():
            return False
        self._M.start()
        self._T = threading.Thread(target=self._record)
        self._T.start()
        self._lT = threading.Thread(target=self._listen)
        self._lT.start()
        return True

    def stop(self):
        "Stops Recording and Streaming within 20 sec"
        if self._T is not None and self._T.is_alive():
            self._d.set()  # signal for thread to shutdown
            self._T.join(20)  # wait 20 sec, or till thread shuts down
            # check if thread shutdown
            if self._T.is_alive() or self._lT.is_alive():
                return False
            self._d.clear()
            self._c.clear()
            self._sock.close()
            self._M.stop()
        return True

    def _record(self):
        with picamera.PiCamera() as c:
            c.resolution = R_RES
            c.framerate = FPS
            # Start recording to file
            c.start_recording(self._S, format='h264')
            while not self._d.is_set():
                # try:
                if self._c.is_set():
                    c.start_recording(
                        self._con,
                        splitter_port=2,
                        format='h264',
                        resize=S_RES)
                    self._c.clear()
                c.wait_recording(5)
                # except <errors from stream disconnect>:
                # c.stop_recording(splitter_port=2)
                # self._con.close()
                # self._con = None
                # self._lT = threading.Thread(target=self._listen)
                # self._lT.start()
            c.stop_recording(splitter_port=2)
            c.stop_recording()
            self._S.close()

    def _listen(self):
        self._sock.settimeout(10)
        while not self._d.is_set():
            # use timeout and try/except block to check _d ~ every 10 sec
            try:
                self._sock.listen()
                self._con = self._sock.accept()[0].makefile('wb')
                self._c.set()
            except socket.timeout:
                pass


if __name__ == "__main__":
    cam = Camera()
    cam.start()
    time.sleep(120)
    cam.stop()
    time.sleep(120)

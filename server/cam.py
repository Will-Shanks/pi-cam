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


class Streamer:
    "writes to stream if connection exists"

    def __init__(self):
        print("streamer started")
        self._sock = socket.socket()
        self._sock.bind((IP, S_PORT))
        self._con = None
        self._d = threading.Event()
        self._T = threading.Thread(target=self._listen)
        self._T.start()

    def __del__(self):
        self.close()

    def write(self, s):
        "writes to socket if there is a connection"
        if self._con:
            try:
                self._con.write(s)
            except:
                self._clean_and_listen()

    def close(self):
        "clean up connections"
        self._d.set()  # signal for thread to shutdown
        try:
            self._con.close()
        except:
            pass
        if self._T and self._T.is_alive():
            self._T.join(5)  # wait 5 sec, or till thread shuts down
        self._con = None
        try:
            self._sock.close()
        except AttributeError:
            pass
        self._sock = None
        self._T = None
        self._d.clear()


    def _clean_and_listen(self):
        print("con lost, looking for a new one")
        try:
            self._con.close()
        except:
            pass
        self._con = None
        self._T = threading.Thread(target=self._listen)
        self._T.start()

    def _listen(self):
        self._sock.settimeout(1)
        while not self._d.is_set():
            try:
                self._sock.listen(0)
                self._con = self._sock.accept()[0].makefile('wb')
                break
            except socket.timeout:
                pass
            except OSError:
                pass
        print("connection found!")


class Saver:
    "write stream into files in chunkcs of R_INTERVAL secs"

    def __init__(self):
        print("Saver made")
        self._fn = None
        self._fh = None
        if not os.path.isdir(R_FILE_DIR):
            os.makedirs(R_FILE_DIR)

    def __del__(self):
        self.close()

    def write(self, s):
        """
        writes s to a file named  '<epoch time / R_INTERVAL>.h264'
        """
        fn = str(int(time.time() / R_INTERVAL))
        # if fn != current fn, then in next R_INTERVAL
        if fn != self._fn:
            # could be no open file (if just started) so try closing file
            try:
                self._fh.close()
            except AttributeError:
                pass
            self._fh = None
            self._fn = fn
            self._fh = open(R_FILE_DIR + "/" + fn + ".h264", 'wb')
            print("opening file: %s.h264" % fn)
        self._fh.write(s)
        # always writes all of s so return len(s)
        return len(s)

    def close(self):
        "cleans up any open files"
        print("Saver closed")
        try:
            self._fh.close()
        except AttributeError:
            pass
        self._fh = None
        self._fn = None


class Camera:
    "Object for recording and streaming video in a background thread"

    def __init__(self):
        self._con = None
        self._S = None
        self._T = None
        self._M = MemoryManager()
        self._d = threading.Event()
        self.start()

    def start(self):
        "Starts recording video and listening for streaming client"
        if self._T is not None and self._T.is_alive():
            return False
        print("starting cam")
        self._con = Streamer()
        self._S = Saver()
        self._M.start()
        self._T = threading.Thread(target=self._record)
        self._T.start()
        return True

    def stop(self):
        "Stops Recording and Streaming within 20 sec"
        print("stoping cam")
        if self._T is not None and self._T.is_alive():
            self._d.set()  # signal for thread to shutdown
            self._T.join(10)  # wait 20 sec, or till thread shuts down
            # check if thread shutdown
        print("cam stopped")
        self._T = None
        self._S = None
        self._con = None
        self._d.clear()
        self._M.stop()
        return True

    def _record(self):
        print("started recording thread")
        with picamera.PiCamera() as c:
            c.resolution = R_RES
            c.framerate = FPS
            # Start recording to file
            try:
                c.start_recording(self._S, format='h264')
                c.start_recording(
                    self._con, splitter_port=2, format='h264', resize=S_RES)
                while not self._d.is_set():
                    c.wait_recording(5)
            finally:
                print("Ending recording")
                c.stop_recording()
                self._S.close()
                c.stop_recording(splitter_port=2)
                self._con.close()


if __name__ == "__main__":
    cam = Camera()
    try:
        cam.start()
        while True:
            time.sleep(10)
    finally:
        cam.stop()

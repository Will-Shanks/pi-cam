"""
Recorder class provides an API to record through the picamera module
and save video in segments
"""
import os
import threading
import time

import picamera
from memoryManager import MemoryManager
from options import R_FILE_DIR, R_FPS, R_INTERVAL, R_RES


class Saver:
    "designed to write stream into chunks of R_INTERVAL long"

    def __init__(self):
        self._dir = R_FILE_DIR
        self._interval = R_INTERVAL
        self._fn = None
        self._fh = None

        if not os.path.isdir(self._dir):
            os.makedirs(self._dir)

    def write(self, s):
        """
        api function called by picamera to save recording video
        saves byte stream in chunks of R_INTERVAL sec long
        """
        fn = str(int(time.time() / self._interval))
        # if a file is open, and its the wrong one close it
        if fn != self._fn and self._fh:
            self._fh.close()
            self._fh = None
        if not self._fh:
            print("opening file " + fn + ".h264")
            self._fn = fn
            self._fh = open(self._dir + "/" + fn + ".h264", "wb")
        self._fh.write(s)
        return len(s)  # always writes all the bytes

    def close(self):
        "frees and nulls memory objects"
        self._fh.close()
        self._fh = None
        self._fn = None


class Recorder:
    "API for recording video in new background thread"

    def __init__(self):
        self._res = R_RES
        self._fps = R_FPS
        self._S = Saver()
        self._T = None
        self._M = MemoryManager()
        self._d = threading.Event()

    def start(self):
        "Starts new thread to record"
        if self._T:
            return False
        print("Starting recorder")
        self._M.start()
        self._T = threading.Thread(name='recorder_thread', target=self._record)
        self._T.start()
        return True

    def stop(self):
        "signals recorder thread to stop"
        if self._T:
            self._d.set()
            self._T.join(20)
            if self._T.is_alive():
                return False
            self._T = None
            self._d.clear()
            self._M.stop()
            print("Recorder Stopped")

        return True

    def _record(self):
        print("Recording")
        with picamera.PiCamera() as camera:
            camera.resolution = self._res
            camera.framerate = self._fps
            camera.start_recording(self._S, format='h264')

            while not self._d.is_set():
                camera.wait_recording(5)
            camera.stop_recording()
        self._S.close()


if __name__ == '__main__':
    r = Recorder()
    r.start()
    time.sleep(120)
    r.stop()
    time.sleep(120)

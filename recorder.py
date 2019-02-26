import threading
import time

from memoryManager import memoryManager
from options import R_FILE_DIR, R_INTERVAL, R_RES, R_FPS

class Saver(object):
    def __init__(self):
        self._dir = R_FILE_DIR
        self._interval = R_INTERVAL
        self._fn = None
        self._fh = None

    def write(self, s):
        fn = str(int(time.time()/self._interval))
        if fn != self._fn and self._fh: #if a file is open, and its the wrong one
            self._fh.close()
            self._fh = None
        if not self._fh:
            print("opening file" + fn)
            self._fn = fn
            self._fh = open(self._dir+"/"+fn+".h264", "wb")
        self._fh.write(s)
        return len(s) #always writes all the bytes

    def close(self):
        self._fh.close()
        self._fh = None
        self._fn = None


class Recorder(object):
    def __init__(self):
        self._res = R_RES
        self._fps = R_FPS
        self._S = Saver()
        self._L = threading.Lock
        self._T = None
        self._G = memoryManager()
        self._d = threading.Event()

    def start(self):
        if self._T:
            return False
        self._T =  threading.Thread(name="recorder", target=self._start)
        return True

    def stop(self):
        if self._T:
            self._d.set()
            self._T.join(20)
            if self._T.is_alive():
                return False
            self._T = None
            self._d.clear()
        return True

    def _start(self):
        with picamera.PiCamera as cam:
            camera.resolution = self.g_res()
            camera.framerate = self.g_fps()
            camera.start_recording(self._S, format='h264')
            while(self._d.is_set()):
                camera.wait_recording(5)
            camera.stop_recording()
        self._S.close()


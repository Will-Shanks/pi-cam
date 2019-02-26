import shutil
import time
import os
import threading

from options import R_INTERVAL, R_FILE_DIR, MIN_FREE_MEM

class MemoryManager:
    def __init__(self):
        self._d = threading.Event()
        self._T = None

    def start(self):
        if self._T:
            return False
        self._T = threading.Thread(target=self._checkMem)
        self._T.start()
        return True

    def stop(self):
        if self._T:
            self._d.set()
            self._T.join(R_INTERVAL)
            if self._T.is_alive():
                return False
            self._T = None
            self._d.clear()
            print("memManager stoped")
        return True

    def _checkMem(self):
        while not self._d.is_set():
            while shutil.disk_usage(R_FILE_DIR).free <= MIN_FREE_MEM and not self._d.is_set():
                oldest = min(os.listdir(R_FILE_DIR), key=lambda x: int(x[:-5]))
                os.remove(R_FILE_DIR+"/"+oldest)
                print("deleting "+oldest)
            time.sleep(R_INTERVAL/2)


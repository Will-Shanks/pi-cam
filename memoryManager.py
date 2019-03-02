"""
MemoryManager class
Designed to ensure disk does not fill up
by deleteing oldest recording file if a min free disk threshold is reached
"""

import os
import shutil
import threading
import time

from options import MIN_FREE_MEM, R_FILE_DIR, R_INTERVAL


class MemoryManager:
    "memoryManager class ensures disk does not fill up"

    def __init__(self):
        self._d = threading.Event()
        self._T = None

    def start(self):
        "starts new thread to monitor free disk"
        if self._T:
            return False
        self._T = threading.Thread(target=self._checkMem)
        self._T.start()

        return True

    def stop(self):
        "signals MemoryManager thread to stop"
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
            while shutil.disk_usage(
                    R_FILE_DIR).free <= MIN_FREE_MEM and not self._d.is_set():
                oldest = min(os.listdir(R_FILE_DIR), key=lambda x: int(x[:-5]))
                os.remove(R_FILE_DIR + "/" + oldest)
                print("deleting " + oldest)
            time.sleep(R_INTERVAL / 2)

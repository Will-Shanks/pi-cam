'''
Class for Streaming Video in a background thread
'''
import socket
import threading

import picamera
from options import FPS, IP, R_RES, S_PORT, S_RES


class Streamer:
    "Streams video if someone is listening"

    def __init__(self):
        self._sock = socket.socket()
        self._sock.bind((IP, S_PORT))
        self._con = None
        self._res = S_RES
        self._T = None
        self._d = threading.Event()

    def start(self):
        "Start streamer thead if not already running"
        if self._T:
            return False
        self._T = threading.Thread(target=self._listen)
        self._T.start()
        return True

    def stop(self):
        "Signal streamer thread to stop"
        if self._T.is_alive():
            self._d.set()
            self._T.join(20)
            if self._T.is_alive():
                return False
            self._sock.close()
            self._d.clear()
            self._T = None
        return True

    def _listen(self):
        self._sock.settimeout(10)
        while not self._d.is_set():
            try:
                self._sock.listen(0)
                self._con = self._sock.accept()[0].makefile('wb')
                self._stream()
            except socket.timeout:
                pass

    def _stream(self):
        try:
            with picamera.PiCamera() as camera:
                # setup camera incase recorder isn't on
                camera.resolution = R_RES
                camera.framerate = FPS
                camera.start_recording(
                    self._con,
                    splitter_port=2,
                    format='h264',
                    resize=self._res)
                while not self._d.is_set():
                    camera.wait_recording(5)
                camera.stop_recording(splitter_port=2)
        finally:
            self._con.close()
            self._con = None
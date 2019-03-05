"""
main api for pi space camera
"""
import time

from recorder import Recorder
from streamer import Streamer

def main():
    """ main loop for space camera api"""
#    r = Recorder()
#    r.start()
    s = Streamer()
    s.start()
    time.sleep(600)
    s.stop()
#    r.stop()


if __name__ == '__main__':
    main()

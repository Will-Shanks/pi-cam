"""
main api for pi space camera
"""
import time

import recorder


def main():
    """ main loop for space camera api"""
    r = recorder.Recorder()
    r.start()
    time.sleep(120)
    r.stop()


if __name__ == '__main__':
    main()

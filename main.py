import time
import threading
import recorder

def main():
    r = recorder.Recorder()
    r.start()
    time.sleep(120)
    r.stop()

if __name__ == '__main__':
    main()


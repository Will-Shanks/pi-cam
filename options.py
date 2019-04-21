"Configuration settings for pi cam"
from enum import Enum

# General settings
IP = '192.168.0.10'
FPS = 60

# Recorder and memory manager options
R_FILE_DIR = "/home/pi/pi-cam/recordings"
R_INTERVAL = 30
R_RES = (640, 480)  # (1920, 1080)

MIN_FREE_MEM = int(2e9)

# Streamer options
S_PORT = 8001  # TCP TODO: use UDP
S_RES = (640, 480)


class LEDS(Enum):
    """LED pwm (power) settings"""
    LOW = 40
    MED = 70
    HIGH = 100


# Control options
C_PORT = 8000


class OPS(Enum):
    """OP code definitions"""
    PI_OFF = 0
    CAM_OFF = 1
    CAM_ON = 2
    LED_OFF = 3
    LED_LOW = 4
    LED_MED = 5
    LED_HIGH = 6

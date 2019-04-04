"Configuration settings for pi cam"

# General settings
IP = '192.168.0.10'
FPS = 5#30

# Recorder and memory manager options
R_FILE_DIR = "/home/pi/pi-cam/recordings"
R_INTERVAL = 30
R_RES = (640,480)#(1920, 1080)

MIN_FREE_MEM = int(2e9)

# Streamer options
S_PORT = 8001  # TCP TODO: use UDP
S_RES = (640, 480)
S_FPS = 5

# Downloader options
D_PORT = 8002

# OpCode definitions
PI_OFF = 0
CAM_OFF = 1
CAM_ON = 2
LED_OFF = 3
LED_LOW = 4
LED_MED = 5
LED_HIGH = 6


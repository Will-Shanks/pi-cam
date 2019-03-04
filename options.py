"Configuration settings for pi cam"

# General settings
IP = '192.168.0.10'
FPS = 30

# Recorder and memory manager options
R_FILE_DIR = "/home/pi/pi-cam/recordings"
R_INTERVAL = 30
R_RES = (1920, 1080)

MIN_FREE_MEM = int(2e9)

# Streamer options
S_PORT = 8001  # TCP TODO: use UDP
S_RES = (640, 480)
S_FPS = 5

# Downloader options
D_PORT = 8002

# OpCode definitions
ops = {}
ops['D_REQ'] = 1

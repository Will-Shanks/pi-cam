# Pi Space-Cam
Records video from the pi camera into h264 format, streams it, and saves it for later
 - saves as much video as possible, but when sd card starts to get full deletes oldes video segments

## Run
- copy the ```options.py``` file into the same directoy as the server scripts
- run ```python3 main.py```

### stream
- To stream video move ```options.py``` into the same directoy as the ```streamer_client.py``` file
- run ```pyton3 streamer_client.py```
- requires vlc

### recordings
- I'm working on a bash script to simplify this


- to use the .h264 files run them through ffmpeg
```ffmpeg -r <record framerate> -i <input h264> -r <record framerate> <output file>```
- to concatenate video segments
```
myfiles.txt
file 'file1.h264'
file 'file2.h264'

ffmpeg -f concat -i myfiles.txt -c copy output.h264
```

#### Potential Concerns
- if ```MIN_FREE_MEM``` is set too high, there won't be enough records in ```R_FILE_DIR``` to delete to create an acceptable amount of free disk
- Current implementation does not allow for different framerates for recording and streaming
- recording must have equal or higher resolution to streaming #TODO: confirm this
- if unix epoch time wraps the memory manager will delete the newest recording segments instead of the oldest
  - a smarted memory managment scheme should be implemented, or the old recording deleted manually if this is a concern


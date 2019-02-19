# Pi Space-Cam
Records video from the pi camera into h264 format, streams it, and saves it for latter
 - saves as much video as possible, but when sd card starts to get full deletes oldes video segments

## To use
- run ```python3 server.py```
- to use the .h264 files run them through ffmpeg
```ffmpeg -r <record framerate> -i <input h264> -r <record framerate> <output file>```
- to concatenate video segments
```
myfiles.txt
file 'file1.h264'
file 'file2.h264'

ffmpeg -f concat -i myfiles.txt -c copy output.h264
```

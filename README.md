`gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' !  x264enc pass=qual quantizer=2 tune=zerolatency ! rtph264pay ! udpsink host=127.0.0.1 port=1234`

# Quick start
## Ubuntu
```
sudo apt install python3-gi-cairo python3-gi python3-gst
```

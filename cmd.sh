gst-launch-1.0 tcpclientsrc host=10.243.81.158 port=9001 ! h264parse ! avdec_h264 ! autovideoconvert ! gtksink

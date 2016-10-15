#!/usr/bin/env python

import signal

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import Gtk
from gi.repository import Gst, Gdk, GdkX11, GstVideo
Gst.init(None)

Gst.init_check(None)


class PipelineManager(object):
    def __init__(self, window, pipeline):
        self.window = window
        if isinstance(pipeline, str):
            pipeline = Gst.parse_launch(pipeline)

        self.pipeline = pipeline

        bus = pipeline.get_bus()
        bus.set_sync_handler(self.bus_callback)
        pipeline.set_state(Gst.State.PLAYING)

    def bus_callback(self, bus, message):
        if message.type is Gst.MessageType.ELEMENT:
            if GstVideo.is_video_overlay_prepare_window_handle_message(message):
                Gdk.threads_enter()
                Gdk.Display.get_default().sync()
                win = self.window.get_property('window')

                if isinstance(win, GdkX11.X11Window):
                    message.src.set_window_handle(win.get_xid())
                else:
                    print('Nope')

                Gdk.threads_leave()
        return Gst.BusSyncReply.PASS




# pipeline = Gst.parse_launch('videotestsrc ! xvimagesink sync=false')
pipeline = 'udpsrc port=1234 ! application/x-rtp, payload=12 ! rtph264depay ! avdec_h264 ! xvimagesink sync=false'
# gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' !  x264enc pass=qual quantizer=2 tune=zerolatency ! rtph264pay ! udpsink host=127.0.0.1 port=1234


builder = Gtk.Builder()
builder.add_from_file('foo.glade')

video_area = builder.get_object('video_area')

pipeline = PipelineManager(video_area, pipeline)

window = builder.get_object("main_window")
window.show_all()
window.connect('destroy', lambda w: Gtk.main_quit())

Gtk.main()

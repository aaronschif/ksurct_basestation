#!/usr/bin/env python

from pprint import pprint

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import Gtk, xlib
from gi.repository import Gst, Gdk, GdkX11, GstVideo
Gst.init(None)
Gst.init_check(None)

# Place 1
from ctypes import cdll
x11 = cdll.LoadLibrary('libX11.so')
x11.XInitThreads()

# [xcb] Unknown request in queue while dequeuing
# [xcb] Most likely this is a multi-threaded client and XInitThreads has not been called
# [xcb] Aborting, sorry about that.
# python3: ../../src/xcb_io.c:179: dequeue_pending_request: Assertion `!xcb_xlib_unknown_req_in_deq' failed.

# (foo.py:31933): Gdk-WARNING **: foo.py: Fatal IO error 11 (Resource temporarily unavailable) on X server :1.

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


pipeline = Gst.parse_launch('videotestsrc ! xvimagesink sync=false')

window = Gtk.ApplicationWindow()

header_bar = Gtk.HeaderBar()
header_bar.set_show_close_button(True)
# window.set_titlebar(header_bar)  # Place 2

drawing_area = Gtk.DrawingArea()
drawing_area.connect('realize', lambda widget: PipelineManager(widget, pipeline))
window.add(drawing_area)

window.show_all()

def on_destroy(win):
    try:
        Gtk.main_quit()
    except KeyboardInterrupt:
        pass

window.connect('destroy', on_destroy)

Gtk.main()

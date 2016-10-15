#!/usr/bin/env python
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import Gtk
from gi.repository import Gst, Gdk, GdkX11, GstVideo
Gst.init(None)

Gst.init_check(None)


class VideoWidget(Gtk.DrawingArea):
    def __init__(self, pipeline):
        super().__init__()

        if isinstance(pipeline, str):
            pipeline = Gst.parse_launch(pipeline)

        bus = pipeline.get_bus()
        bus.set_sync_handler(self.bus_callback)
        pipeline.set_state(Gst.State.PLAYING)

    def bus_callback(self, bus, message):
        if message.type is Gst.MessageType.ELEMENT:
            if GstVideo.is_video_overlay_prepare_window_handle_message(message):
                Gdk.threads_enter()
                Gdk.Display.get_default().sync()
                win = drawing.get_property('window')

                if isinstance(win, GdkX11.X11Window):
                    message.src.set_window_handle(win.get_xid())
                else:
                    print('Nope')

                Gdk.threads_leave()
        return Gst.BusSyncReply.PASS


# pipeline = Gst.parse_launch('videotestsrc ! xvimagesink sync=false')
pipeline = Gst.parse_launch('udpsrc port=1234 ! application/x-rtp, payload=12 ! rtph264depay ! avdec_h264 ! xvimagesink sync=false')
# gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' !  x264enc pass=qual quantizer=2 tune=zerolatency ! rtph264pay ! udpsink host=127.0.0.1 port=1234

drawing = VideoWidget(pipeline)
drawing.set_size_request(640, 480)

window = Gtk.Window()
window.set_size_request(300, 50)
main_box = Gtk.HBox()
entry = Gtk.Entry()
main_box.pack_start(entry, True, True, 0)
log = Gtk.TextView()
log.set_editable(False)
log.set_size_request(30, 30)
main_box.pack_start(log, True, True, 0)
main_box.pack_start(drawing, False, False, 0)
main_box.pack_start(Gtk.Button('Foo'), True, True, 0)
window.add(main_box)
window.show_all()
window.connect('destroy', lambda w: Gtk.main_quit())

Gtk.main()

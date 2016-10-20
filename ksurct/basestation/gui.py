from pathlib import Path

from . import gi_init
from gi.repository import Gtk, GLib

from .video_widget import GstWidget

here = Path(__file__).parent

builder = Gtk.Builder()
builder.add_from_file(str(here/'widgets.glade'))
builder.add_from_file(str(here/'header.glade'))

main_box = builder.get_object('main_box')
video_area = builder.get_object('video_area')
relation_widget = builder.get_object('relation_widget')
header = builder.get_object('header')

# gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' !  x264enc pass=qual quantizer=2 tune=zerolatency ! rtph264pay ! udpsink host=127.0.0.1 port=1234
pipeline = 'udpsrc port=1234 ! application/x-rtp, payload=12 ! rtph264depay ! avdec_h264 ! videoconvert'
# pipeline = 'videotestsrc'


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_icon_from_file(str(here/'icons'/'ksurct.png'))
        self.add(main_box)
        self.set_titlebar(self._create_header())

        video_area.pack_start(GstWidget(pipeline), True, True, 0)

        relation_widget.connect('draw', self._draw_relation_widget)
        GLib.timeout_add(1000/30, self._sced)

    def _create_header(self):
        menu = builder.get_object('menu')
        app_menu = builder.get_object('app-menu')
        menu.bind_model(app_menu, None)
        return header

    def _sced(self):
        relation_widget.queue_draw()
        return True

    def _draw_relation_widget(self, widget, cairo):
        from time import time
        cairo.set_source_rgb(.5, .5, .5)
        cairo.paint()
        cairo.set_source_rgb(1, 0, 0)
        cairo.rectangle(20, 20, 20, 20 + 10*(time()%40))
        cairo.stroke()


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='ksurct.basestation')

        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="ksurct Basestation")
            self.window.show_all()

        self.window.present()

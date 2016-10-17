from pathlib import Path
from pprint import pprint

from . import gi_init
from gi.repository import Gtk, GLib

from .video_widget import PipelineManager


here = Path(__file__).parent

builder = Gtk.Builder()
builder.add_from_file(str(here/'widgets.glade'))
builder.add_from_file(str(here/'header.glade'))

main_box = builder.get_object('main_box')
video_widget = builder.get_object('video_widget')
relation_widget = builder.get_object('relation_widget')
header = builder.get_object('header')

pipeline = 'udpsrc port=1234 ! application/x-rtp, payload=12 ! rtph264depay ! avdec_h264 ! xvimagesink sync=false'
pipeline = 'videotestsrc ! xvimagesink sync=false'


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_icon_from_file(str(here/'icons'/'ksurct.png'))
        self.add(main_box)
        # self.set_titlebar(self._create_header())
        video_widget.set_double_buffered(False)
        video_widget.set_app_paintable(True)
        video_widget.connect('realize', self._init_video_widget)

        relation_widget.set_double_buffered(False)
        relation_widget.set_app_paintable(True)
        relation_widget.connect('draw', self._draw_relation_widget)
        GLib.timeout_add(1000/30, self._sced)

    def _create_header(self):
        menu = builder.get_object('menu')
        app_menu = builder.get_object('app-menu')
        menu.bind_model(app_menu, None)
        return header

    def _init_video_widget(self, widget):
        PipelineManager(widget, pipeline)

    def _sced(self):
        relation_widget.queue_draw()
        return True

    def _draw_relation_widget(self, widget, cairo):
        from time import time
        cairo.set_source_rgb(0, 0, 0)
        cairo.paint()
        cairo.set_source_rgb(100, 0, 0)
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


if __name__ == '__main__':
    app = Application()
    try:
        app.run()
    except:
        app.quit()

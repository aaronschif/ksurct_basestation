import pkgutil
from pathlib import Path

from . import gi_init  # noqa
from gi.repository import Gtk, GLib

from .video_widget import GstWidget

here = Path(__file__).parent

builder = Gtk.Builder()
builder.add_from_string(pkgutil.get_data(__package__, 'glade/widgets.glade').decode('utf-8'))
builder.add_from_string(pkgutil.get_data(__package__, 'glade/header.glade').decode('utf-8'))


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        main_box = builder.get_object('main_box')
        self.relation_widget = builder.get_object('relation_widget')

        self.buffer_log = builder.get_object('log')

        self.set_icon_from_file(str(here/'icons'/'ksurct.png'))
        self.add(main_box)
        self.set_titlebar(self._create_header())

        self.relation_widget.connect('draw', self._draw_relation_widget)
        GLib.timeout_add(1000/30, self._sced)
        GLib.timeout_add(1000/4, self.show_log, 'asdf\n')

    def _create_header(self):
        header = builder.get_object('header')
        menu = builder.get_object('menu')
        app_menu = builder.get_object('app-menu')
        menu.bind_model(app_menu, None)
        return header

    def _sced(self):
        self.relation_widget.queue_draw()
        return True

    def _draw_relation_widget(self, widget, cairo):
        cairo.set_source_rgb(.9, .9, .9)
        cairo.paint()  # Grey background
        cairo.set_source_rgb(.1, .1, .1)
        cairo.rectangle(50, 200, 100, 140)
        cairo.stroke()
        cairo.set_source_rgb(1, 0, 0)
        cairo.move_to(54, 190)
        cairo.line_to(54, 100)
        cairo.move_to(146, 190)
        cairo.line_to(146, 100)
        cairo.stroke()

    def show_log(self, msg):
        i = self.buffer_log.get_start_iter()
        self.buffer_log.insert(i, msg)

        i.set_line(100)
        self.buffer_log.delete(i, self.buffer_log.get_end_iter())

        return True

    def start_video(self, pipeline):
        video_area = builder.get_object('video_area')
        video_area.add(GstWidget(pipeline))


class Application(Gtk.Application):
    def __init__(self, config, channel):
        super().__init__(application_id='ksurct.basestation')

        self.window = None
        self.config = config

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="ksurct Basestation")
            self.window.start_video(self.config['video_pipeline'])
            self.window.show_all()

        self.window.present()

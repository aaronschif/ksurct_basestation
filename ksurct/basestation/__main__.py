from pathlib import Path

from . import gi_init
from gi.repository import Gtk

from .video_widget import PipelineManager

from gi.repository import Gtk


here = Path(__file__).parent

builder = Gtk.Builder()
builder.add_from_file(str(here/'widgets.glade'))
builder.add_from_file(str(here/'header.glade'))

main_box = builder.get_object('main_box')
video_widget = builder.get_object('video_widget')
header = builder.get_object('header')

pipeline = 'udpsrc port=1234 ! application/x-rtp, payload=12 ! rtph264depay ! avdec_h264 ! xvimagesink sync=false'


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_icon_from_file(str(here/'icons'/'ksurct.png'))
        self.add(main_box)
        PipelineManager(video_widget, pipeline)
        # self.set_titlebar(self._create_header())

    def _create_header(self):
        menu = builder.get_object('menu')
        app_menu = builder.get_object('app-menu')
        menu.bind_model(app_menu, None)
        return header


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

from gi.repository import Gst, Gdk, GdkX11, GstVideo, Gtk

Gst.init(None)
Gst.init_check(None)


class PipelineManager(object):
    def __init__(self, window, pipeline):
        assert isinstance(window, Gtk.DrawingArea)
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

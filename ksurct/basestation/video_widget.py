from gi.repository import Gst, Gtk

Gst.init(None)
Gst.init_check(None)


class GstWidget(Gtk.Bin):
    def __init__(self, pipeline):
        super().__init__()
        self.connect('realize', self._on_realize)
        self._bin = Gst.parse_bin_from_description(pipeline, True)

    def _on_realize(self, widget):
        pipeline = Gst.Pipeline()
        factory = pipeline.get_factory()
        gtksink = factory.make('gtksink')
        pipeline.add(gtksink)
        pipeline.add(self._bin)
        self._bin.link(gtksink)
        self.add(gtksink.props.widget)
        gtksink.props.widget.show()
        pipeline.set_state(Gst.State.PLAYING)

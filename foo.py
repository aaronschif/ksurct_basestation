#!/usr/bin/env python
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Gst, Gdk, GdkX11, GstVideo
Gst.init(None)

Gst.init_check(None)

pipeline = Gst.parse_launch('videotestsrc ! xvimagesink sync=false')

# overlay = Gtk.Overlay()
drawing = Gtk.DrawingArea()
drawing.set_size_request(640, 480)
# drawing.show()



print(list(filter(lambda e: 'verlay' in e, dir(GstVideo))))

# exit()

def bus_callback(bus, message):
    if message.type is Gst.MessageType.ELEMENT:
        if message.get_structure().get_name() == 'prepare-window-handle':
            Gdk.threads_enter()
            Gdk.Display.get_default().sync()
            win = drawing.get_property('window')
            message.src.set_window_handle(win.get_xid())
            Gdk.threads_leave()
    return Gst.BusSyncReply.PASS


window = Gtk.Window()
window.set_size_request(300, 50)
main_box = Gtk.HBox()
main_box.pack_start(drawing, False, False, 0)
main_box.pack_start(Gtk.Button('Foo'), False, False, 0)
# main_box.pack_start(overlay, False, False, 0)
window.add(main_box)
window.show_all()
window.connect('destroy', lambda w: Gtk.main_quit())

bus = pipeline.get_bus()
bus.set_sync_handler(bus_callback)
pipeline.set_state(Gst.State.PLAYING)

Gtk.main()

# class PlaybackInterface:
#
#     def __init__(self):
#         self.playing = False
#
#         # A free example sound track
#         self.uri = "http://cdn02.cdn.gorillavsbear.net/wp-content/uploads/2012/10/GORILLA-VS-BEAR-OCTOBER-2012.mp3"
#
#         # GTK window and widgets
#         self.window = Gtk.Window()
#         self.window.set_size_request(300,50)
#
#         vbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, 0)
#         vbox.set_margin_top(3)
#         vbox.set_margin_bottom(3)
#         self.window.add(vbox)
#
#         self.playButtonImage = Gtk.Image()
#         self.playButtonImage.set_from_stock("gtk-media-play", Gtk.IconSize.BUTTON)
#         self.playButton = Gtk.Button.new()
#         self.playButton.add(self.playButtonImage)
#         self.playButton.connect("clicked", self.playToggled)
#         Gtk.Box.pack_start(vbox, self.playButton, False, False, 0)
#
#         self.slider = Gtk.HScale()
#         self.slider.set_margin_left(6)
#         self.slider.set_margin_right(6)
#         self.slider.set_draw_value(False)
#         self.slider.set_range(0, 100)
#         self.slider.set_increments(1, 10)
#
#         Gtk.Box.pack_start(vbox, self.slider, True, True, 0)
#
#         self.label = Gtk.Label(label='0:00')
#         self.label.set_margin_left(6)
#         self.label.set_margin_right(6)
#         Gtk.Box.pack_start(vbox, self.label, False, False, 0)
#
#         self.window.show_all()
#
#         # GStreamer Setup
#         Gst.init_check(None)
#         self.IS_GST010 = Gst.version()[0] == 0
#         self.player = Gst.ElementFactory.make("playbin", "player")
#         fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
#         self.player.set_property("video-sink", fakesink)
#         bus = self.player.get_bus()
#         #bus.add_signal_watch_full()
#         bus.connect("message", self.on_message)
#         self.player.connect("about-to-finish",  self.on_finished)
#
#     def on_message(self, bus, message):
#         t = message.type
#         if t == Gst.Message.EOS:
#             self.player.set_state(Gst.State.NULL)
#             self.playing = False
#         elif t == Gst.Message.ERROR:
#             self.player.set_state(Gst.State.NULL)
#             err, debug = message.parse_error()
#             print "Error: %s" % err, debug
#             self.playing = False
#
#         self.updateButtons()
#
#     def on_finished(self, player):
#         self.playing = False
#         self.slider.set_value(0)
#         self.label.set_text("0:00")
#         self.updateButtons()
#
#     def play(self):
#         self.player.set_property("uri", self.uri)
#         self.player.set_state(Gst.State.PLAYING)
#         GObject.timeout_add(1000, self.updateSlider)
#
#     def stop(self):
#         self.player.set_state(Gst.State.NULL)
#
#     def playToggled(self, w):
#         self.slider.set_value(0)
#         self.label.set_text("0:00")
#
#         if(self.playing == False):
#             self.play()
#         else:
#             self.stop()
#
#         self.playing=not(self.playing)
#         self.updateButtons()
#
#     def updateSlider(self):
#         if(self.playing == False):
#            return False # cancel timeout
#
#         try:
#            if self.IS_GST010:
#               nanosecs = self.player.query_position(Gst.Format.TIME)[2]
#               duration_nanosecs = self.player.query_duration(Gst.Format.TIME)[2]
#            else:
#               nanosecs = self.player.query_position(Gst.Format.TIME)[1]
#               duration_nanosecs = self.player.query_duration(Gst.Format.TIME)[1]
#
#            # block seek handler so we don't seek when we set_value()
#            # self.slider.handler_block_by_func(self.on_slider_change)
#
#            duration = float(duration_nanosecs) / Gst.SECOND
#            position = float(nanosecs) / Gst.SECOND
#            self.slider.set_range(0, duration)
#            self.slider.set_value(position)
#            self.label.set_text ("%d" % (position / 60) + ":%02d" % (position % 60))
#
#            #self.slider.handler_unblock_by_func(self.on_slider_change)
#
#         except Exception as e:
#             # pipeline must not be ready and does not know position
#             print e
#             pass
#
#         return True
#
#     def updateButtons(self):
#         if(self.playing == False):
#            self.playButtonImage.set_from_stock("gtk-media-play", Gtk.IconSize.BUTTON)
#         else:
#            self.playButtonImage.set_from_stock("gtk-media-stop", Gtk.IconSize.BUTTON)
#
# if __name__ == "__main__":
#     PlaybackInterface()
#     Gtk.main()
from threading import Event
from collections import namedtuple

from janus import Queue
from gi.repository import GLib


class Channel(object):
    def __init__(self):
        self.aio_gtk = None
        self.gtk_aio = None
        self._aio_ready = Event()
        self._aio_ready.clear()
        self._gtk_ready = Event()
        self._gtk_ready.clear()

        self.gtk_callbacks = set()

    def gtk_init(self, loop):
        self._gtk_ready.set()

    def wait_gtk_init(self):
        self._gtk_ready.wait()

    def complete_gtk_init(self):
        self._gtk_ready.set()

    def gtk_add_callback(self, cb):
        self.gtk_callbacks.add(cb)

    def gtk_send_msg(self, msg):
        pass

    def aio_init(self, loop):
        self.aio_gtk = Queue(loop=loop)
        self.gtk_aio = Queue(loop=loop)
        self._aio_ready.set()

    def wait_aio_init(self):
        self._aio_ready.wait()

    def aio_wait_msg(self):
        pass

    def aio_send_msg(self, msg):
        pass


NewSensorData = namedtuple('NewSensorData', ['left', 'right'])

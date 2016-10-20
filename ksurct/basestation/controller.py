from .server import Server
from .gui import Application


class Controller(object):
    def __init__(self):
        self.application = Application()

    def begin(self):
        self.application.run()

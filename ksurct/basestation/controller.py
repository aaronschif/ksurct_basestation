import sys
import yaml

from .server import Server
from .gui import GuiThread
from .messaging import Channel


class Controller(object):
    def __init__(self):
        config_file = sys.argv[1]
        with open(config_file, 'r') as f:
            config = yaml.load(f)

        self.channel = Channel()
        self.server = Server(config, self.channel)
        self.application = GuiThread(config, self.channel)

    def begin(self):
        try:
            self.application.start()
            self.server.run()
        finally:
            self.application.stop()
            self.application.join()

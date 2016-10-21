import sys
import yaml

from .server import Server
from .gui import Application


class Controller(object):
    def __init__(self):
        config_file = sys.argv[1]
        with open(config_file, 'r') as f:
            config = yaml.load(f)

        self.application = Application(config)

    def begin(self):
        self.application.run()

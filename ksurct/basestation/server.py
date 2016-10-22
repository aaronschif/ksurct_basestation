import asyncio
from threading import Thread


class Server(Thread):
    def __init__(self, config, channel):
        super().__init__(daemon=True)
        self.config = config
        self.channel = channel

    def run(self):
        loop = asyncio.new_event_loop()
        self.channel.aio_init(loop)

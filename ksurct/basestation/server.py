import asyncio
from threading import Thread

from .xbox import Controller

Controller.init()


class Server(Thread):
    def __init__(self, config, channel):
        super().__init__(daemon=True)
        self.config = config
        self.channel = channel
        self.xbox = Controller(0)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.channel.aio_init(loop)

        loop.run_until_complete(self.main_loop())
        loop.close()

    async def main_loop(self):
        while True:
            await asyncio.sleep(1.5)
            self.xbox.update()
            print(self.xbox.formatted_state())

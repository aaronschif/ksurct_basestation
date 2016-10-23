import asyncio
from threading import Thread
from contextlib import suppress

import websockets

from .xbox import Controller
from .proto.main_pb2 import BaseStation

Controller.init()


class XboxComponent(object):
    def __init__(self, **kwargs):
        self.parts = kwargs
        self.state = {k: None for k in kwargs}

    def check_updates(self):
        needs_update = False
        for k, v in self.parts.items():
            new_value = v()
            old_value = self.state[k]
            if new_value != old_value:
                needs_update = True

            self.state[k] = new_value
        return needs_update


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
        lights = XboxComponent(on=self.xbox.get_y)

        async with websockets.connect('ws://10.243.81.158:9002/') as websocket:
            while True:
                self.xbox.update()

                if lights.check_updates():
                    print(lights.state['on'])

                with suppress(asyncio.TimeoutError):
                    msg = await asyncio.wait_for(websocket.recv(), .1)
                    base_msg = BaseStation()
                    base_msg.ParseFromString(msg)

                    print("SD left ", base_msg.sensor_data.front_left)
                    print("SD right ", base_msg.sensor_data.front_right)

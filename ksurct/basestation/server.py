import asyncio
from contextlib import suppress

import websockets

from .xbox2 import Controller
from .proto.main_pb2 import BaseStation, Robot
from .messaging import NewSensorData

Controller.init()


class Toggle(object):
    def __init__(self, cb):
        self.state = False
        self.cb = cb

    def __call__(self):
        self.state ^= self.cb()
        return self.state


def calculate_motor_speed(x, y, mod):
        r, l = -y, -y
        r += -x/4
        l += x/4

        modifier = 120
        if mod:
            modifier = 60

        r = int(r*modifier)
        l = int(l*modifier)
        return r, l


class Server(object):
    def __init__(self, config, channel):
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
        lights = Toggle(self.xbox.y)
        breaks = self.xbox.b
        motors = lambda: calculate_motor_speed(x=self.xbox.left_x(), y=self.xbox.left_y(), mod=self.xbox.x())
        trigger_arm = self.xbox.right_trigger
        close_claw = self.xbox.a
        camera_degree = lambda: self.xbox.right_x() * 190
        # wrist_degree = self.xbox.dpad()
        wrist_degree = lambda: False

        async with websockets.connect('ws://10.243.81.158:9002/') as websocket:
            while True:
                self.xbox.update()

                robot_msg = Robot()

                robot_msg.headlights.update = True
                robot_msg.headlights.on = lights()

                right_speed, left_speed = motors()
                robot_msg.motor_right_rpm.update = True
                robot_msg.motor_right_rpm.speed = right_speed
                robot_msg.motor_right_rpm.breaks = breaks()
                robot_msg.motor_left_rpm.update = True
                robot_msg.motor_left_rpm.speed = left_speed
                robot_msg.motor_left_rpm.breaks = breaks()

                robot_msg.claw.update = True
                robot_msg.claw.degree = close_claw() * 90

                robot_msg.arm.update = True
                robot_msg.arm.degree = 5304 if trigger_arm() else 3120

                robot_msg.wrist.update = True
                robot_msg.wrist.degree = 171 * wrist_degree()

                robot_msg.camera.update = True
                robot_msg.camera.degree = 190 - int(camera_degree())

                ser_msg = robot_msg.SerializeToString()

                await websocket.send(ser_msg)

                with suppress(asyncio.TimeoutError):
                    msg = await asyncio.wait_for(websocket.recv(), .1)
                    base_msg = BaseStation()
                    base_msg.ParseFromString(msg)

                    self.channel.aio_send_msg(NewSensorData(
                        left=base_msg.sensor_data.front_left,
                        right=base_msg.sensor_data.front_right,
                    ))

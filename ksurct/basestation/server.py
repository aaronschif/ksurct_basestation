from time import sleep
from threading import Thread


class Server(Thread):
    def __init__(self):
        super().__init__(daemon=True)

    def run(self):
        while True:
            sleep(1)
            print(1)

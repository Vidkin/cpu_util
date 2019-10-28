import psutil

from datetime import datetime
from time import sleep
from threading import Thread

from common import Singleton

from .rabbitmq_exchange import Sender


class CpuUtil(Thread, metaclass=Singleton):
    def __init__(self, timeout: int = 1, load_limit: int = 60):
        Thread.__init__(self, name='cpu-util')
        self.current_util = None
        self.load_limit = load_limit
        self.timeout = timeout
        self.sender = Sender()

    def run(self):
        while True:
            res = round(psutil.cpu_percent(interval=None))
            if res > self.load_limit:
                self.sender.send_msg(
                    f'{datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")} CPU load exceeded: {res}')
            self.current_util = res
            sleep(self.timeout)

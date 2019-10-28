import time
import threading
try:
    from thread import get_ident
except ImportError:
    from _thread import get_ident

from utils.cpu_util import CpuUtil
from utils.img_generator import get_image


class StreamEvent:
    def __init__(self):
        self.events = {}

    def wait(self):
        ident = get_ident()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        self.events[get_ident()][0].clear()


class Stream:
    thread = None
    frame = None
    event = StreamEvent()

    def __init__(self):
        if Stream.thread is None:
            Stream.thread = threading.Thread(target=self._thread)
            Stream.thread.start()

            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        Stream.event.wait()
        Stream.event.clear()

        return Stream.frame

    @staticmethod
    def frame_generator():
        while True:
            time.sleep(1)  # timeout to update cpu utilization
            yield get_image(str(CpuUtil().current_util))

    @classmethod
    def _thread(cls):
        frames_iterator = cls.frame_generator()
        for frame in frames_iterator:
            Stream.frame = frame
            Stream.event.set()
            time.sleep(0)

        Stream.thread = None

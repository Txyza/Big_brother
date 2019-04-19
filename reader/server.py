from threading import Lock, Condition


class Server:
    def __init__(self):
        # Thread synchronization for all clients
        self._mutex = Lock()
        self._cond = Condition(self._mutex)
        self._last_frame = {}

    def new_frame(self, camera, frame):
        self._mutex.acquire()
        try:
            self._last_frame[camera] = frame
            self._cond.notify_all()
        finally:
            self._mutex.release()

    def get_last_frame(self, camera):
        frame = None

        self._mutex.acquire()
        try:
            self._cond.wait()
            frame = self._last_frame[camera]
        finally:
            self._mutex.release()

        return frame

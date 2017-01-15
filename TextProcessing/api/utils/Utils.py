import time


class StopWatch:
    def __init__(self):
        self.start_mills = 0
        self.end_millis = 0

    def start(self):
        self.start_mills = self.current_milli_time()

    def stop(self):
        self.end_millis = self.current_milli_time()

    def get_run_time(self):
        return self.end_millis - self.start_mills

    def current_milli_time(self):
        return int(round(time.time() * 1000))


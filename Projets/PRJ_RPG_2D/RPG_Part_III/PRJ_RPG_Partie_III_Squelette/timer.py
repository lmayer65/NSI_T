import time

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.is_running = False

    def start(self):
        self.start_time = time.time()
        self.is_running = True

    def stop(self):
        self.is_running = False

    def get_elapsed_time(self):
        if self.is_running:
            return time.time() - self.start_time
        return 0

    def is_expired(self):
        return self.get_elapsed_time() >= self.duration
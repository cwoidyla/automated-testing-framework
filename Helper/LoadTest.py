import threading
from queue import Queue
import time

class LoadTest:
    def __init__(self):
        self.print_lock = threading.Lock()
        self.q = Queue()
        self.blah = "blah"

    def thread_logger(self, message):
        with self.print_lock:
            print()

    def load_modulator(self,thread_num):
        for i in range(thread_num):
            print("starting thread " + thread_num)
            print("delay until other test is a fraction of the way through")
        # TODO: figure out how to calculate system load performance
        # I could store load performance data in sqllite database or Log file

    def web_minion(self, thread_num):
        for job in range(10):
            self.q.put(job)
        for i in range(thread_num):
            thread = threading.Thread(target = self.thread_logger)
        thread.daemon = True # set to False if I want thread to keep running in background
        thread.start()


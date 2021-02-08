import threading
from time import sleep


class Clock(threading.Thread):
    def __init__(self, data, name, interval=3, start_at=0):
        super().__init__()
        self.data = data
        self.name = name
        self.interval = interval
        data[name] = start_at

    def run(self):
        while True:
            sleep(self.interval)
            self.data[self.name] += 1
            print(f'tick {self.name} = {self.data[self.name]}')

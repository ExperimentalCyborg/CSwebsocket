from time import sleep


class Data:
    """
    Simulate an async k/v store or MQTT broker -ish interface.
    This works fine in the demo because of the GIL.
    """
    def __init__(self):
        self.data = {}

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def wait_for_update(self, poll_rate, key, value=None):
        while True:
            if self.data[key] != value:
                return self.data[key]
            else:
                sleep(poll_rate)

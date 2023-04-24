

class Subscriber:
    def notify(self):
        pass


class Publisher:
    def __init__(self, value=None):
        self.value = value
        self.subs = []

    def get_value(self):
        return self.value

    def subscribe(self, subscriber: Subscriber):
        self.subs.append(subscriber)
    def set_value(self, value):
        self.value = value
        for sub in self.subs:
            sub.notify()

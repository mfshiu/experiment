import threading


class ThreadSafeCounter:
    def __init__(self, initial=0):
        self.initial_value = initial
        self.value = self.initial_value
        self.lock = threading.Lock()
    
    def add(self, number):
        with self.lock:
            self.value += number
            value = self.value
        return value
    
    def substract(self, number):
        with self.lock:
            self.value -= number
            value = self.value
        return value
    
    def increment(self):
        with self.lock:
            self.value += 1
            value = self.value
        return value
    
    def decrement(self):
        with self.lock:
            self.value -= 1
            value = self.value
        return value
    
    def reset(self):
        with self.lock:
            self.value = self.initial_value
            value = self.value
        return value

    def get_value(self):
        with self.lock:
            return self.value

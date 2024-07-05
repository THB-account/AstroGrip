from collections import deque

class BufferQueue:
    def __init__(self,sample_object,size):
        self.size = size
        self.container = deque(maxlen=self.size)
        self.sample_object = sample_object
        self.name = sample_object.name
    
    # queue behavior
    def on_full(self):
        for x in self.container:
            pass
        self.container.clear()
    
    def append(self,scalar):
        self.container.append(scalar)
        if len(self.container) == self.size:
            self.on_full()

    # sample/sensor behavior
    def sample(self):
        self.append(self.sample_object.sample())

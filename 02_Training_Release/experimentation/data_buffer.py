import numpy as np
from collections import deque
import timeit

class A:
    def __init__(self,size):
        self.size = size
        self.container = np.ndarray((self.size,))
        self.head = 0

    def on_full(self):
        self.head = 0
        for x in np.nditer(self.container):
            pass
    
    def append(self,scalar):
        self.container[self.head] = scalar
        self.head += 1
        if self.head == self.size:
            self.on_full()

class B:
    def __init__(self,size):
        self.size = size
        self.container = deque(maxlen=self.size)
        

    def on_full(self):
        for x in self.container:
            pass
        self.container.clear()
    
    def append(self,scalar):
        self.container.append(scalar)
        if len(self.container) == self.size:
            self.on_full()


size = 400
a = A(size)
b = B(size)


def f1(c):
    for i in range(405):
        c.append(i)


iter = 10000
t1 = timeit.timeit(lambda : f1(a),number=iter)
t2 = timeit.timeit(lambda : f1(b),number=iter)

print("time 1 :\t",t1)
print("time 2 :\t",t2)


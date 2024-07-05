import collections
import matplotlib.pyplot as plt
import timeit
import numpy as np

d = collections.deque(maxlen=30)

class CircularBuffer():
    def __init__(self,size):
        self.size = size
        self.container = np.zeros(self.size)
        self.head = 0
        self.tail = 0

    def enqueue(self, scalar):
        self.container[self.tail] = scalar
        self.tail += 1
        if self.tail-self.head == self.size:
            

    def dequeue(self):
        pass

    def clear(self):
        pass

    def data(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        
        

def f1_app(d):
    [d.append(i) for i in range(60)]

def f1_
    

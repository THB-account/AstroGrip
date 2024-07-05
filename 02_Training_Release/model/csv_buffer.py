from collections import deque
from time import time

from model.abstract_buffer import AbstractBufferQueue
from data.access import write_data2csv

class CSVBufferQueue(AbstractBufferQueue):
    def __init__(self,sample_object,size,data_buffer_size=0,time_buffer=False):
        super().__init__(sample_object)
        if data_buffer_size<0:
            raise Exception("Invalid Value of data_buffer_size in CSV BufferQueue {self.name} of {data_buffer_size}.")
        
        self.__size = size
        self.__container = deque(maxlen=self.__size)
        self.__use_time = time_buffer
        if data_buffer_size>0:
            self.__data_buffer = deque(maxlen=data_buffer_size)
            if time_buffer:
                self.__time_buffer = deque(maxlen=data_buffer_size)
    
    # queue behavior
    def on_full(self):
        write_data2csv(self.__container,self.name)
        self.__container.clear()
    
    def append(self,values):
        t = time()
        # buffer for plotting
        self.__data_buffer.append(values)
        if self.__use_time:
            self.__time_buffer.append(t)
        # buffer for storage
        self.__container.append((values,t))
        if len(self.__container) == self.__size:
            self.on_full()

    # sample/sensor behavior
    def sample(self):
        self.append(self._sample_object.sample())

    def close(self):
        self._sample_object.turn_off()

    @property
    def data_buffer(self):
        return self.__data_buffer
    
    @property
    def use_time(self):
        return self.__use_time

    @property
    def time_buffer(self):
        return self.__time_buffer

    
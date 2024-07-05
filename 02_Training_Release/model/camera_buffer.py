from model.abstract_buffer import AbstractBufferQueue
from data.access import write_data2image
from collections import deque
from time import time

class CameraBufferQueue(AbstractBufferQueue):
    def __init__(self,sample_object, data_buffer_size=0, time_buffer=False):
        super().__init__(sample_object)
        if data_buffer_size<0:
            raise Exception("Invalid Value of data_buffer_size in CSV BufferQueue {self.name} of {data_buffer_size}.")
        self.__container = None
        self.__last_uuid = None # for passing a reference to the image for plotting
        self.__open_jobs = 0    # for tracking how many pictures still need to be taken
        # this is due to the fact that a user could press the record button multiple times
        self.__use_time = None
        self.__data_buffer = None
        self.__time_buffer = None

    
    # queue behavior
    def on_full(self):
        self.__last_uuid = write_data2image(self.__container,self.name)
        self.__container = None

    
    def append(self,values):
        self.__container = values
        self.on_full()

    # sample/sensor behavior
    def sample(self):
        if self.__open_jobs<=0:
            raise Exception("CameraBufferQueue reached illegal state trying to take picture when no pending jobs exist.")
        self.__open_jobs-=1

        # TODO add exception check here
        self.append(self._sample_object.sample())
        
    def close(self):
        self._sample_object.turn_off()

    def transition(self):
        while self.__open_jobs>0:
            self.sample()

    def open_job(self):
        self.__open_jobs +=1

    def on_shutdown(self):
        pass

    def check_for_jobs(self):
        return (self.__open_jobs>0)

    @property
    def last_job(self):
        return self.__last_uuid
    
    @property
    def data_buffer(self):
        return self.__data_buffer
    
    @property
    def use_time(self):
        return self.__use_time

    @property
    def time_buffer(self):
        return self.__time_buffer
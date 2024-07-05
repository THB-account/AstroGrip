class AbstractBufferQueue:
    def __init__(self,sample_object):
        if sample_object==None:
            raise Exception("None sample_object passed to BufferQueue.")
        self._sample_object = sample_object
    
    # queue behavior
    def on_full(self):
        raise NotImplementedError()
    
    def append(self,scalar):
        raise NotImplementedError()

    # sample/sensor behavior
    def sample(self):
        raise NotImplementedError()
    
    def close(self):
        raise NotImplementedError()

    def transition(self):
        pass
    
    def open_job(self):
        pass

    def on_shutdown(self):
        self.on_full()
    
    @property
    def name(self):
        return self._sample_object.name
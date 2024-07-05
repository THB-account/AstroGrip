import AbstractSensor
from numpy.random import normal

class GaussianSensor(AbstractSensor):
    def __init__(self,name,mean=0,cov=1):
        self.name = name
        self.mean = mean
        self.cov = cov

    def __initialize_sensor(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        raise NotImplementedError()

    def sample(self):
        return normal(self.mean,self.cov)
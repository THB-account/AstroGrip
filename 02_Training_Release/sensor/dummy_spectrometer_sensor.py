from sensor.abstract_sensor import AbstractSensor
from numpy.random import normal

class SpectrometerSensor(AbstractSensor):
    def __init__(self,name,mean=0,cov=1):
        super().__init__(name)
        self.__initialize_sensor()
        self.mean = mean
        self.cov = cov

    def __initialize_sensor(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def sample(self):
        return [normal(self.mean,self.cov) for _ in range(19)]
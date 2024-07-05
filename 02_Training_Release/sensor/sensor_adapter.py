from sensor.abstract_sensor import AbstractSensor

class AdapterSensor(AbstractSensor):
    def __init__(self,name, sensor,sample_func):
        super().__init__(name)
        self.__sensor = sensor
        self.__sample_func = sample_func
        

    def __initialize_sensor(self):
        pass

    def turn_on(self):
        self.__sensor.turn_on()

    def turn_off(self):
        self.__sensor.turn_off()

    def sample(self):
        return self.__sample_func(self.__sensor)
    
    def state_transition(self):
        self.__sensor.state_transition()

    @property
    def name(self):
        return self.__sensor.name
    
    @property
    def sensor(self):
        return self.__sensor

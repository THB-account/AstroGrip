from sensor.abstract_sensor import AbstractSensor

class SensorWrapper(AbstractSensor):
    def __init__(self,sensor, access_function):
        self.__sensor = sensor
        self.__access_function = access_function

    def __initialize_sensor(self):
        pass

    def turn_on(self):
        self.__sensor.turn_on()

    def turn_off(self):
        self.__sensor.turn_off()

    def sample(self):
        return self.__access_function(self.__sensor)
    
    def state_transition(self):
        self.__sensor.transition()

    @property
    def name(self):
        return self.__sensor.name

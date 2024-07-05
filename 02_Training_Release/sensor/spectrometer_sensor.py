from sensor.abstract_sensor import AbstractSensor
from sensor.drivers.spectrometer.spectrometer import i2c,readCAL#,readRAW


class SpectrometerSensor(AbstractSensor):
    def __init__(self,name):
        super().__init__(name)
        self.__initialize_sensor()
        
    def __initialize_sensor(self):
        # file defines own i2c connection
        # should only be closed on shut down
        self.__i2c = i2c

    # is already open on start
    def turn_on(self):
        self.__i2c.open()

    def turn_off(self):
        # defined in another file,
        self.__i2c.close()

    def sample(self):
        return readCAL()
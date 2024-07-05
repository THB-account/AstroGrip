from sensor.abstract_sensor import AbstractSensor
from sensor.drivers.bmp581.smbus_adaption import ByteSMBus
from sensor.drivers.bmp581.bmp581 import BMP581
from time import sleep

class BMP581Sensor(AbstractSensor):
    def __init__(self,name):
        super().__init__(name)
        self.__initialize_sensor()
        
    def __initialize_sensor(self):
        """
        1. Initialize Smbus class
        """
        self.__bus = ByteSMBus(1)
        sleep(1)
        self.__open = True
        self.__bmp = BMP581(self.__bus, address=0x47) # standard adress 0x47 is assumed
        # burn trough first recording
        _ = self.__bmp.temperature
        _ = self.__bmp.pressure

    def turn_on(self):
        self.__open = True
        self.__bus.open()

    def turn_off(self):
        self.__open = False
        self.__bus.close()

    def sample_pressure(self):
        """
        1. with smbus as i2c:
            - read values depending on configuration
        """
        if not self.__open:
            self.turn_on()
        return self.__bmp.pressure

    def sample_temperature(self):
        if not self.__open:
            self.turn_on()
        return self.__bmp.temperature

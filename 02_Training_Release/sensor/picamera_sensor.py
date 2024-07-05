from sensor.abstract_sensor import AbstractSensor
from picamera2 import Picamera2
from time import sleep

class CameraSensor(AbstractSensor):
    def __init__(self,name):
        super().__init__(name)
        self.__initialize_sensor()
        
    def __initialize_sensor(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def sample(self):
        with Picamera2() as cam:
            cam.start()
            time.sleep(1)
            image = cam.capture_image("main")
        
        return image

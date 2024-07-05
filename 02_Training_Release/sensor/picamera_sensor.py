from sensor.abstract_sensor import AbstractSensor
from picamera import PiCamera
from PIL import Image
from time import sleep
from io import BytesIO

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
        with PiCamera as cam:
            # Create the in-memory stream
            stream = BytesIO()
            cam.start_preview()
            sleep(2)
            cam.capture(stream, format='jpeg')
            # "Rewind" the stream to the beginning so we can read its content
            stream.seek(0)
            image = Image.open(stream) 
        
        return image